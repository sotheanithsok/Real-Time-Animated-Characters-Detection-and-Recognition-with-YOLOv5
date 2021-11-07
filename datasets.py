from pathlib import Path
from distutils import dir_util
from zipfile import ZipFile
from ruamel.yaml import YAML
import numpy as np
import argparse
from mega import Mega
import json
import os

ROOT = Path(__file__).parent


def train_test_split(x: np.array, y: np.array, split: float = 0.7):
    """Split given dataset into train dataset and test dataset

    Args:
        x (np.array): data.
        y (np.array): labels.
        split (float, optional): splitting ratio. Defaults to 0.7.

    Returns:
        tuple: train_data, train_labels, test_data, test_labels
    """
    x = np.array(x)
    y = np.array(y)

    indices = np.random.choice(range(len(x)), int(split * len(x)), replace=False)

    return x[indices], y[indices], np.delete(x, indices), np.delete(y, indices)


def datasets(
    overwrite: bool = False,
):
    # Load settings.json
    with open(ROOT / "settings.json") as f:
        settings = json.load(f)

    # Create variables
    datasets = ROOT / settings["datasets"]
    url = settings["datasets_url"][settings["datasets_select"]]
    ratios = settings["ratios"]

    # Remove all files in the directory if overwrite is true
    if overwrite and datasets.exists():
        dir_util.remove_tree(str(datasets))

    # Create the directory if it doesn't exist
    datasets.mkdir(exist_ok=True)

    # Download zip files and extract it to a temporary folder
    datasets_zip = datasets / "dataset.zip"
    datasets_unzip = datasets / "temp"
    datasets_unzip.mkdir(exist_ok=True)

    # If dataset zip file hasn't downlaod yet
    if not datasets_zip.exists():
        try:
            m = Mega().login()
            m.download_url(url, str(datasets_zip.parent), datasets_zip.name)
        except:
            pass

    # Extract the zip file to a temporary folder
    zipfile = ZipFile(datasets_zip)
    zipfile.extractall(datasets_unzip)
    zipfile.close()

    # Update images and lables filenames
    for f in datasets_unzip.rglob("*"):
        new_name = f.stem.split("_")[0]
        f.rename(f.parent / f"{new_name}{f.suffix}")

    # Split the dataset into train, val, and test
    # Path to the 3 folders
    train = datasets_unzip / "train"
    val = datasets_unzip / "val"
    test = datasets_unzip / "test"

    # Create dataset folders
    train.mkdir(exist_ok=True)
    val.mkdir(exist_ok=True)
    test.mkdir(exist_ok=True)

    # Create images folders
    (train / "images").mkdir(exist_ok=True)
    (val / "images").mkdir(exist_ok=True)
    (test / "images").mkdir(exist_ok=True)

    # Create labels folders
    (train / "labels").mkdir(exist_ok=True)
    (val / "labels").mkdir(exist_ok=True)
    (test / "labels").mkdir(exist_ok=True)

    # Find all images and all labels
    images = list((train / "images").glob("*"))
    labels = list((train / "labels").glob("*"))

    # Split all dataset into 70% training and 30% unused
    train_images, train_labels, images, labels = train_test_split(images, labels)
    val_images, val_labels, test_images, test_labels = train_test_split(images, labels)

    # Move val dataset from train folder into val folder
    for image, label in zip(val_images, val_labels):
        os.rename(str(image), str(val / "images" / image.name))
        os.rename(str(label), str(val / "labels" / label.name))

    # Move test dataset from train folder into test folder
    for image, label in zip(test_images, test_labels):
        os.rename(str(image), str(test / "images" / image.name))
        os.rename(str(label), str(test / "labels" / label.name))

    # Split the dataset into 4 datasets with different size
    # Form paths and create the four datasets folders
    mini_datasets = [datasets / str(ratio) for ratio in ratios]
    [mini_dataset.mkdir(exist_ok=True) for mini_dataset in mini_datasets]

    # Start the splitting process
    for mini_dataset, ratio in zip(mini_datasets, ratios):
        # Copy contents from the temporary folder the the dataset folder
        dir_util.copy_tree(
            str(datasets_unzip),
            str(mini_dataset),
        )

        # Update yaml file with train, val, and test paths of the dataset
        train_path = mini_dataset / "train"
        val_path = mini_dataset / "valid"
        test_path = mini_dataset / "test"

        yaml = YAML()
        yaml.width = 4096
        data = None

        with open(mini_dataset / "data.yaml", "r") as f:
            data = yaml.load(f)

        if data:
            data["train"] = str(train_path / "images")
            data["val"] = str(val_path / "images")
            data["test"] = str(test_path / "images")

        with open(mini_dataset / "data.yaml", "w") as f:
            yaml.dump(data, f)

        # Adjust the size of train, val, and test data of the dataset
        for local_path in [train_path, val_path, test_path]:
            images = list((local_path / "images").glob("*"))
            labels = list((local_path / "labels").glob("*"))
            choices = np.random.choice(
                range(0, len(images)), int((1 - ratio) * len(images)), replace=False
            )
            for i in choices:
                images[i].unlink()
                labels[i].unlink()

    # Remove temp folders
    dir_util.remove_tree(datasets_unzip)


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
