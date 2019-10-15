from speechcorpus.word_counter import build_counter
from glob import glob
from os.path import join
import numpy as np
from collections import Counter
from tqdm import tqdm
from multiprocessing import Pool


def get_words(path):
    counter = Counter()
    ch_words = list(np.load(path, allow_pickle=True))
    for ch in ch_words:
        for word in ch:
            counter.update([word["word"]])
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
                    subset.append([w])
        all_words = subset

    if serial:
        counter = Counter()
        for session_word_path in tqdm(all_words):
            ch_words = list(np.load(session_word_path, allow_pickle=True))
            for ch in ch_words:
                for word in ch:
                    counter.update([word])
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


nlp_path = "data/nlp"

print("Creating POS vocab")
all_pos_paths = glob(join(nlp_path, "**/pos.npy"))
counter = build_counter(all_pos_paths, type="pos")

spath = "data/pos_counter.npy"
np.save(spath, counter, allow_pickle=True)
print("POS counter saved to -> ", spath)


all_word_paths = glob(join(nlp_path, "**/words.npy"))

counter = build_word_counter("data/nlp")

counter.most_common(1000)

spath = "data/word_counter.npy"
np.save(spath, counter, allow_pickle=True)
print("Word counter saved to -> ", spath)


# test
if True:
    spath = "data/pos_counter.npy"
    pos = np.load(spath, allow_pickle=True).item()
    print("POS: ", len(pos))
    print("Most common:")
    for p in pos.most_common(5):
        print(p)
    spath = "data/word_counter.npy"
    words = np.load(spath, allow_pickle=True).item()
    print("-" * 50)
    print("Words: ", len(words))
    print("Most common:")
    for p in words.most_common(5):
        print(p)


counter = np.load("data/word_counter.npy", allow_pickle=True).item()

counter.most_common(1000)
