import argparse
import cv2
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent


def extract(
    n_frames: int = 1000,
    overwrite: bool = False,
    train_video_path: Path = ROOT / "videos/train.mp4",
    frames_path: Path = ROOT / "frames",
) -> None:

    # Remove all files in the directory if overwrite is true
    # Note: from distutils.dir_util import remove_tree cause directory creation problem due to race condition.
    if overwrite and frames_path.exists():
        for f in frames_path.glob("*.png"):
            f.unlink()

    # Create the directory if it doesn't exist
    frames_path.mkdir(exist_ok=True)

    # Create video capture object
    cap = cv2.VideoCapture(str(train_video_path))

    # Find the number of frames in the video
    nums_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Find all frames that have been extracted already
    existed_frames = [int(f.stem) for f in frames_path.glob("*.png")]

    # Find all frames that haven't been extracted yet
    new_frames = [i for i in range(nums_frame) if i not in existed_frames]

    # Randomly pick frames
    picked_frames = np.random.choice(
        new_frames, n_frames - len(existed_frames), replace=False
    )

    # Write frames to the directory
    for frame in picked_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        _, frame_val = cap.read()
        cv2.imwrite(str(frames_path / f"{frame}.png"), frame_val)


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n_frames", "-n", default=1000, type=int, help="number of frames to extact"
    )
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    extract(n_frames=opt.n_frames, overwrite=opt.overwrite)
