import sys
from pathlib import Path
from distutils import dir_util
import json
import argparse


# Add yolov5 folder to path
ROOT = Path(__file__).parent


def train(overwrite: bool = False):
    # Load settings.json
    with open(ROOT / "settings.json") as f:
        settings = json.load(f)

    # Create variables
    datasets = ROOT / settings["datasets"]
    models = ROOT / settings["models"]
    yolov5 = ROOT / settings["yolov5"]
    images_size = settings["datasets_images_size"][settings["datasets_select"]]

    # Add yolov5 to path and import it
    sys.path.append(str(yolov5))
    import _yolov5 as yolov5

    if overwrite and models.exists():
        dir_util.remove_tree(models)
    models.mkdir(exist_ok=True)

    datasets = list(filter(lambda dataset: dataset.is_dir(), datasets.glob("*/")))

    for dataset in datasets:
        # Hyperparameter
        # Max batch_size for 12gb vram
        # 1280   => XL: 1,  L: 4,    M: 6,      S: 14,       N: 26
        # 640    => XL: 8,  L: 16,   M: 30,     S: 60,      N: 104
        weights = "yolov5n.pt"
        epochs = 300
        batch_size = 104
        patience = 300

        # Other paremeters
        device = 0

        # Pick the correct pretrained weights based on the dataset
        weights = (
            weights[: weights.find(".")] + "6" + weights[weights.find(".") :]
            if settings["datasets_select"] == 1
            else weights
        )

        # Train a model
        yolov5.train(
            weights=models / weights,
            data=dataset / "data.yaml",
            epochs=epochs,
            batch_size=batch_size,
            imgsz=images_size,
            device=device,
            project=models / dataset.name,
            name="train",
            exist_ok=True,
            patience=patience
        )

        # Validate the model with test dataset
        yolov5.val(
            data=dataset / "data.yaml",
            weights=models / dataset.name / "train/weights/best.pt",
            batch_size=batch_size,
            imgsz=images_size,
            task="test",
            device=device,
            verbose=True,
            project=models / dataset.name,
            name="test",
            exist_ok=True,
        )

        # Detect bounding boxes and coffidence with the dataset
        yolov5.detect(
            weights=models / dataset.name / "train/weights/best.pt",
            source=dataset / "test/images",
            imgsz=[images_size, images_size],
            device=device,
            save_txt=True,
            save_conf=True,
            save_crop=True,
            project=models / dataset.name,
            name="test",
            exist_ok=True,
        )


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    train(overwrite=opt.overwrite)
