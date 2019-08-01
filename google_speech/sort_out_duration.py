from subprocess import check_output
from os.path import join, expanduser
from os import makedirs
import numpy as np
from glob import glob
from tqdm import tqdm
import shutil
from multiprocessing import Pool
from speechcorpus.utils import read_txt


def get_duration_sox(fpath):
    out = (
        check_output(f"sox --i {fpath}", shell=True).decode("utf-8").strip().split("\n")
    )
    for line in out:
        if line.lower().startswith("duration"):
            l = [f for f in line.split(" ") if not f == ""]
            duration = l[2].split(":")
            hh, mm, ss = duration
            total = int(hh) * 60 * 60 + int(mm) * 60 + float(ss)
    return total


def not_one(path):
    not_1_second = []
    dur = get_duration_sox(path)
    if dur != 1.0:
        return path


path = "/Users/erik/SpeechCorpus/google_speech/train/audio"
wav_files = glob(join(path, "**/*.wav"))

with Pool() as pool:
    not_1 = list(
        tqdm(
            pool.imap(not_one, wav_files),
            total=len(wav_files),
            desc="Process",
            dynamic_ncols=True,
        )
    )

not_1 = [f for f in not_1 if f is not None]


npaths = read_txt("data/not_1_second_files.txt")

not_1_dir = "data/train_not_one_second"
makedirs(not_1_dir, exist_ok=True)

for f in npaths:
    old_path = join(expanduser("~"), f)
    name = f.split("/")[-2:]
    makedirs(join(not_1_dir, name[0]), exist_ok=True)
    new_path = join(not_1_dir, name[0], name[1])
    shutil.move(old_path, new_path)

path = "/Users/erik/SpeechCorpus/google_speech/data/train/audio"
wav_files = glob(join(path, "**/*.wav"))

print("total: ", len(wav_files))
