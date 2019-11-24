from os.path import join, expanduser, split, abspath, exists
from os import listdir, makedirs
from subprocess import check_output
import xml.etree.ElementTree as ET
import numpy as np
from tqdm import tqdm
from speechcorpus.utils import get_duration_sox


"""
Extract annotation inforamtion.

Extracts:
    - VAD
    - Words
    - POS
    - Silence
    - Noise

* Save vad as arrays with percentages based on time
    - (vad_start, vad_end) / total_duration
* Save to disk at `data/vad/filename_vad.npy`
* Make to one hot dependent on frame size etc during dataset loading
"""

# =========================== Words, Vad, Silence ==============================
def get_timed_units(xml_path, duration):
    xml_element_tree = ET.parse(xml_path)
    tu, sil, noi = [], [], []
    for elem in xml_element_tree.iter():
        try:
            tmp = (float(elem.attrib["start"]), float(elem.attrib["end"]))
        except:
            continue
        if elem.tag == "tu":
            # elem.attrib: start, end, utt
            # tu.append({"time": tmp, "words": elem.text})
            id = elem.attrib["id"]
            if len(elem.text.split()) > 1:
                print(elem.text)
                print(tmp)
                input()
            else:
                print(elem.text)
            tu.append({"time": tmp, "words": elem.text, "id": id})
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
        s = t["time"][0] / duration
        e = t["time"][1] / duration
        vad.append((s, e))
        words.append({"word": t["words"], "time": (s, e)})
    assert len(vad) == len(words)
    vad = np.array(vad)
    sil = np.array(sil) / duration
    noi = np.array(noi) / duration
    return {"vad": vad, "words": words, "silence": sil, "noise": noi}


def get_pos(pos_xml_path, tu_xml_path, tokens_xml_path, duration):
    """ Slow iteration through files """

    def find_time_tu(id, elem_tree):
        for elem in elem_tree.iter():
            if "id" in elem.keys():
                if id == elem.attrib["id"]:
                    s = float(elem.attrib["start"])
                    e = float(elem.attrib["end"])
                    return s, e

    def find_time_token(id, elem_tree):
        for elem in elem_tree.iter():
            if "turef" in elem.keys():
                if id == elem.attrib["id"]:
                    s = float(elem.attrib["start"])
                    e = float(elem.attrib["end"])
                    return s, e

    pos_xml_element_tree = ET.parse(pos_xml_path)
    tu_xml_element_tree = ET.parse(tu_xml_path)
    tokens_xml_element_tree = ET.parse(tokens_xml_path)

    # examples
    # <tw tag="ppss" id="q1ec1g.pos.34" >< href="q1ec1.g.tokens.xml#id(q1ec1g.tok.2)"/></tw>
    # <tw tag="ber"  id="q1ec1g.pos.35" >< href="q1ec1.g.tokens.xml#id(q1ec1g.tok.3)"/></tw>
    # <tw tag="vbg"  id="q1ec1g.pos.36" >< href="q1ec1.g.timed-units.xml#id(q1ec1g.40)"/></tw>
    # <tw tag="ql"   id="q1ec1g.pos.110">< href="q1ec1.g.timed-units.xml#id(q1ec1g.120)..id(q1ec1g.120.1)"/></tw>

    # each line contains 2 elements tw, href
    all_pos, tmp = [], {}
    for elem in pos_xml_element_tree.iter():
        if "tag" in elem.attrib:
            tmp["pos"] = elem.attrib["tag"]

        elif "href" in elem.attrib:
            ref, id = elem.attrib["href"].split("#")
            id = id.replace("id(", "").replace(")", "")  # q7nc4g.1

            if ".." in id:  # sometimes 2 places are referenced
                id0, id1 = id.split("..")
                s, _ = find_time_tu(id0, tu_xml_element_tree)
                _, e = find_time_tu(id1, tu_xml_element_tree)
            else:
                if "timed-units" in ref:
                    s, e = find_time_tu(id, tu_xml_element_tree)
                elif "tokens" in ref:
                    s, e = find_time_token(id, tokens_xml_element_tree)
                else:
                    print("no ref")
            tmp["time"] = (s / duration, e / duration)
            all_pos.append(tmp)
            tmp = {}

    # concatenated wods "we're" contain 2 POS tags
    # this method splits the times in half (not entirely accurate but good enough
    for p1, p2 in zip(all_pos[:-1], all_pos[1:]):
        if p1["time"] == p2["time"]:
            s = p1["time"][0]
            e = p1["time"][1]
            mid = (s + e) / 2
            p1["time"] = (s, mid)
            p2["time"] = (mid, e)
    return all_pos


