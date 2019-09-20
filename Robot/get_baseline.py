from os.path import join, expanduser
import matplotlib.pyplot as plt
import numpy as np
from speechcorpus.utils import get_duration_sox
from turntaking.utils import get_onehot_vad
from turntaking.plot_utils import plot_vad


def load_labels(wname, time_step=0.05):
    root = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set")
    wav_path = join(root, "audio", wname + ".wav")
    v_path = join(root, "vad2", wname, "vad.npy")
    e_path = join(root, "vad2", wname, "events.npy")
    en_path = join(root, "vad2", wname, "events_named.npy")

    vad = np.load(v_path, allow_pickle=True)
    event = np.load(e_path, allow_pickle=True)
    event_named = np.load(en_path, allow_pickle=True).item()

    dur = get_duration_sox(wav_path)
    n_frames = round(dur / time_step)

    vad_oh = get_onehot_vad(vad, n_frames)
    shifts = (event_named["shifts"] * n_frames).round().astype(np.int)
    holds = (event_named["holds"] * n_frames).round().astype(np.int)

    return vad_oh, shifts, holds


def get_baseline(vad_oh, label, horizon_frames, tt="shifts"):
    correct = []
    wrong = []
    for s, e in zip(label, label + horizon_frames):
        user = vad_oh[0][s:e].nonzero()[0]
        robo = vad_oh[1][s:e].nonzero()[0]

        if len(user) > 0:
            user_min = user[0]
        else:
            user_min = horizon_frames + 1

        if len(robo) > 0:
            robo_min = robo[0]
        else:
            robo_min = horizon_frames + 1

        winner = np.argmin((user_min, robo_min))

        if tt == "shifts":
            if winner == 1:
                correct.append(s)
            else:
                wrong.append(s)
        else:
            if winner == 1:
                wrong.append(s)
            else:
                correct.append(s)
    return correct, wrong


def plot_baseline(vad_oh, shifts, holds, correct, wrong):
    fig = plt.figure()
    plot_vad(vad_oh)
    plt.vlines(
        holds,
        ymax=2,
        ymin=0,
        color="k",
        label="hold label",
        linewidth=2,
        linestyles="dashed",
    )
    plt.vlines(
        correct["holds"],
        ymin=-2,
        ymax=0,
        label="Correct holds",
        color="g",
        linewidth=2,
        linestyles="dashed",
    )
    plt.vlines(
        wrong["holds"],
        ymin=-2,
        ymax=0,
        label="Wrong holds",
        color="r",
        linewidth=2,
        linestyles="dashed",
    )
    plt.vlines(shifts, ymax=2, ymin=0, color="k", label="shift label", linewidth=2)
    plt.vlines(
        correct["shifts"],
        ymin=-2,
        ymax=0,
        label="Correct shifts",
        color="g",
        linewidth=2,
    )
    plt.vlines(
        wrong["shifts"], ymin=-2, ymax=0, label="Wrong shifts", color="r", linewidth=2
    )
    plt.tight_layout()
    plt.legend()
    plt.pause(0.001)
    return fig


# TODO
# Use edlund to get gaps, pauses, overlap_w, overlap_w
# Then fix error when robot started talking user overlap_w

if __name__ == "__main__":

    time_step = 0.05
    horizon_time = 1
    horizon_frames = round(horizon_time / time_step)
    wname = "1_session_002"
    vad_oh, shifts, holds = load_labels(wname, time_step)

    correct_shifts, wrong_shifts = get_baseline(
        vad_oh, label=shifts, horizon_frames=horizon_frames, tt="shifts"
    )
    correct_holds, wrong_holds = get_baseline(
        vad_oh, label=holds, horizon_frames=horizon_frames, tt="holds"
    )
    correct = {"shifts": correct_shifts, "holds": correct_holds}
    wrong = {"shifts": wrong_shifts, "holds": wrong_holds}

    plot_baseline(vad_oh, shifts, holds, correct, wrong)
