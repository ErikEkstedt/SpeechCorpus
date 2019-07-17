from collections import Counter
from os import listdir
from os.path import join, expanduser, isdir, abspath
from tqdm import tqdm
import numpy as np
import re
import time


"""
Combine vad and word arrays to get timed words.

This should then be used in training together with (PreTrained) embeddings handled by
the dataprocessing
"""


def clean(text):
    clean_word = []
    for w in text:
        clean_word.append(re.sub("[^A-Za-z0-9]+", "", w))

    if len(clean_word) == 1:
        clean_word = clean_word[0]
    return clean_word


# after words.npy, vad.npy has been saved
def extract_timed_words_and_vocab(path, save=True, verbose=False):
    dirs = [f for f in listdir(path) if isdir(join(path, f))]
    print(len(dirs))
    vocab = set()
    t_start = time.time()
    for sample in tqdm(dirs):
        word_path = join(path, sample, "words.npy")
        vad_path = join(path, sample, "vad.npy")
        words = list(np.load(word_path, allow_pickle=True))
        vad = np.load(vad_path, allow_pickle=True)

        # Add words to vocab
        all_words = set([item for sublist in words for item in sublist])
        for w in all_words:
            vocab.add(w)

        unique_words = set(words[0])

        timed_words = [[], []]
        for channel in [0, 1]:
            assert vad[channel].shape[0] == len(words[channel])
            for t, word in zip(vad[channel], words[channel]):
                if verbose:
                    print(f"{t}: {word}")
                timed_words[channel].append((t[0], t[1], clean(word)))

        if save:
            save_path = join(path, sample, "time_words.npy")
            np.save(save_path, timed_words, allow_pickle=True)
    if save:
        save_path = join(path, "Vocab.npy")
        np.save(save_path, vocab, allow_pickle=True)
    t_dur = time.time() - t_start
    print(f"Found {len(vocab)} total words in {t_dur} seconds")


path = abspath("maptask/data/vad")
extract_timed_words_and_vocab(path, save=True, verbose=False)