def get_annotation(fname, anno_path, audio_path):
    """
    Extracts vad-timings, words, silences and noise

    fname:          str, e.g 'q1ec1.wav'
    anno_path:      path, path to annotations
    data_path:      path, path to wavs (for duration)
    """

    # File info
    wav_path = join(audio_path, fname)
    duration = get_duration_sox(wav_path)

    name = fname.strip(".wav")
    tu_path = join(anno_path, "Data/timed-units")
    pos_path = join(anno_path, "Data/pos")
    token_path = join(anno_path, "Data/tokens")

    pos_xml_path = join(pos_path, name)
    tu_xml_path = join(tu_path, name)
    token_xml_path = join(token_path, name)

    tu_path_ch0 = tu_xml_path + ".g.timed-units.xml"
    tu_path_ch1 = tu_xml_path + ".f.timed-units.xml"
    pos_path_ch0 = pos_xml_path + ".g.pos.xml"
    pos_path_ch1 = pos_xml_path + ".f.pos.xml"
    token_path_ch0 = token_xml_path + ".g.tokens.xml"
    token_path_ch1 = token_xml_path + ".f.tokens.xml"

    # Find word xmls
    # contains words
    tu_ch0 = get_timed_units(tu_path_ch0, duration)
    tu_ch1 = get_timed_units(tu_path_ch1, duration)

    # Find word xmls
    pos_ch0 = get_pos(pos_path_ch0, tu_path_ch0, token_path_ch0, duration)
    pos_ch1 = get_pos(pos_path_ch1, tu_path_ch1, token_path_ch1, duration)

    vad = [tu_ch0["vad"], tu_ch1["vad"]]
    words = [tu_ch0["words"], tu_ch1["words"]]
    pos = [pos_ch0, pos_ch1]
    silence = [tu_ch0["silence"], tu_ch1["silence"]]
    noise = [tu_ch0["noise"], tu_ch1["noise"]]
    return {"vad": vad, "words": words, "pos": pos, "silence": silence, "noise": noise}


def save_maptask_anno(audio_path, anno_path, save_path):
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
        pos_path = join(session_path, "pos.npy")

        # if (
        #     exists(word_path)
        #     and exists(vad_path)
        #     and exists(silence_path)
        #     and exists(noise_path)
        #     and exists(pos_path)
        # ):
        #     continue

        anno = get_annotation(wav, anno_path, audio_path)

        np.save(vad_path, anno["vad"], allow_pickle=True)
        np.save(word_path, anno["words"], allow_pickle=True)
        np.save(pos_path, anno["pos"], allow_pickle=True)
        np.save(noise_path, anno["noise"], allow_pickle=True)
        np.save(silence_path, anno["silence"], allow_pickle=True)


if __name__ == "__main__":
    from os.path import join

    from turntaking.dataprocessing.tokenizer import NewCustomTokenizer

    audio_path = "data/audio"
    anno_path = "data/annotations"
    save_path = "data/nlp3"

    save_maptask_anno(audio_path, anno_path, save_path)
    # save_maptask_vad(audio_path, anno_path, save_path)

    # # Test
    if False:
        ppath = join(save_path, "q1ec1/pos.npy")
        wpath = join(save_path, "q1ec1/words.npy")
        vpath = join(save_path, "q1ec1/vad.npy")
        npath = join(save_path, "q1ec1/noise.npy")
        spath = join(save_path, "q1ec1/silence.npy")

        pos = list(np.load(ppath, allow_pickle=True))
        words = list(np.load(wpath, allow_pickle=True))
        vad = list(np.load(vpath, allow_pickle=True))
        noise = list(np.load(npath, allow_pickle=True))
        silence = list(np.load(spath, allow_pickle=True))

        tokenizer = NewCustomTokenizer()

        for dialog in listdir(save_path):
            wpath = join(save_path, dialog, "words.npy")
            words = list(np.load(wpath, allow_pickle=True))
            for ch in range(2):
                for w in words[ch]:
                    toks = tokenizer(w)
                    if len(toks) > 2:
                        print(dialog, ":", w, "->", toks)
                        input()

        print("words: ", len(words[0]))
        print("vad: ", len(vad[0]))
        print("pos: ", len(pos[0]))
        print("noise: ", len(noise[0]))
        print("silence: ", len(silence[0]))

        # Check
        for p1, p2 in zip(pos[0][:-1], pos[0][1:]):
            if p1["time"] == p2["time"]:
                s = p1["time"][0]
                e = p1["time"][1]
                mid = (s + e) / 2
                print("same time")
