from os.path import join, expanduser, basename
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
from speechcorpus.utils import get_duration_sox
from turntaking.utils import get_onehot_vad
from turntaking.plot_utils import plot_vad


def load_labels(wname, time_step=0.05):
    root = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set")
    wav_path = join(root, "audio", wname + ".wav")
    v_path = join(root, "vad", wname, "vad.npy")
    e_path = join(root, "vad", wname, "events.npy")
    en_path = join(root, "vad", wname, "events_named.npy")

    vad = np.load(v_path, allow_pickle=True)
    event = np.load(e_path, allow_pickle=True)
    event_named = np.load(en_path, allow_pickle=True).item()

    dur = get_duration_sox(wav_path)
    n_frames = int(dur / time_step)

    vad_oh = get_onehot_vad(vad, n_frames)
    shifts = (event_named["shifts"] * n_frames).astype(np.int)
    holds = (event_named["holds"] * n_frames).astype(np.int)

    return vad_oh, shifts, holds


def get_baseline(vad_oh, label, horizon_frames, tt="shifts"):
    correct = []
    wrong = []
    for s, e in zip(label, label + horizon_frames):
        user = vad_oh[0][s:e].nonzero()[0]
        robo = vad_oh[1][s:e].nonzero()[0]

        if tt == "shifts":
            if len(user) > 0:
                user_min = user[0]
            else:
                user_min = horizon_frames + 1

            if len(robo) > 0:
                robo_min = robo[0]
            else:
                robo_min = horizon_frames + 1

                winner = np.argmin((user_min, robo_min))

            if winner == 1:
                correct.append(s)
            else:
                wrong.append(s)
        else:
            if len(robo) > 0:
                wrong.append(s)
            else:
                correct.append(s)
    return correct, wrong


def plot_baseline(vad_oh, shifts, holds, correct, wrong):
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


# TODO
# Use edlund to get gaps, pauses, overlap_w, overlap_w
# Then fix error when robot started talking user overlap_w

if __name__ == "__main__":
    from turntaking.utils import read_json, read_txt, get_home_path, load_numpy
    from turntaking.dataset.dataset import load_vad, ExtractFeaturesDataset
    from turntaking.plot_utils import plot_vad

    hparams = {
        "data": read_json("hparams/data/robot.json"),
        "features": read_json("hparams/features/features.json"),
    }

    hparams["features"]["feature_types"] = ["vad"]
    files = read_txt(hparams["data"]["train_files"])
    dset = ExtractFeaturesDataset(hparams, files, cache=False)

    d = dset["1_session_001"]
    f = dset.files[0]
    d = dset[f]

    wav_path = "/home/erik/SpeechCorpus/Robot/data/training_set/audio/1_session_001.wav"
    event_named_path = "/home/erik/SpeechCorpus/Robot/data/training_set/vad/1_session_001/events_named.npy"
    named = load_numpy(event_named_path).item()
    vad_path = (
        "/home/erik/SpeechCorpus/Robot/data/training_set/vad/1_session_001/vad.npy"
    )
    vad_idx = list(load_numpy(vad_path))

    dur = get_duration_sox(wav_path)

    n_frames = round(dur / hparams["features"]["time_step"])

    vad = np.zeros((2, n_frames))
    vad_idx[0] = (vad_idx[0] * n_frames).round()
    vad_idx[1] = (vad_idx[1] * n_frames).round()

    for i in range(2):
        for s, e in vad_idx[i]:
            vad[i, int(s) : int(e)] = 1

    events = {}
    for k, v in named.items():
        events[k] = np.zeros(n_frames)
        for i in (v * n_frames).round():
            events[k][int(i)] = 1

    plot_vad(vad)
    plt.plot(events["shifts"], color="g", label="shifts")
    plt.plot(events["holds"], color="r", label="holds")
    plt.plot(events["optional"], color="k", label="optional")
    plt.legend()
    plt.show()

    full_files = [join(get_home_path(), f) for f in files]
    wav_path = full_files[0]
    vad = load_vad(wav_path, hparams)

    if frames is None:
        dur = get_duration_sox(wav_path)
        frames = round(dur / hparams["features"]["time_step"])

    return get_onehot_vad(vad, frames)

    for wname in wnames:
        print(wname)
        vad_oh, shifts, holds = load_labels(wname, time_step)
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
        plt.show()

    correct_shifts, wrong_shifts = get_baseline(
        vad_oh, label=shifts, horizon_frames=horizon_frames, tt="shifts"
    )
    correct_holds, wrong_holds = get_baseline(
        vad_oh, label=holds, horizon_frames=horizon_frames, tt="holds"
    )
    correct = {"shifts": correct_shifts, "holds": correct_holds}
    wrong = {"shifts": wrong_shifts, "holds": wrong_holds}

    plot_baseline(vad_oh, shifts, holds, correct, wrong)

    for wname in wnames:

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
        input()
        plt.clf()
