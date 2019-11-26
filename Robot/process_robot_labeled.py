"""
Starting with `training_set_11Nov2014.zip` and `setup.zip` process the data to appropriate format
We assume they are both located in SpechCorpus/Robot/data => $PWD/data
1. unzip files to desired destination
2. organize files appropriately
3. extract vad, duration and timed_words
"""
from os.path import join, basename, split, exists
from os import system, listdir, makedirs
from glob import glob
import sys
import shutil
import numpy as np
from tqdm import tqdm

from turntaking.utils import read_txt, read_wav, get_duration_sox


def remove_created_dirs():
    system("rm -rf data/train_data")
    system("rm -rf data/train_labeled_words")
    print("Removed files to data/{train_data, train_labeled_words}")


def unzip_files():
    data, labeled_data = "data/train_data", "data/train_labeled_words"
    if not (exists(data) and exists(labeled_data)):
        print("Unzipping files to data/{train_data, train_labeled_words}")
        system(f"unzip -d {data}/training_set_11Nov2014.zip")
        system(f"unzip -d {labeled_data}data/train_labeled_words data/setup.zip")
        print("Done!")
    else:
        print("Data paths already exists! Delete or use that data")
        sys.exit(1)


def get_wav_path(split_name):
    return join(
        "data/train_data/training_set",
        "/".join(split_name[1:-1] + [split_name[-2]]) + ".wav",
    )


def lab_to_timed_words(lab_path, duration):
    lab1 = read_txt(lab_path)
    lab2 = read_txt(lab_path.replace("track1", "track2"))

    tw, words, vad = [[], []], [[], []], [[], []]
    for i, labels in enumerate([lab1, lab2]):
        for row in labels:
            s, e, w = row.split()
            s = float(s) / duration
            e = float(e) / duration
            if w != "_":
                vad[i].append((s, e))
                tw[i].append((s, e, w))
                words[i].append(w)
    return vad, tw, words


def organize_audio_and_nlp_data_train_set():
    """
    Audio:
    splits:  SpeechCorpus/Robot/data/robot_labeled/training_set/audio/10_session_001.wav
    NLP:
    "SpeechCorpus/Robot/data/robot_labeled/training_set/nlp"
    """

    audio_path = "data/training_set/audio"
    nlp_path = "data/training_set/nlp"
    makedirs(audio_path, exist_ok=True)
    makedirs(nlp_path, exist_ok=True)

    label_path = "data/train_labeled_words"
    for lab_path in tqdm(glob(join(label_path, "*track1.lab"))):
        split_name = lab_path.split("__")
        wav_path = get_wav_path(split_name)

        # Extraction
        duration = get_duration_sox(wav_path)
        vad, timed_words, words = lab_to_timed_words(lab_path, duration)

        # Save paths
        name = f"{split_name[1]}_{split_name[-2]}"
        tmp_audio_path = join(audio_path, name + ".wav")
        tmp_nlp_path = join(nlp_path, name)

        makedirs(tmp_nlp_path, exist_ok=True)

        # Copy audio and save nlp data
        shutil.copy(wav_path, tmp_audio_path)
        np.save(join(tmp_nlp_path, "vad.npy"), vad, allow_pickle=True)
        np.save(join(tmp_nlp_path, "timed_words.npy"), timed_words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "words.npy"), words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "duration.npy"), duration, allow_pickle=True)


def organize_audio_and_nlp_data_eval():
    """
    Audio:
    splits:  SpeechCorpus/Robot/data/robot_labeled/training_set/audio/10_session_001.wav
    NLP:
    "SpeechCorpus/Robot/data/robot_labeled/training_set/nlp"
    """

    audio_path = "data/robot_labeled/training_set/audio"
    nlp_path = "data/robot_labeled/training_set/nlp"
    makedirs(audio_path, exist_ok=True)
    makedirs(nlp_path, exist_ok=True)

    label_path = "data/train_labeled_words"
    for lab_path in tqdm(glob(join(label_path, "*track1.lab"))):
        split_name = lab_path.split("__")
        wav_path = get_wav_path(split_name)

        # Extraction
        duration = get_duration_sox(wav_path)
        timed_words, words = lab_to_timed_words(lab_path, duration)

        # Save paths
        name = f"{split_name[1]}_{split_name[-2]}"
        tmp_audio_path = join(audio_path, name + ".wav")
        tmp_nlp_path = join(nlp_path, name)

        makedirs(tmp_nlp_path, exist_ok=True)

        # Copy audio and save nlp data
        shutil.copy(wav_path, tmp_audio_path)
        np.save(join(tmp_nlp_path, "timed_words.npy"), timed_words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "words.npy"), words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "duration.npy"), duration, allow_pickle=True)


if __name__ == "__main__":

    ans = input("Unzip files? (y/n)")
    if ans.lower() == "y":
        unzip_files()

    organize_audio_and_nlp_data_train_set()
