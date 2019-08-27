from xml.dom import minidom
import numpy as np
from os import walk, makedirs
from os.path import join, expanduser
from speechcorpus.utils import read_wav, get_duration_sox
import shutil


def get_vad(xml_path, wav_path):
    total_duration = get_duration_sox(wav_path)
    data = minidom.parse(xml_path)
    tracks = data.getElementsByTagName("track")
    tracks = [t.attributes["id"].value for t in tracks]
    ch0, ch1 = [], []
    for seg in data.getElementsByTagName("segment"):
        start = float(seg.attributes["start"].value)
        end = float(seg.attributes["end"].value)
        if seg.attributes["track"].value == tracks[0]:
            ch0.append((start, end))
        else:
            ch1.append((start, end))
    vad0 = np.array(ch0, dtype=np.float32) / total_duration
    vad1 = np.array(ch1, dtype=np.float32) / total_duration
    return (vad0, vad1)


def save_all_vads(datapath, savepath):
    makedirs(savepath, exist_ok=True)
    for dirpath, dirnames, files in walk(datapath):
        if len(files) > 0:
            cont = True
            for f in files:
                if f.endswith(".wav"):
                    cont = False
            if cont:
                continue
            else:
                fpath = join(savepath, "_".join(dirpath.split("/")[-2:]))
                makedirs(fpath, exist_ok=True)
                filename = join(fpath, "vad.npy")
                wav_path = [
                    f
                    for f in files
                    if f.endswith(".wav") and not f.endswith("user.wav")
                ][0]
                wav_path = join(dirpath, wav_path)
                xml_path = [f for f in files if f.endswith(".xml")][0]
                xml_path = join(dirpath, xml_path)
                vad = get_vad(xml_path, wav_path)

                np.save(filename, vad, allow_pickle=True)


def move_wavs(datapath, savepath):
    makedirs(savepath, exist_ok=True)
    for dirpath, dirnames, files in walk(datapath):
        if len(files) > 0:
            cont = True
            for f in files:
                if f.endswith(".wav"):
                    cont = False
            if cont:
                continue
            else:
                name = "_".join(dirpath.split("/")[-2:]) + ".wav"
                to_path = join(savepath, name)
                wav_path = [
                    f
                    for f in files
                    if f.endswith(".wav") and not f.endswith("user.wav")
                ][0]
                from_path = join(dirpath, wav_path)

                shutil.move(from_path, to_path)


if __name__ == "__main__":

    ans = input("Process Train? (y/n)")
    if ans.lower() == "y":
        print("Processing training_set")
        path = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set")
        savepath = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set/vad")
        save_all_vads(path, savepath)

        ans = input("Move wavs? (y/n)")
        if ans.lower() == "y":
            savepath = join(
                expanduser("~"), "SpeechCorpus/Robot/data/training_set/audio"
            )
            move_wavs(path, savepath)

    # saves vad
    ans = input("Process eval? (y/n)")
    if ans.lower() == "y":
        print("Processing user_evaluation_set")
        path = join(expanduser("~"), "SpeechCorpus/Robot/data/user_evaluation_set")
        savepath = join(
            expanduser("~"), "SpeechCorpus/Robot/data/user_evaluation_set/vad"
        )
        save_all_vads(path, savepath)

        # moves wavs (not
        savepath = join(
            expanduser("~"), "SpeechCorpus/Robot/data/user_evaluation_set/audio"
        )
        move_wavs(path, savepath)
