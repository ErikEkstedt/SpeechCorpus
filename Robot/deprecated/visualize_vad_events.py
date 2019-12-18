import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import join, expanduser
from speechcorpus.utils import list_starts_ends_percentage_to_onehot
from glob import glob
import random


def visualize_vad(vad, color="b"):
    v0 = vad[0]
    # ax = plt.plot(v0, label="vad ch 0", color="b", alpha=0.5)
    plt.fill_between(
        np.arange(len(v0)), v0, where=v0 >= 0, interpolate=True, color=color, alpha=0.5
    )
    v1 = vad[1]
    plt.yticks([])
    # plt.plot(v1, label="vad ch 1", color="b", alpha=0.5)
    plt.fill_between(
        np.arange(len(v1)), -v1, where=v1 >= 0, interpolate=True, color=color, alpha=0.5
    )
    plt.yticks([])


def plot_event_vad(vad, shifts, holds, s=0, e=-1):
    if e is not -1 and e <= s:
        e = s + 200
    if not e == -1:
        holds = holds[holds <= e]
        holds = holds[holds >= s]
        holds -= s
        shifts = shifts[shifts <= e]
        shifts = shifts[shifts >= s]
        shifts -= s
    fig = plt.figure()
    visualize_vad(vad[:, s:e])
    plt.vlines(holds, ymin=-1, ymax=1, colors="k", label=f"Holds {len(holds)}")
    plt.vlines(shifts, ymin=-1, ymax=1, colors="r", label=f"Shifts {len(shifts)}")
    plt.legend()
    return fig


root = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set/vad_shift_holds")

paths = listdir(root)
files = random.choice(paths)
path = join(root, files)

vad = list(np.load(join(path, "vad.npy"), allow_pickle=True))
events = np.load(join(path, "events.npy"), allow_pickle=True)
frames = 5000
vad = list_starts_ends_percentage_to_onehot(vad, frames)

events[:, 0] = (events[:, 0] * frames).round()
events = events.astype(np.int)

shifts = (events["shifts"] * frames).round().astype(np.int)
holds = (events["holds"] * frames).round().astype(np.int)

s = round(frames * 0.1)
e = round(frames * 0.7)
plot_event_vad(vad, shifts, holds, s, e)
plt.tight_layout()


plt.close("all")
