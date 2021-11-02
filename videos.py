import argparse
from distutils import dir_util
from pathlib import Path
from pytube import YouTube

ROOT = Path(__file__).parent


def videos(
    overwrite: bool = False,
    urls: list[str] = ["https://youtu.be/rilFfbm7j8k", "https://youtu.be/cqyziA30whE"],
    filenames: list[str] = ["train.mp4", "test.mp4"],
    videos_path: Path = ROOT / "videos",
) -> None:

    # Remove all files in directory if overwrite is true
    if overwrite and videos_path.exists():
        dir_util.remove_tree(str(videos_path))

    # Create the directory if it doesn't exist
    videos_path.mkdir(exist_ok=True)

    # Download all vidoes
    for url, filename in zip(urls, filenames):
        stream = YouTube(url).streams.get_highest_resolution()
        stream.download(videos_path, filename)


def parse_opt(known: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    videos(overwrite=opt.overwrite)
