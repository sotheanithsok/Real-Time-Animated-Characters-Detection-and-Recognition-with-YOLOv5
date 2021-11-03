import sys
from pathlib import Path
from distutils import dir_util


# Add yolov5 folder to path
ROOT = Path(__file__).parent
sys.path.append(str(ROOT / "yolov5"))

import train as yolov5
import argparse


def train_(
    overwrite: bool = False,
    models_path: Path = ROOT / "models",
    datasets_path: Path = ROOT / "datasets",
):
    print(overwrite)
    if overwrite and models_path.exists():
        dir_util.remove_tree(models_path)
    models_path.mkdir(exist_ok=True)

    datasets = list(filter(lambda dataset: dataset.is_dir(), datasets_path.glob("*/")))

    for dataset in datasets:
        # Hyperparameter
        input_img_size = 640
        pretrained_weight = "yolov5s.pt"
        num_epochs = 5000
        batch_size = 32

        # Paths
        data_yaml_path = dataset / "data.yaml"
        models_path = models_path
        model_name = dataset.name

        # Early stopping parameters
        patience = 100

        # Other paremeters
        workers = 8
        save_period = -1
        device = 0

        # Train yolov5 with above parameters
        yolov5.run(
            imgsz=input_img_size,
            weights=models_path/pretrained_weight,
            epochs=num_epochs,
            batch_size=batch_size,
            data=data_yaml_path,
            project=models_path,
            name=model_name,
            patience=patience,
            exist_ok=True,
            workers=workers,
            save_period=save_period,
            device=device,
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
    train_(overwrite=opt.overwrite)
