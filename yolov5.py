from pathlib import Path
from urllib3 import PoolManager
from zipfile import ZipFile
from distutils import dir_util
import argparse
import json

ROOT = Path(__file__).parent


def yolov5(
    overwrite: bool = False,
) -> None:

    # Load settings.json
    with open(ROOT / "settings.json") as f:
        settings = json.load(f)

    #Create variables
    yolov5 = ROOT/settings['yolov5']
    url = settings['yolov5_url']

    # Remove all files in the directory if overwrite is true
    if overwrite and yolov5.exists():
        dir_util.remove_tree(str(yolov5))

    # Create the directory if it doesn't exist
    yolov5.mkdir(exist_ok=True)

    # Download the YoloV5 zip file from github
    http = PoolManager()
    req = http.request("GET", url)
    yolov5_zip = yolov5 / "yolov5.zip"
    with open(yolov5_zip, "wb") as f:
        f.write(req.data)

    # Extract the zip file
    zipfile = ZipFile(yolov5_zip)
    zipfile.extractall(yolov5)
    zipfile.close()

    # Copy extracted files to the correct folder
    yolov5_unzip = yolov5 / zipfile.filelist[0].filename
    dir_util.copy_tree(str(yolov5_unzip), str(yolov5))

    # Stop yolov5 from checking update with github
    with open(yolov5 / "train.py", "r+") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "check_git_status()" in line:
                lines[i] = lines[i].replace("check_git_status()", "#check_git_status()")
        f.seek(0)
        f.writelines(lines)

    # Stop yolov5 from creating new folders when visualizing model's layers
    with open(yolov5 / "detect.py", "r+") as f:
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

    # Update yolov5 to work as a package
    with open(yolov5 / "__init__.py", "w") as f:
        f.seek(0)
        f.write(
            "from yolov5.train import run as train\nfrom yolov5.val import run as val\nfrom yolov5.detect import run as detect"
        )

    # Remove unnecessary files
    dir_util.remove_tree(yolov5_unzip)
    yolov5_zip.unlink()


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
