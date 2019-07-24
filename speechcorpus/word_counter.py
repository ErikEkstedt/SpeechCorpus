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
    return clean_word.lower()


def get_words(path):
    counter = Counter()
    ch_words = list(np.load(path, allow_pickle=True))
    for ch in ch_words:
        for word in ch:
            counter.update([clean(word["word"])])
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


# ------- POS ----------
def get_pos(path):
    counter = Counter()
    ch_pos = list(np.load(path, allow_pickle=True))
    for ch in ch_pos:
        for pos in ch:
            counter.update([pos["pos"]])
    return counter


def build_counter(all_paths, serial=True, type="pos"):
    """
    all_paths:       path to vad extraction

    E.g Switchboard
    $path/(sw2001, sw2005, sw2006, ...)/(vad.npy, words.npy, silence.npy)
    """
    if type.lower() == "pos":
        method = get_pos
    elif type.lower() == "words" or type.lower() == "word":
        method = get_words
    else:
        print('Type unknown. Please use "words" or "pos"')
        return None

    if serial:
        counter = Counter()
        for session_path in tqdm(all_paths):
            c = method(session_path)
            counter.update(c)
    else:
        with Pool() as pool:
            counters = list(
                tqdm(
                    pool.imap(method, all_paths),
                    total=len(all_paths),
                    desc="Loading",
                    dynamic_ncols=True,
                )
            )
        counter = Counter()
        for c in counters:
            counter.update(c)

    return counter


if __name__ == "__main__":
    from os.path import expanduser

    path = join(expanduser("~"), "SpeechCorpus/maptask/data/nlp")

    all_paths = glob(join(path, "**/pos.npy"))
    all_paths = glob(join(path, "**/words.npy"))
    c = build_counter(all_paths, type="word")
