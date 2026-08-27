import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from users_groups_setup import run, group_exists, ensure_group

MEDIA_LIBRARIES = [
    "tv",
    "movies",
    "anime",
    "anime_movies",
    "cartoons",
    "cartoon_movies",
    "documentaries",
    "other_videos",
    "music",
    "books",
    "comics",
    "audiobooks",
    "podcasts",
    "audiobookshelf-metadata",
]

RECYCLE_FOLDERS = [
    "tv",
    "movies",
    "anime",
    "anime_movies",
    "cartoons",
    "documentaries",
    "other_videos",
    "music",
    "books",
    "comics",
]

REQUIRED_GROUPS = [
    ("media_read", 12999),
    ("media_write", 13000),
]


def _validate_groups():
    for groupname, gid in REQUIRED_GROUPS:
        ensure_group(groupname, gid)


def create_folders(root_dir_hdd):
    media_root = f"{root_dir_hdd.rstrip('/')}/data"

    _validate_groups()

    dirs = [
        f"{media_root}/media",
        f"{media_root}/usenet",
        f"{media_root}/torrents",
        f"{media_root}/usenet/incomplete",
        f"{media_root}/usenet/complete",
        f"{media_root}/torrents/incomplete",
        f"{media_root}/torrents/complete",
    ]

    dirs += [f"{media_root}/media/{folder}" for folder in MEDIA_LIBRARIES]
    dirs += [f"{media_root}/recycle/{folder}" for folder in RECYCLE_FOLDERS]

    for d in dirs:
        if not group_exists("media_write"):
            raise RuntimeError(
                "media_write group does not exist; run users_groups_setup.py first"
            )
        run(["sudo", "mkdir", "-pv", "-m", "775", d])

    run([
        "sudo", "chown",
        f"{os.getuid()}:media_write",
        media_root
    ])


if __name__ == "__main__":
    root_dir_hdd = os.environ.get("ROOT_DIR_HDD")

    if not root_dir_hdd:
        print("Where would you like to keep your hdd media/download files?", end=" ")
        root_dir_hdd = input().strip()

    create_folders(root_dir_hdd)
    print("Folder structure created successfully.")
