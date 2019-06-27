#!/usr/bin/env python
from os.path import join
from os import listdir, makedirs, system
from tqdm import tqdm
import shutil
import sys


# TODO
def download_audio(audio_path, url=None):
    if url is None:
        url = "http://datashare.is.ed.ac.uk/download/DS_10283_2651.zip"

    # Not done anything with this yet
    wget_cmd = [
        "wget",
        "-P",
        audio_path,
        "-r",
        "-np",
        "-R",
        "index.html*",
        "-nd",
        url,
        "-q",
        "--show-progress",
    ]
    system(" ".join(wget_cmd))

    for f in listdir(audio_path):
        fpath = join(audio_path, f)
        if not f.endswith(".wav"):
            system(f"rm {fpath}")
