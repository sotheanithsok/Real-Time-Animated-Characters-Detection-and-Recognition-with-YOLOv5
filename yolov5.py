from pathlib import Path
from urllib3 import PoolManager
from zipfile import ZipFile
from distutils import dir_util
import argparse
import json

ROOT = Path(__file__).parent


def yolov5_no_update(wd: Path):
    """Modify YOLOv5 files such that it stops checking for update with git when training. 

    Args:
        wd (Path): YOLOv5 path. 
    """
    with open(wd / "train.py", "r+") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "check_git_status()" in line:
                lines[i] = lines[i].replace("check_git_status()", "#check_git_status()")
        f.seek(0)
        f.writelines(lines)


def yolov5_visualize_no_new_folders(wd: Path):
    """Modify YOLOv5 files such that it stops creating new folders when visualizing layers.

    Args:
        wd (Path): YOLOv5 path.
    """
    with open(wd / "detect.py", "r+") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if (
                "visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False"
                in line
            ):
                lines[i] = lines[i].replace(
                    "visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False",
                    "visualize = increment_path(save_dir / Path(path).stem, mkdir=True, exist_ok=exist_ok) if visualize else False",
                )
        f.seek(0)
        f.writelines(lines)


def yolov5_add_init(wd: Path):
    """Modifying YOLOv5 files such that it can be imported as a package.

    Args:
        wd (Path): YOLOv5 path.
    """
    with open(wd / "__init__.py", "w") as f:
        f.seek(0)
        f.write(
            "from _yolov5.train import run as train\nfrom _yolov5.val import run as val\nfrom _yolov5.detect import run as detect"
        )


def yolov5(
    overwrite: bool = False,
) -> None:

    # Load settings.json
    with open(ROOT / "settings.json") as f:
        settings = json.load(f)

    # Create variables
    yolov5 = ROOT / settings["yolov5"]
    url = settings["yolov5_url"]

    # Remove all files in the directory if overwrite is true
    if overwrite and yolov5.exists():
        dir_util.remove_tree(str(yolov5))

    # Create the directory if it doesn't exist
    yolov5.mkdir(exist_ok=True)

    # Download the YOLOv5 zip file from github
    yolov5_zip = yolov5 / "yolov5.zip"
    if not yolov5_zip.exists():
        http = PoolManager()
        req = http.request("GET", url)
        with open(yolov5_zip, "wb") as f:
            f.write(req.data)

    # Extract the zip file to a temporary folder
    zipfile = ZipFile(yolov5_zip)
    zipfile.extractall(yolov5)
    zipfile.close()
    temp = yolov5 / zipfile.filelist[0].filename

    # Copy contents of the temporary folder to the YOLOv5 folder
    dir_util.copy_tree(str(temp), str(yolov5))

    # Modify YOLOv5 files for various purposes
    yolov5_no_update(yolov5)
    yolov5_visualize_no_new_folders(yolov5)
    yolov5_add_init(yolov5)

    # Remove the temporary folder
    dir_util.remove_tree(temp)


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    yolov5(overwrite=opt.overwrite)
