"""
Starting with `training_set_11Nov2014.zip` and `setup.zip` process the data to appropriate format
We assume they are both located in SpechCorpus/Robot/data => $PWD/data
1. unzip files to desired destination
2. organize files appropriately
3. extract vad, duration and timed_words
"""
from os.path import join, basename, split, exists
from os import system, listdir, makedirs
from glob import glob
import sys
import shutil
import numpy as np
from tqdm import tqdm
from xml.dom import minidom

from turntaking.utils import read_txt, read_wav, get_duration_sox


def remove_created_dirs():
    system("rm -rf data/train_data")
    system("rm -rf data/train_labeled_words")
    print("Removed files to data/{train_data, train_labeled_words}")


def unzip_files():
    data, labeled_data = "data/train_data", "data/train_labeled_words"
    if not (exists(data) and exists(labeled_data)):
        print("Unzipping files to data/{train_data, train_labeled_words}")
        audio_extraction = f"unzip -d {data} data/training_set_11Nov2014.zip"
        label_extraction = f"unzip -d {labeled_data} data/setup.zip"
        print("AUDIO: ", audio_extraction)
        print("LABEL: ", label_extraction)
        system(audio_extraction)
        system(label_extraction)
        print("Done!")
    else:
        print("Data paths already exists! Delete or use that data")
        sys.exit(1)


def get_wav_path(split_name):
    return join(
        "data/train_data/training_set",
        "/".join(split_name[1:-1] + [split_name[-2]]) + ".wav",
    )


def lab_to_timed_words(lab_path, duration):
    lab1 = read_txt(lab_path)
    lab2 = read_txt(lab_path.replace("track1", "track2"))

    tw, words, vad = [[], []], [[], []], [[], []]
    for i, labels in enumerate([lab1, lab2]):
        for row in labels:
            s, e, w = row.split()
            s = float(s) / duration
            e = float(e) / duration
            if w != "_":
                vad[i].append((s, e))
                tw[i].append((s, e, w))
                words[i].append(w)
    return vad, tw, words


def organize_audio_and_nlp_data_train_set(
    audio_path="data/training_set/audio", nlp_path="data/training_set/nlp"
):
    """
    Uses the aligned words from data/train_labeled_words to get vad, timed_words and words. Also sox to get duration in
    seconds.

    Audio:
    splits:  SpeechCorpus/Robot/data/robot_labeled/training_set/audio/10_session_001.wav
    NLP:
    "SpeechCorpus/Robot/data/robot_labeled/training_set/nlp"



    """

    makedirs(audio_path, exist_ok=True)
    makedirs(nlp_path, exist_ok=True)

    label_path = "data/train_labeled_words"
    for lab_path in tqdm(glob(join(label_path, "*track1.lab"))):
        split_name = lab_path.split("__")
        wav_path = get_wav_path(split_name)

        # Extraction
        duration = get_duration_sox(wav_path)
        vad, timed_words, words = lab_to_timed_words(lab_path, duration)

        # Save paths
        name = f"{split_name[1]}_{split_name[-2]}"
        tmp_audio_path = join(audio_path, name + ".wav")
        tmp_nlp_path = join(nlp_path, name)

        makedirs(tmp_nlp_path, exist_ok=True)

        # Copy audio and save nlp data
        shutil.copy(wav_path, tmp_audio_path)
        np.save(join(tmp_nlp_path, "vad.npy"), vad, allow_pickle=True)
        np.save(join(tmp_nlp_path, "timed_words.npy"), timed_words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "words.npy"), words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "duration.npy"), duration, allow_pickle=True)


