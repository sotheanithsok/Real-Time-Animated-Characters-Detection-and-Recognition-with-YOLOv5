from os import mkdir
from pathlib import Path
import argparse
import json
from distutils import dir_util
import sys

import shutil

ROOT = Path(__file__).parent


def detect(overwrite: bool = False):

    # Load settings.json
    with open(ROOT / "settings.json", "r") as f:
        settings = json.load(f)

    # Create variables
    videos = ROOT / settings["videos"]
    models = ROOT / settings["models"]
    detect = ROOT / settings["detect"]
    yolov5 = ROOT / settings["yolov5"]
    images_size = settings["datasets_images_size"][settings["datasets_select"]]

    # Add yolov5 to path and import it
    sys.path.append(str(yolov5))
    import _yolov5 as yolov5

    # Remove all files in directory if overwrite is true
    if overwrite and detect.exists():
        dir_util.remove_tree(str(detect))
    detect.mkdir(exist_ok=True)

    # Get all vidoes and models
    videos = list(videos.glob("*"))
    models = list(filter(lambda model: model.is_dir(), models.glob("*")))

    # Pairs every vidoes with every models
    videos_and_models = [(video, model) for video in videos for model in models]

    for video, model in videos_and_models:

        # Copy video from _video into a temporary folder and rename it to video_model_extension
        (detect / "temp").mkdir(exist_ok=True)
        shutil.copy2(video, detect / f"temp/{video.stem}_{model.name}{video.suffix}")
        video = detect / f"temp/{video.stem}_{model.name}{video.suffix}"

        # Detect bounding boxes and confidences in the video
        yolov5.detect(
            weights=model / "train/weights/best.pt",
            source=video,
            imgsz=[images_size, images_size],
            device=0,
            project=detect.parent,
            name=detect.name,
            exist_ok=True,
        )

    # Remove the temporary folder
    dir_util.remove_tree(str(detect / "temp"))


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    detect(overwrite=opt.overwrite)
