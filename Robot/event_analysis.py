from os.path import join, abspath
from os import listdir, makedirs
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from tqdm import tqdm

from turntaking.utils import get_home_path, get_duration_sox
from librosa import load
from librosa.output import write_wav

NLP_PATH = "data/training_set/nlp"
AUDIO_PATH = "data/training_set/audio"


def total_dirty_clean():
    # sessions = [join(NLP_PATH, f) for f in listdir(NLP_PATH)]
    session_names = listdir(NLP_PATH)
    dirty_holds, clean_holds = [], []
    dirty_shifts, clean_shifts = [], []
    for name in session_names:
        session = join(NLP_PATH, name)
        clean_holds.append((name, np.load(join(session, "holds_clean.npy"))))
        clean_shifts.append((name, np.load(join(session, "shifts_clean.npy"))))
        try:
            dirty_holds.append((name, np.load(join(session, "holds_dirty.npy"))))
        except:
            pass
        try:
            dirty_shifts.append((name, np.load(join(session, "shifts_dirty.npy"))))
        except:
            pass

    # get total
    n_dirty_shifts = 0
    n_dirty_holds = 0
    n_clean_shifts = 0
    n_clean_holds = 0

    for _, e in dirty_shifts:
        n_dirty_shifts += e.size
    for _, e in dirty_holds:
        n_dirty_holds += e.size
    for _, e in clean_shifts:
        n_clean_shifts += e.size
    for _, e in clean_holds:
        n_clean_holds += e.size

    n_holds = n_dirty_holds + n_clean_holds
    n_shifts = n_dirty_shifts + n_clean_shifts
    n_total = n_holds + n_shifts
    print(f"total holds: {n_holds} ({round(n_holds/n_total * 100, 1)}%)")
    print(f"total shifts: {n_shifts} ({round(n_shifts/n_total * 100, 1)}%)")
    print(f"dirty holds: {n_dirty_holds} ({round(n_dirty_holds/n_holds * 100, 1)}%)")
    print(
        f"dirty shifts: {n_dirty_shifts} ({round(n_dirty_shifts/n_shifts * 100, 1)}%)"
    )

    return {
        "clean": {"shifts": clean_shifts, "holds": clean_holds},
        "dirty": {"shifts": dirty_shifts, "holds": dirty_holds},
    }


def process_dirty_event(session, events, save_folder="data/dirty_shifts", debug=False):
    """
    All events in dirty needs to remove the robot voice for the event

    1. loop over all dirty events
    2. create new audio where interfering robot voice is muted (only requires up until event + some padding)
          - New waveform for robot channel. copy silence from same wav
    3. get new index for the new audio (percentage of duration)
    4. save the new audio to training_set/edited_audio.
    5. save the new event time with the same name (except .wav -> .npy)
    """

    makedirs(save_folder, exist_ok=True)

    wav_path = join(get_home_path(), "SpeechCorpus/Robot", AUDIO_PATH, session + ".wav")
    duration = get_duration_sox(wav_path)
    y, sr = load(wav_path, mono=False, sr=None)
    sr = int(sr)
    total_samples = y.shape[1]
    # total_samples = round(duration * sr)

    for i, event in enumerate(events):
        # print(event)
        ev_start = round(event * total_samples)
        seg_start = int(ev_start - sr * 3)
        seg_end = int(ev_start + sr * 3)
        rel_ev_start = int(sr * 3)

        y_new = y[:, :seg_end].copy()
        y_new[1, int(ev_start - sr) : int(ev_start + sr)] = 0

        y_new = np.asfortranarray(y_new)

        if debug:
            plt.close("all")
            fig = plt.figure(figsize=(10, 6))
            plt.subplot(311)
            plt.plot(y[0, seg_start:seg_end])
            plt.vlines(x=int(sr * 3), ymin=-1, ymax=1, color="r")
            plt.subplot(312)
            plt.plot(y[1, seg_start:seg_end])
            plt.vlines(x=rel_ev_start, ymin=-1, ymax=1, color="r")
            plt.subplot(313)
            plt.plot(y_new[1, seg_start:seg_end])
            plt.vlines(x=int(sr * 3), ymin=-1, ymax=1, color="r")
            plt.tight_layout()
            plt.pause(0.01)
            sd.play(y[:, seg_start:seg_end].T, samplerate=sr, blocking=True)

        # Save audio and event
        tmp_dir = join(save_folder, f"{session}_ev_{i}")
        makedirs(tmp_dir)

        wav_path = join(tmp_dir, "audio.wav")
        write_wav(wav_path, y_new, sr)

        new_event_percent = ev_start / y_new.shape[1]

        ev_path = join(tmp_dir, "event.npy")
        np.save(ev_path, new_event_percent)


def look_at_processed(folder):
    event = float(np.load(join(folder, "event.npy"), allow_pickle=True))
    y, sr = load(join(folder, "audio.wav"), mono=False, sr=None)
    frames = y.shape[1]
    ev = round(event * frames)

    start = frames - (sr * 10)
    rel_ev = ev - start

    plt.close("all")
    fig = plt.figure(figsize=(10, 6))
    plt.subplot(211)
    plt.plot(y[0, start:])
    plt.vlines(x=rel_ev, ymin=-1, ymax=1, color="r")
    plt.subplot(212)
    plt.plot(y[1, start:])
    plt.vlines(x=rel_ev, ymin=-1, ymax=1, color="r")
    plt.tight_layout()
    plt.pause(0.01)
    sd.play(y[:, start:].T, samplerate=sr, blocking=True)


if __name__ == "__main__":
    print("Analize Events")

    events_sorted = total_dirty_clean()
    print(events_sorted.keys())

    # All events in clean should be used per usual

    session, events = events_sorted["dirty"]["shifts"][0]

    print("Dirty Shifts")
    for session, events in tqdm(events_sorted["dirty"]["shifts"]):
        process_dirty_event(
            session, events, save_folder="data/training_set/dirty_shifts", debug=False
        )

    print("Dirty Holds")
    for session, events in tqdm(events_sorted["dirty"]["holds"]):
        process_dirty_event(
            session, events, save_folder="data/training_set/dirty_holds", debug=False
        )

    # folder = "/home/erik/SpeechCorpus/Robot/data/training_set/dirty_shifts/8_session_004_ev_1"
    # look_at_processed(folder)
