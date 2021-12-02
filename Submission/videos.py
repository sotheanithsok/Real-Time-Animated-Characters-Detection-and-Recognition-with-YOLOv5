import argparse
from distutils import dir_util
from pathlib import Path
from pytube import YouTube
import json

ROOT = Path(__file__).parent


def videos(
    overwrite: bool = False,
) -> None:
    """Download the train video and the test video from YouTube and save them to files.

    Args:
        overwrite (bool, optional): overwrite existing files. Defaults to False.
    """

    # Load settings.json
    with open(ROOT / "settings.json") as f:
        settings = json.load(f)

    # Create varaibles
    videos = ROOT / settings["videos"]
    urls = settings["vidoes_urls"]
    names = settings["vidoes_names"]

    # Remove all files in directory if overwrite is true
    if overwrite and videos.exists():
        dir_util.remove_tree(str(videos))

    # Create the directory if it doesn't exist
    videos.mkdir(exist_ok=True)

    # Download all vidoes
    for url, name in zip(urls, names):
        stream = YouTube(url).streams.get_highest_resolution()
        stream.download(videos, name)


def parse_opt(known: bool = False) -> argparse.Namespace:
    """Set up command line arguments

    Args:
        known (bool, optional): if arguments are known, throw an error if an unknown argument are passed in. Defaults to False.

    Returns:
        argparse.Namespace: parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--overwrite", action="store_true", help="overwrite the directory"
    )
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


# Run this code if this script is called from a command line
if __name__ == "__main__":
    opt = parse_opt()
    videos(overwrite=opt.overwrite)
