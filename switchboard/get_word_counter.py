from speechcorpus.word_counter import build_word_counter
import numpy as np

counter = build_word_counter(path="data/vad", serial=False)
np.save("data/word_counter.npy", counter, allow_pickle=True)
c = np.load("data/word_counter.npy", allow_pickle=True).item()