def organize_audio_and_nlp_data_eval():
    """
    Audio:
    splits:  SpeechCorpus/Robot/data/robot_labeled/training_set/audio/10_session_001.wav
    NLP:
    "SpeechCorpus/Robot/data/robot_labeled/training_set/nlp"
    """

    audio_path = "data/robot_labeled/training_set/audio"
    nlp_path = "data/robot_labeled/training_set/nlp"
    makedirs(audio_path, exist_ok=True)
    makedirs(nlp_path, exist_ok=True)

    label_path = "data/train_labeled_words"
    for lab_path in tqdm(glob(join(label_path, "*track1.lab"))):
        split_name = lab_path.split("__")
        wav_path = get_wav_path(split_name)

        # Extraction
        duration = get_duration_sox(wav_path)
        timed_words, words = lab_to_timed_words(lab_path, duration)

        # Save paths
        name = f"{split_name[1]}_{split_name[-2]}"
        tmp_audio_path = join(audio_path, name + ".wav")
        tmp_nlp_path = join(nlp_path, name)

        makedirs(tmp_nlp_path, exist_ok=True)

        # Copy audio and save nlp data
        shutil.copy(wav_path, tmp_audio_path)
        np.save(join(tmp_nlp_path, "timed_words.npy"), timed_words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "words.npy"), words, allow_pickle=True)
        np.save(join(tmp_nlp_path, "duration.npy"), duration, allow_pickle=True)


def get_vads_holds_shifts_events_train(xml_path, wav_path):
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
    shifts = np.array(shifts, dtype=np.float32) / total_duration
    holds = np.array(holds, dtype=np.float32) / total_duration
    vad = [np.array(ch0) / total_duration, np.array(ch1) / total_duration]
    return (events, {"shifts": shifts, "holds": holds, "vad": vad})


def save_shift_holds_labels(
    audio_path="data/training_set/audio", nlp_path="data/training_set/nlp"
):
    xml_root = "data/train_data/training_set"

    for wav in listdir(audio_path):
        a = wav.split("_")
        name = "_".join(a[1:])
        n = name[-5]
        dir, session = a[0], name.replace(".wav", "")

        xml_path = glob(join(xml_root, dir, session, "*.xml"))[0]
        wav_path = join(audio_path, wav)
        events, events_named = get_vads_holds_shifts_events_train(xml_path, wav_path)

        nlp_session = join(nlp_path, wav.replace(".wav", ""))
        np.save(join(nlp_session, "events.npy"), events, allow_pickle=True)
        np.save(join(nlp_session, "events_named.npy"), events_named, allow_pickle=True)


def test():
    import matplotlib.pyplot as plt
    from turntaking.plot_utils import plot_vad

    organize_audio_and_nlp_data_train_set(
        audio_path="data/test/audio", nlp_path="data/test/nlp"
    )

    save_shift_holds_labels(audio_path="data/test/audio", nlp_path="data/test/nlp")

    # # Test
    # ev_path = "data/training_set/nlp/1_session_001/events_named.npy"
    ev_path = "data/test/nlp/1_session_001/events_named.npy"
    event = np.load(ev_path, allow_pickle=True).item()
    # ev_path = "data/training_set/nlp/1_session_001/events.npy"
    # event = np.load(ev_path, allow_pickle=True)
    print(event.keys())
    vad = event["vad"]
    shifts = event["shifts"]
    holds = event["holds"]
    print(vad[0].shape)
    print(vad[1].shape)
    print(len(shifts))
    print(len(holds))


if __name__ == "__main__":

    ans = input("Unzip files? (y/n)")
    if ans.lower() == "y":
        unzip_files()

    ans = input("Process? (y/n)")
    if ans.lower() == "y":

        # Uses the aligned words from data/train_labeled_words.
        # Extracts vad, timed_words and words from these labels.
        # Uses 'sox' to extract duration in seconds.
        organize_audio_and_nlp_data_train_set()

        # Looks in the original labels to find the labeled shift/hold events
        # Extracts the labels and vad from the base annotations
        # Saves
        #   events.npy:     array of (end of utterance, next_speaker, prev_speaker)
        #                           (0.3445, {0,1,2}, 0), where {0}-holds, {1}-shift, {2}-optional and 0 (in the last
        #                           index means the user was speaking (true for all))
        #   named_events.npy:     shifts, holds, vad based on the base annotations
        save_shift_holds_labels()
