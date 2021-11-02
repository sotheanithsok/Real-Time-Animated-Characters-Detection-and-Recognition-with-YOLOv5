
from pathlib import Path
from distutils import dir_util
from urllib3 import PoolManager
from zipfile import ZipFile
from ruamel.yaml import YAML
import numpy as np
import os
import argparse

ROOT = Path(__file__).parent


def datasets(
    overwrite: bool = False,
    url: str = "https://drive.google.com/file/d/1t07yKW2yxeRJa-8ZMX0tmuQqki-NeE8z/view?usp=sharing",
    datasets_path: Path = ROOT / "datasets",
):
    # Remove all files in the directory if overwrite is true
    if overwrite and datasets_path.exists():
        dir_util.remove_tree(str(datasets_path))

    # Create the directory if it doesn't exist
    datasets_path.mkdir(exist_ok=True)

    # Download zip files and extract it to a temporary folder
    zip_file_path = datasets_path / "dataset.zip"
    unzip_folder_path = datasets_path / "temp"
    unzip_folder_path.mkdir(exist_ok=True)

    # If dataset zip file hasn't downlaod yet
    if not zip_file_path.exists():
        # Parse and generate download url
        file_id = url.split("/")[5]
        url = f"https://docs.google.com/uc?export=download&id={file_id}"

        # Download the dataset zip file from google drive
        http = PoolManager()
        req = http.request("GET", url)
        zip_file_path = datasets_path / "dataset.zip"
        with open(zip_file_path, "wb") as f:
            f.write(req.data)

    # Extract the zip file to a temporary folder
    zipfile = ZipFile(zip_file_path)
    zipfile.extractall(unzip_folder_path)
    zipfile.close()

    # Split the dataset into 4 datasets with different size
    # Form paths and create the four datasets folders
    _25_dataset_path = datasets_path / "0.25"
    _50_dataset_path = datasets_path / "0.50"
    _75_dataset_path = datasets_path / "0.75"
    _100_dataset_path = datasets_path / "1.00"
    _25_dataset_path.mkdir(exist_ok=True)
    _50_dataset_path.mkdir(exist_ok=True)
    _75_dataset_path.mkdir(exist_ok=True)
    _100_dataset_path.mkdir(exist_ok=True)

    # Pair the 4 datasets path with its respecitve size
    paths_and_sizes = zip(
        [_25_dataset_path, _50_dataset_path, _75_dataset_path, _100_dataset_path],
        [0.25, 0.5, 0.75, 1.0],
    )

    # Start the splitting process
    for path, size in paths_and_sizes:
        # Copy contents from the temporary folder the the dataset folder
        dir_util.copy_tree(
            str(unzip_folder_path),
            str(path),
        )

        # Update yaml file with train, val, and test paths of the dataset
        train_path = path / "train"
        val_path = path / "valid"
        test_path = path / "test"

        yaml = YAML()
        yaml.width = 4096
        data = None

        with open(path / "data.yaml", "r") as f:
            data = yaml.load(f)

        if data:
            data["train"] = str(train_path / "images")
            data["val"] = str(val_path / "images")
            data["test"] = str(test_path / "images")

        with open(path / "data.yaml", "w") as f:
            yaml.dump(data, f)

        # Adjust the size of train, val, and test data of the dataset
        for local_path in [train_path, val_path, test_path]:
            images = list((local_path / "images").glob("*"))
            labels = list((local_path / "labels").glob("*"))
            choices = np.random.choice(
                range(0, len(images)), int((1 - size) * len(images)), replace=False
            )
            for i in choices:
                images[i].unlink()
                labels[i].unlink()

    # Remove temp folders
    dir_util.remove_tree(unzip_folder_path)


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    datasets(overwrite=opt.overwrite)
