from os.path import join, expanduser, split, abspath, exists
from os import listdir, makedirs
from subprocess import check_output
import xml.etree.ElementTree as ET
import numpy as np
from tqdm import tqdm

from utils import get_duration_sox


"""
Extract VAD based on annotations

* Save vad as arrays with percentages based on time
    - (vad_start, vad_end) / total_duration
* Save to disk at `data/vad/filename_vad.npy`
* Make to one hot dependent on frame size etc during dataset loading
"""


def get_word_annotation(fname, anno_path, data_path):
    """
    fname:   str, e.g 'q1ec1.wav'
    """

    def get_times(xml_element_tree, duration):
        tu, sil, noi = [], [], []
        for elem in xml_element_tree.iter():
            try:
                tmp = (float(elem.attrib["start"]), float(elem.attrib["end"]))
            except:
                continue
            if elem.tag == "tu":
                # elem.attrib: start, end, utt
                # tu.append({"time": tmp, "words": elem.text})
                tu.append({"time": tmp, "words": elem.text})
            elif elem.tag == "sil":
                # elem.attrib: start, end
                sil.append(tmp)
            elif elem.tag == "noi":
                # elem.attrib: start, end, type='outbreath/lipsmack/...'
                noi.append(tmp)

        tu.sort(key=lambda x: x["time"][0])
        sil.sort(key=lambda x: x[0])
        noi.sort(key=lambda x: x[0])

        vad, words = [], []
        for t in tu:
            vad.append(t["time"])
            words.append(t["words"])

        assert len(vad) == len(words)
        vad = np.array(vad) / duration
        sil = np.array(sil) / duration
        noi = np.array(noi) / duration
        return {"vad": vad, "words": words, "silence": sil, "noise": noi}

    # Find xmls

    name = fname.strip(".wav")
    word_anno_path = join(anno_path, "Data/timed-units")

    xml_element_tree0 = ET.parse(join(word_anno_path, name + ".g.timed-units.xml"))
    xml_element_tree1 = ET.parse(join(word_anno_path, name + ".f.timed-units.xml"))

    wav_path = join(data_path, fname)
    duration = get_duration_sox(wav_path)

    ch0 = get_times(xml_element_tree0, duration)
    ch1 = get_times(xml_element_tree1, duration)
    return [ch0, ch1]


def save_maptask_vad(audio_path, anno_path, save_path):
    makedirs(save_path, exist_ok=True)

    wav_files = [f for f in listdir(audio_path) if f.endswith(".wav")]

    for wav in tqdm(wav_files):
        session = wav.strip(".wav")
        session_path = join(save_path, session)
        makedirs(session_path, exist_ok=True)

        word_path = join(session_path, "words.npy")
        vad_path = join(session_path, "vad.npy")
        noise_path = join(session_path, "noise.npy")
        silence_path = join(session_path, "silence.npy")

        if (
            exists(word_path)
            and exists(vad_path)
            and exists(silence_path)
            and exists(noise_path)
        ):
            continue

        anno = get_word_annotation(wav, anno_path, audio_path)

        words = [anno[0]["words"], anno[1]["words"]]
        vad = [anno[0]["vad"], anno[1]["vad"]]
        noise = [anno[0]["noise"], anno[1]["noise"]]
        silence = [anno[0]["silence"], anno[1]["silence"]]

        np.save(word_path, words, allow_pickle=True)
        np.save(vad_path, vad, allow_pickle=True)
        np.save(noise_path, noise, allow_pickle=True)
        np.save(silence_path, silence, allow_pickle=True)


if __name__ == "__main__":

    audio_path = "data/audio"
    anno_path = "data/annotations"
    save_path = "data/vad"

    save_maptask_vad(audio_path, anno_path, save_path)

    # # Test
    # test = 'data/vad/q1ec1'
    # vad = list(np.load(join(test, 'vad.npy'), allow_pickle=True))
