from os.path import join, expanduser
from os import listdir
from glob import glob
from speechcorpus.utils import read_txt
import numpy as np

path = "data/swb_ms98_transcriptions"

listdir(join(path, "32", "3246"))

# Get all trans files
search = "*trans.text"
files = glob(join(path, "**/**", search))
files.sort()


for A, B in zip(files[:-1], files[1:]):
    assert A[:6] == B[:6]
    f = read_txt(A)
    # Read lines in A
    for line in f:
        s = line.split()
        start = s[1]
        end = s[2]
        txt = " ".join(s[3:])
        print(f"{start}-{end}")
        print(txt)
        input()

words = A.replace("trans.text", "word.text")
w = read_txt(words)

wpath = "/Users/erik/SpeechCorpus/switchboard/data/vad/sw2001/words.npy"

words = list(np.load(wpath, allow_pickle=True))

# Construction 1
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English

nlp = English()
# Create a blank Tokenizer with just the English vocab
tokenizer = Tokenizer(nlp.vocab)

tok = tokenizer(" ".join(w[0]))
tokenizer(w[0])

for w in words[0]:
    t = tokenizer(w)
    if t.text != w:
        print(f"{w} -> {t}")
        input()
