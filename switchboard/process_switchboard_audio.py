from os import system, makedirs, listdir
from os.path import join, expanduser, exists, abspath, basename
from glob import glob
from tqdm import tqdm
import shutil
import random


def resample_audio(audio_path, savepath=None, sr=16000, bitrate=16):
    files = glob(join(abspath(audio_path), "**/*.sph"), recursive=True)
    if not len(files) > 0:
        print("No .sph files found. Do you have the audio in ./data?")
        return None
    print(f"found {len(files)} .sph files")
    print(f"Resample .sph files -> sr: {sr}, bitrate: {bitrate}? (y/n)")
    ans = input()
    if ans.lower() == "y":
        if savepath is not None:
            makedirs(savepath)
        for fpath in tqdm(files):
            if savepath is None:
                fpath_wav = join(
                    audio_path, fpath.replace(".sph", ".wav").replace("sw0", "sw")
                )
            else:
                fpath_wav = join(
                    savepath,
                    basename(fpath).replace(".sph", ".wav").replace("sw0", "sw"),
                )
            cmd = ["sox", fpath, "-r", str(sr), "-b", str(bitrate), fpath_wav]
            system(" ".join(cmd))

    print("Done!")
    print("Remove .sph files? (y/n)")
    ans = input()
    if ans.lower() == "y":
        for fpath in files:
            system(f"rm {fpath}")


def split_data(audio_path, out_path, n_test_files=438):
    wavs = [f for f in listdir(audio_path) if f.endswith(".wav")]
    makedirs(out_path, exists_ok=True)
    random.shuffle(wavs)

    print("Moving {n_test_files} to {out_path}")
    for w in wavs[:n_test_files]:
        src = join(audio_path, w)
        dst = join(out_path, w)
        shutil.move(src, dst)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process Switchboard Audio")
    parser.add_argument("--audio_path", default="data")
    parser.add_argument("--out_path", default="data/audio")
    args = parser.parse_args()

    resample_audio(args.audio_path, args.out_path)

    ans = input("Split audio data into audio/audio_test? (y/n)")
    if ans.lower() == "y":
        split_data("data/audio", "data/audio_test")
