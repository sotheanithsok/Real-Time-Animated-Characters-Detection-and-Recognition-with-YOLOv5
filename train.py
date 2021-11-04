from os import name
import sys
from pathlib import Path
from distutils import dir_util
import json
import argparse


# Add yolov5 folder to path
ROOT = Path(__file__).parent


def train(overwrite: bool = False, visualize: bool = False, resume: bool = False):
    # Load settings.json
    with open(ROOT / "settings.json") as f:
        settings = json.load(f)

    # Create variables
    datasets = ROOT / settings["datasets"]
    models = ROOT / settings["models"]
    yolov5 = ROOT / settings["yolov5"]

    # Add yolov5 to path and import it
    sys.path.append(str(yolov5))
    import _yolov5 as yolov5

    if overwrite and models.exists():
        dir_util.remove_tree(models)
    models.mkdir(exist_ok=True)

    datasets = list(filter(lambda dataset: dataset.is_dir(), datasets.glob("*/")))

    for dataset in datasets:
        # Hyperparameter
        pretrained_weights = "yolov5s.pt"
        epochs = 10000
        batch_size = 32
        patience = 100

        # Other paremeters
        device = 0

        # Train a model
        yolov5.train(
            weights=models / "weights" / pretrained_weights,
            data=dataset / "data.yaml",
            epochs=epochs,
            batch_size=batch_size,
            device=device,
            project=models / dataset.name,
            name="train",
            exist_ok=True,
            patience=patience,
            save_period=10,
            resume=True,
        )

        # Validate the model with test dataset
        yolov5.val(
            data=dataset / "data.yaml",
            weights=models / dataset.name / "train/weights/best.pt",
            batch_size=batch_size,
            task="test",
            device=device,
            verbose=True,
            save_txt=True,
            save_conf=True,
            save_json=True,
            project=models / dataset.name,
            name="test",
            exist_ok=True,
        )

        # Detect bounding boxes and coffidence with the dataset
        yolov5.detect(
            weights=models / dataset.name / "train/weights/best.pt",
            source=dataset / "test/images",
            imgsz=[640, 640],
            device=device,
            save_txt=True,
            save_conf=True,
            save_crop=True,
            visualize=visualize,
            project=models / dataset.name,
            name="detect",
            exist_ok=True,
        )


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    parser.add_argument(
        "-v", "--visualize", action="store_true", help="visualize model's layers"
    )
    parser.add_argument(
        "-r", "--resume", action="store_true", help="resume training"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    train(overwrite=opt.overwrite, visualize=opt.visualize, resume=opt.resume)
