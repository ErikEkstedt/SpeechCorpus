from collections import Counter
from os.path import join
import numpy as np
import re
from tqdm import tqdm
from glob import glob
from multiprocessing import Pool


def clean(text):
    if isinstance(text, str):
        clean_word = re.sub("[^A-Za-z0-9]+", "", text)
    else:
        clean_words = []
        for w in text:
            clean_words.append(re.sub("[^A-Za-z0-9]+", "", w))
        clean_word = clean_words[-1]
    return [clean_word.lower()]


def get_words(path):
    counter = Counter()
    ch_words = list(np.load(path, allow_pickle=True))
    for ch in ch_words:
        for word in ch:
            counter.update(clean(word))
    return counter


def build_word_counter(path, files=None, serial=True):
    """
    path:       path to vad extraction

    E.g Switchboard
    $path/(sw2001, sw2005, sw2006, ...)/(vad.npy, words.npy, silence.npy)
    """

    all_words = glob(join(path, "**/words.npy"))
    if files is not None:
        subset = []
        for f in files:
            for w in all_words:
                if f in w:
                    subset.append(w)
        all_words = subset

    if serial:
        counter = Counter()
        for session_word_path in tqdm(all_words):
            ch_words = list(np.load(session_word_path, allow_pickle=True))
            for ch in ch_words:
                for word in ch:
                    counter.update(clean(word))
    else:
        with Pool() as pool:
            counters = list(
                tqdm(
                    pool.imap(get_words, all_words),
                    total=len(all_words),
                    desc="Loading words",
                    dynamic_ncols=True,
                )
            )
        counter = Counter()
        for c in tqdm(counters):
            counter.update(c)

    if len(counter) == 0:
        print("Could not find any files. Wrong path? ", path)
        return None
    return counter
