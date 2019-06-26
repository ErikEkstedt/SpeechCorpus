from os.path import join, abspath, exists
from os import makedirs, listdir
from utils import get_duration_sox, read_txt
from glob import glob
from tqdm import tqdm
import numpy as np


"""
Extract vad, words, noise, silence from treebank transcription.

Saves to e.g :

    'data/vad/sw02954/(vad, words, silence, noise).npy


Missing annotations ?

"""


def extract_data(transcript_path, duration):
    transcript = read_txt(transcript_path)

    silence = []
    noise = []
    vad = []
    words = []
    for line in transcript:
        l = line.split("\t")
        start = float(l[2])
        end = float(l[3])
        utt = l[4], l[5]
        if "[silence]" in utt:
            silence.append((start, end))
        elif "[noise]" in utt:
            noise.append((start, end))
        else:
            words.append(utt)
            vad.append((start, end))

    vad = np.array(vad).astype(np.float32) / duration
    silence = np.array(silence).astype(np.float32) / duration
    noise = np.array(noise).astype(np.float32) / duration

    return vad, words, silence, noise


def save_switchboard_vad_treebank(audio_path, anno_path, save_path):
    makedirs(save_path, exist_ok=True)

    # Get all annotation files
    anno_paths = glob(join(anno_path, "**/*.text"))
    anno_paths.sort()

    skip = []
    wav_files = [f for f in listdir(audio_path) if f.endswith(".wav")]
    for wav in tqdm(wav_files):
        name = wav.strip(".wav").replace("sw0", "sw")
        anno = [f for f in anno_paths if name in f]
        anno.sort()

        # Missing annotations ?
        if len(anno) == 0:
            skip.append(wav)
            continue

        # Paths
        session_path = join(save_path, wav.strip(".wav"))
        makedirs(session_path, exist_ok=True)
        word_path = join(session_path, "words.npy")
        vad_path = join(session_path, "vad.npy")
        noise_path = join(session_path, "noise.npy")
        silence_path = join(session_path, "silence.npy")

        # check if all features already exists
        if (
            exists(word_path)
            and exists(vad_path)
            and exists(silence_path)
            and exists(noise_path)
        ):
            continue

        wpath = join(audio_path, wav)
        duration = get_duration_sox(wpath)

        vad0, words0, silence0, noise0 = extract_data(anno[0], duration)
        vad1, words1, silence1, noise1 = extract_data(anno[1], duration)

        np.save(word_path, (words0, words1), allow_pickle=True)
        np.save(vad_path, (vad0, vad1), allow_pickle=True)
        np.save(noise_path, (noise0, noise1), allow_pickle=True)
        np.save(silence_path, (silence0, silence1), allow_pickle=True)

    print(f"Skipped {len(skip)}/{len(wav_files)} files")


if __name__ == "__main__":

    audio_path = "data/audio"
    anno_path = "data/data/alignments"
    save_path = "data/vad"

    save_switchboard_vad_treebank(audio_path, anno_path, save_path)
