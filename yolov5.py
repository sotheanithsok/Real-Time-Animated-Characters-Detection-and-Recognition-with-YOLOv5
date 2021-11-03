from pathlib import Path
from urllib3 import PoolManager
from zipfile import ZipFile
from distutils import dir_util
import argparse

ROOT = Path(__file__).parent


def yolov5(
    overwrite: bool = False,
    url: str = "https://github.com/ultralytics/yolov5/archive/refs/heads/master.zip",
    yolov5_path: Path = ROOT / "yolov5",
) -> None:

    # Remove all files in the directory if overwrite is true
    if overwrite and yolov5_path.exists():
        dir_util.remove_tree(str(yolov5_path))

    # Create the directory if it doesn't exist
    yolov5_path.mkdir(exist_ok=True)

    # Download the YoloV5 zip file from github
    http = PoolManager()
    req = http.request("GET", url)
    yolov5_zip_path = yolov5_path / "yolov5.zip"
    with open(yolov5_zip_path, "wb") as f:
        f.write(req.data)

    # Extract the zip file
    zipfile = ZipFile(yolov5_zip_path)
    zipfile.extractall(yolov5_path)
    zipfile.close()

    # Copy extracted files to the correct folder
    src = yolov5_path / zipfile.filelist[0].filename
    dst = yolov5_path
    dir_util.copy_tree(str(src), str(dst))

    # Stop yolov5 from checking update with github
    with open (yolov5_path/'train.py', 'r+') as f:
        lines = f.readlines()
        for i, line  in enumerate(lines):
            if 'check_git_status()' in line:
                lines[i] = lines[i].replace('check_git_status()', '#check_git_status()')
        f.seek(0)
        f.writelines(lines)

    # Remove unnecessary files
    dir_util.remove_tree(src)
    yolov5_zip_path.unlink()


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
