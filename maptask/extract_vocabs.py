from speechcorpus.word_counter import build_counter
from glob import glob
from os.path import join
import numpy as np


nlp_path = "data/nlp"

print("Creating POS vocab")
all_pos_paths = glob(join(nlp_path, "**/pos.npy"))
counter = build_counter(all_pos_paths, type="pos")

spath = "data/pos_counter.npy"
np.save(spath, counter, allow_pickle=True)
print("POS counter saved to -> ", spath)


print("\nCreating POS vocab")
all_word_paths = glob(join(nlp_path, "**/words.npy"))
counter = build_counter(all_word_paths, type="word")

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
