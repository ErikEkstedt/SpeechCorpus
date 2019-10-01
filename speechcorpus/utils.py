from subprocess import check_output, call, DEVNULL
from scipy.io.wavfile import read
import json
import csv
import numpy as np


def read_wav(path, norm=False):
    sr, y = read(path)
    y = y.astype(np.float32)
    y /= 2 ** 15
    y = y.astype(np.float32)
    if norm:
        y /= np.abs(y).max()
    return y, sr


def read_csv(path, delimiter=","):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)
    return data


def list_percentage_to_onehot(vad, frames):
    """ converts a list of length Channels to a onehot array of shape (Channels, frames)"""
    assert isinstance(vad, list)
    onehot = np.zeros((len(vad), frames))
    for i, ch in enumerate(vad):
        ch = (ch * frames).round().astype(np.int)
        for s, e in ch:
            onehot[i, s:e] = 1
    return onehot


def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        data = json.loads(f.read())
    return data


def print_dict(d, indent=2):
    if not isinstance(d, dict):
        print(f"Can't print {type(d)}. Requires dict")
        return None
    print(json.dumps(d, indent=indent))


def write_json(data, filename):
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)


def read_txt(filename):
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            data.append(line.strip())
    return data


def write_txt(filename, data):
    """
    Argument:
        txt:    list of strings
        name:   filename
    """
    with open(filename, "w") as f:
        f.write("\n".join(data))


# Audio


def resample_wav2sph(audiopath, to_path, channels=2):
    """ Resample from .wav ->  .sph and mu-law encoding using sox """
    # ffmpeg_cmd = ["ffmpeg", "-i", audiopath, "-acodec", "pcm_mulaw", "-ar", str(8000), to_path]
    cmd = [
        "sox",
        audiopath,
        "-e",
        "mu-law",
        "-r",
        str(8000),
        "-c",
        str(channels),
        to_path,
    ]
    call(cmd, stdout=DEVNULL)


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


def get_sample_rate_sox(fpath):
    out = (
        check_output(f"sox --i {fpath}", shell=True).decode("utf-8").strip().split("\n")
    )
    for line in out:
        if line.lower().startswith("sample rate"):
            l = [f for f in line.split(" ") if not f == ""]
            return int(l[-1])
