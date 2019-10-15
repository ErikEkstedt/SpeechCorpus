from collections import Counter
from glob import glob
import numpy as np
from os.path import join, expanduser
from tqdm import tqdm


def build_word_counter(path):
    """
    path:       path to vad extraction
    E.g Switchboard
    $path/(sw2001, sw2005, sw2006, ...)/(vad.npy, words.npy, silence.npy)
    """
    all_words = glob(join(path, "**/words.npy"))
    counter = Counter()
    for session_word_path in tqdm(all_words):
        ch_words = list(np.load(session_word_path, allow_pickle=True))
        for ch in ch_words:
            for word in ch:
                counter.update([word])
    if len(counter) == 0:
        print("Could not find any files. Wrong path? ", path)
    return counter


if __name__ == "__main__":

    speechcorpus_path = join(expanduser("~"), "SpeechCorpus")

    swb_counter = build_word_counter(join(speechcorpus_path, "switchboard/data/nlp"))
    mt_counter = build_word_counter(join(speechcorpus_path, "maptask/data/nlp"))

    total_counter = swb_counter + mt_counter

    print("swb: ", len(swb_counter))
    print("mt: ", len(mt_counter))
    print("total: ", len(total_counter))

    np.save("maptask_switchboard_counter.npy", total_counter)
