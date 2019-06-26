#!/usr/bin/env python
from os.path import join
from os import listdir, makedirs, system
from tqdm import tqdm
import shutil
import sys

# URLS
DIALOG_URL = "http://groups.inf.ed.ac.uk/maptask/signals/dialogues"
ANNO_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"


def download_annotation(savepath, url=None):
    if url is None:
        url = ANNO_URL

    wget_cmd = ["wget", "-P", savepath, url, "-q", "--show-progress"]
    print("Downloading annotations")
    print("-----------------------")
    system(" ".join(wget_cmd))
    print("Download complete")

    print(f"Extracted annotations -> {savepath}/annotations")
    unzip_cmd = [
        "unzip",
        "-qq",
        join(savepath, "hcrcmaptask.nxtformatv2-1.zip"),
        "-d",
        savepath,
    ]
    system(" ".join(unzip_cmd))
    system(
        f'mv {join(savepath, "maptaskv2-1")} {join(savepath, "maptask_annotations")}'
    )
    system(f'rm {join(savepath, "hcrcmaptask.nxtformatv2-1.zip")}')


def download_audio(audio_path, url=None):
    if url is None:
        url = DIALOG_URL

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

    # print("Removing: 6ec2.mix.wav for it is corrupt...")
    # system(f'rm {join(audio_path, "q6ec2.mix.wav")}')


def resample(audio_path, sr=16000, bitrate=16, remove=True):
    for filename in tqdm(listdir(audio_path)):
        if filename.endswith(".wav"):
            fpath = join(audio_path, filename)
            to_path = join(audio_path, filename.replace(".mix", ""))
            if fpath == to_path:
                to_path = to_path.replace(".wav", "_resampled.wav")
            cmd = ["sox", fpath, "-b", str(bitrate), "-r", str(sr), to_path]
            system(" ".join(cmd))
            if remove:
                system(f"rm {fpath}")


def ffmpeg_split(filename, split_path, session):
    cmd = ["ffmpeg", "-loglevel", "panic", "-i"]
    cmd += [filename]
    cmd += ["-map_channel", "0.0.0"]
    cmd += [join(split_path, f"{session}_g.wav")]
    cmd += ["-map_channel", "0.0.1"]
    cmd += [join(split_path, f"{session}_f.wav")]
    system(" ".join(cmd))


def sox_split(filename, split_path, session, sr=16000):
    cmd = [
        "sox",
        filename,
        "-r",
        str(sr),
        "-c",
        "1",
        join(split_path, f"{session}_g.wav"),
        "remix",
        str(1),
    ]
    system(" ".join(cmd))
    cmd = [
        "sox",
        filename,
        "-r",
        str(sr),
        "-c",
        "1",
        join(split_path, f"{session}_f.wav"),
        "remix",
        str(2),
    ]
    system(" ".join(cmd))


def split_channels(audio_path, split_path):
    try:
        makedirs(split_path)
    except:
        print("Split path already exists. Done with this step?")

    print("Splitting audio")
    print("---------------")

    for file in listdir(audio_path):
        if file.endswith(".wav"):
            session = file.split(".")[0]
            # ffmpeg_split(join(audio_path, file), split_path, session)
            sox_split(join(audio_path, file), split_path, session)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Maptask")
    parser.add_argument("--savepath", default="data")
    parser.add_argument("--samplerate", default=16000)
    parser.add_argument("--bitrate", default=16)
    args = parser.parse_args()

    print("Download annotations? (y/n)")
    ans = input()
    if ans.lower() == "y":
        download_annotation(args.savepath)

    audio_path = join(args.savepath, "audio")
    print("Download audio? (y/n)")
    ans = input()
    if ans.lower() == "y":
        download_audio(audio_path)

    print("Resample audio? (y/n)")
    ans = input()
    if ans.lower() == "y":
        remove = True
        print("Keep original files? (y/n)")
        ans = input()
        if ans.lower() == "y":
            remove = False
        resample(audio_path, sr=args.samplerate, bitrate=args.bitrate, remove=remove)

    split_path = join(args.savepath, "audio_mono")
    print("Stereo -> Mono? (y/n)")
    ans = input()
    if ans.lower() == "y":
        split_channels(audio_path, split_path)
