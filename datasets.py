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
    """Split a given dataset into train dataset and test dataset

    Args:
        x (np.array): data.
        y (np.array): labels.
        split (float, optional): splitting ratio. Defaults to 0.7.

    Returns:
        tuple: train_data, train_labels, test_data, test_labels
    """
    indices = np.random.choice(range(len(x)), int(split * len(x)), replace=False)

    return x[indices], y[indices], np.delete(x, indices), np.delete(y, indices)


def train_valid_test_split(wd: Path, ratio: float = 1.0):
    """Split the dataset in a given directory into three datasets: train, valid, and test.

    Args:
        wd (Path): dataset path.
        ratio (float, optional): the percentage of data to keep. Defaults to 1.0.
    """
    # Form paths to the three datasets: train, valid, test
    train = wd / "train"
    valid = wd / "valid"
    test = wd / "test"

    # Create images folders for all datasets
    (train / "images").mkdir(parents=True, exist_ok=True)
    (valid / "images").mkdir(parents=True, exist_ok=True)
    (test / "images").mkdir(parents=True, exist_ok=True)

    # Create labels folders for all datasets
    (train / "labels").mkdir(parents=True, exist_ok=True)
    (valid / "labels").mkdir(parents=True, exist_ok=True)
    (test / "labels").mkdir(parents=True, exist_ok=True)

    # Find the dataset
    images = np.array(list((train / "images").glob("*")))
    labels = np.array(list((train / "labels").glob("*")))

    # Remove data from the dataset until a certain percentage of data remained
    size = len(images)
    indices = np.random.choice(range(size), int((1.0 - ratio) * size), replace=False)
    for image, label in zip(images[indices], labels[indices]):
        image.unlink()
        label.unlink()
    images = np.delete(images, indices)
    labels = np.delete(labels, indices)

    # Split the dataset into train, valid, and test
    train_images, train_labels, images, labels = train_test_split(images, labels)
    valid_images, valid_labels, test_images, test_labels = train_test_split(
        images, labels
    )

    # Move data from the train dataset into the valid dataset
    for image, label in zip(valid_images, valid_labels):
        os.rename(str(image), str(valid / "images" / image.name))
        os.rename(str(label), str(valid / "labels" / label.name))

    # Move data from the train dataset into the test dataset
    for image, label in zip(test_images, test_labels):
        os.rename(str(image), str(test / "images" / image.name))
        os.rename(str(label), str(test / "labels" / label.name))

    # Update data.yaml
    yaml = YAML()
    yaml.width = 4096
    data = None
    with open(wd / "data.yaml", "r") as f:
        data = yaml.load(f)
    if data:
        data["train"] = str(train / "images")
        data["val"] = str(valid / "images")
        data["test"] = str(test / "images")
    with open(wd / "data.yaml", "w") as f:
        yaml.dump(data, f)


def datasets(
    overwrite: bool = False,
):
    # Load settings.json
    with open(ROOT / "settings.json") as fil:
        settings = json.load(fil)

    # Create variables
    datasets = ROOT / settings["datasets"]
    url = settings["datasets_url"][settings["datasets_select"]]
    ratios = settings["ratios"]

    # Remove all files in the directory if overwrite is true
    if overwrite and datasets.exists():
        dir_util.remove_tree(str(datasets))

    # Make the directory if it doesn't exist
    datasets.mkdir(exist_ok=True)

    # Download the dataset zip file
    dataset_zip = datasets / "dataset.zip"
    if not dataset_zip.exists():
        try:
            m = Mega().login()
            m.download_url(url, str(dataset_zip.parent), dataset_zip.name)
        except:
            pass

    # Extract the zip file into a temporary folder
    temp = datasets / "temporary"
    temp.mkdir(exist_ok=True)
    zipfile = ZipFile(dataset_zip)
    zipfile.extractall(temp)
    zipfile.close()

    # Update filenames of images and labels
    for fil in temp.rglob("*"):
        new_name = fil.stem.split("_")[0]
        fil.rename(fil.parent / f"{new_name}{fil.suffix}")

    # Create new datasets from the dataset based on given ratios
    for ratio in ratios:
        src = temp
        dst = datasets / str(ratio)

        # Copy contents from the temporary folder to the new dataset folder
        dir_util.copy_tree(str(src), str(dst))

        # Split the new dataset into train, val, test dataset with a given ratio
        train_valid_test_split(dst, ratio)

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
    datasets(overwrite=opt.overwrite)
