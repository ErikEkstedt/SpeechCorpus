from xml.dom import minidom
import xml.dom as dom
import xml.etree.ElementTree as ET
import numpy as np
from os import walk, makedirs
from os.path import join, expanduser
from speechcorpus.utils import read_wav, get_duration_sox
import shutil


def get_vad(xml_path, wav_path):
    total_duration = get_duration_sox(wav_path)
    data = minidom.parse(xml_path)
    tracks = data.getElementsByTagName("track")
    tracks = [t.attributes["id"].value for t in tracks]
    ch0, ch1 = [], []
    for seg in data.getElementsByTagName("segment"):
        start = float(seg.attributes["start"].value)
        end = float(seg.attributes["end"].value)
        if seg.attributes["track"].value == tracks[0]:
            ch0.append((start, end))
        else:
            ch1.append((start, end))
    vad0 = np.array(ch0, dtype=np.float32) / total_duration
    vad1 = np.array(ch1, dtype=np.float32) / total_duration
    return (vad0, vad1)


def save_all_vads(datapath, savepath):
    makedirs(savepath, exist_ok=True)
    for dirpath, dirnames, files in walk(datapath):
        if len(files) > 0:
            cont = True
            for f in files:
                if f.endswith(".wav"):
                    cont = False
            if cont:
                continue
            else:
                fpath = join(savepath, "_".join(dirpath.split("/")[-2:]))
                makedirs(fpath, exist_ok=True)
                filename = join(fpath, "vad.npy")
                wav_path = [
                    f
                    for f in files
                    if f.endswith(".wav") and not f.endswith("user.wav")
                ][0]
                wav_path = join(dirpath, wav_path)
                xml_path = [f for f in files if f.endswith(".xml")][0]
                xml_path = join(dirpath, xml_path)
                vad = get_vad(xml_path, wav_path)
                np.save(filename, vad, allow_pickle=True)


def move_wavs(datapath, savepath):
    makedirs(savepath, exist_ok=True)
    for dirpath, dirnames, files in walk(datapath):
        if len(files) > 0:
            cont = True
            for f in files:
                if f.endswith(".wav"):
                    cont = False
            if cont:
                continue
            else:
                name = "_".join(dirpath.split("/")[-2:]) + ".wav"
                to_path = join(savepath, name)
                wav_path = [
                    f
                    for f in files
                    if f.endswith(".wav") and not f.endswith("user.wav")
                ][0]
                from_path = join(dirpath, wav_path)

                shutil.move(from_path, to_path)


def process_train():
    ans = input("Process Train? (y/n)")
    if ans.lower() == "y":
        print("Processing training_set")
        path = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set")
        ans = input("Extract vad? (y/n)")
        if ans.lower() == "y":
            savepath = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set/vad")
            save_all_vads(path, savepath)

        ans = input("Move wavs? (y/n)")
        if ans.lower() == "y":
            savepath = join(
                expanduser("~"), "SpeechCorpus/Robot/data/training_set/audio"
            )
            move_wavs(path, savepath)


def process_eval():
    # saves vad
    ans = input("Process eval? (y/n)")
    if ans.lower() == "y":
        print("Processing user_evaluation_set")
        path = join(expanduser("~"), "SpeechCorpus/Robot/data/user_evaluation_set")
        savepath = join(
            expanduser("~"), "SpeechCorpus/Robot/data/user_evaluation_set/vad"
        )
        save_all_vads(path, savepath)

        # moves wavs (not
        savepath = join(
            expanduser("~"), "SpeechCorpus/Robot/data/user_evaluation_set/audio"
        )
        move_wavs(path, savepath)


def get_vads_holds_shifts(xml_path, wav_path):
    """
    Gets VAD from annotation of starts and ends. The events are manually labeled as what should have happened.
    The event times are at the end of the user utterances.

    In turntaking repo events are automatically annotated from what actually happened in the audio.
    events are stored as list of tuples and transformed to numpy with the following structure:

        event = [(time, next_speaker, prev_speaker), ..., (time, next_speaker, prev_speaker)]

    shifts and holds are then calculated from those values.
    """
    data = minidom.parse(xml_path)
    total_duration = get_duration_sox(wav_path)

    tracks = data.getElementsByTagName("track")
    tracks = [t.attributes["id"].value for t in tracks]
    ch0, ch1 = [], []
    holds, shifts = [], []
    events = []
    prev_speaker = False
    for seg in data.getElementsByTagName("segment"):
        start = float(seg.attributes["start"].value)
        end = float(seg.attributes["end"].value)
        features = seg.getElementsByTagName("features")
        act, feedback, misc = None, None, None
        if len(features) == 1:
            for f in features[0].getElementsByTagName("feature"):
                name = f.getAttribute("name")
                if "feedback" == name:
                    feedback = f.firstChild.data

        if seg.attributes["track"].value == tracks[0]:
            ch0.append((start, end))
            if feedback is not None:
                if feedback == "hold":
                    holds.append(end)
                    next_speaker = prev_speaker
                elif feedback == "respond":
                    shifts.append(end)
                    next_speaker = not prev_speaker
                elif feedback == "optional":
                    next_speaker = 2.0
                events.append((end, float(next_speaker), float(prev_speaker)))
        else:
            ch1.append((start, end))

    events = np.array(events, dtype=np.float32)
    events[:, 0] /= total_duration
    vad0 = np.array(ch0, dtype=np.float32) / total_duration
    vad1 = np.array(ch1, dtype=np.float32) / total_duration
    return (vad0, vad1), events


def save_all_vads_holds_shifts(datapath, savepath):
    makedirs(savepath, exist_ok=True)
    for dirpath, dirnames, files in walk(datapath):
        if len(files) > 0:
            cont = True
            for f in files:
                if f.endswith(".wav"):
                    cont = False
            if cont:
                continue
            else:
                fpath = join(savepath, "_".join(dirpath.split("/")[-2:]))
                makedirs(fpath, exist_ok=True)
                vad_path = join(fpath, "vad.npy")
                hold_shift_path = join(fpath, "events.npy")
                wav_path = [
                    f
                    for f in files
                    if f.endswith(".wav") and not f.endswith("user.wav")
                ][0]
                wav_path = join(dirpath, wav_path)
                xml_path = [f for f in files if f.endswith(".xml")][0]
                xml_path = join(dirpath, xml_path)
                vad, events = get_vads_holds_shifts(xml_path, wav_path)
                np.save(vad_path, vad, allow_pickle=True)
                np.save(hold_shift_path, events, allow_pickle=True)


if __name__ == "__main__":

    print("Processing training_set")
    path = join(expanduser("~"), "SpeechCorpus/Robot/data/training_set")
    ans = input("Extract vad? (y/n)")
    if ans.lower() == "y":
        savepath = join(
            expanduser("~"), "SpeechCorpus/Robot/data/training_set/vad_shift_holds"
        )
        save_all_vads_holds_shifts(path, savepath)
