from xml.dom import minidom
import xml.dom as dom
import xml.etree.ElementTree as ET
import numpy as np
from os import makedirs, listdir, system
from os.path import join, expanduser, isfile
from speechcorpus.utils import read_wav, get_duration_sox
import shutil
from tqdm import tqdm


def get_vad(xml_path, wav_path, duration=None):
    if duration is None:
        duration = get_duration_sox(wav_path)
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
    vad0 = np.array(ch0, dtype=np.float32) / duration
    vad1 = np.array(ch1, dtype=np.float32) / duration
    if len(vad1) > 0:
        vad = (vad0, vad1)
    else:
        vad = vad0
    return vad, duration


def get_all_vads_wavs(root_path, vad_path, audio_path, save=False):
    makedirs(vad_path, exist_ok=True)
    makedirs(audio_path, exist_ok=True)

    prefixes = set(
        [
            f[:5]
            for f in listdir(root_path)
            if isfile(join(root_path, f)) and not f.startswith("log")
        ]
    )
    for i in tqdm(prefixes):
        prefix = str(i).zfill(3)
        user_xml = join(root_path, prefix + "_user.xml")
        user_wav = join(root_path, prefix + "_user.wav")
        system_xml = join(root_path, prefix + "_system.xml")
        system_wav = join(root_path, prefix + "_system.wav")

        dur_user = get_duration_sox(user_wav)
        dur_system = get_duration_sox(system_wav)

        if dur_system > dur_user:
            dur = dur_system
        else:
            dur = dur_user

        vad_user_list, dur_user = get_vad(user_xml, user_wav, duration=dur)
        vad_sys_list, dur_system = get_vad(system_xml, system_wav, duration=dur)
        vad = [vad_user_list, vad_sys_list]

        if save:
            vpath = join(vad_path, prefix)
            makedirs(vpath, exist_ok=True)
            np.save(join(vpath, "vad.npy"), vad, allow_pickle=True)
            to_path = join(audio_path, f"{prefix}.wav")
            system(f"sox -M {user_wav} {system_wav} {to_path}")
        else:
            n_frames = round(dur / 0.05)
            vad_oh = list_percentage_to_onehot(vad, n_frames)
            plt.close()
            visualize_vad(vad_oh)
            plt.xlim([0, vad_oh.shape[1]])
            plt.tight_layout()
            plt.pause(0.01)
            input()


if __name__ == "__main__":
    from speechcorpus.utils import list_percentage_to_onehot
    from turntaking.plot_utils import visualize_vad
    import matplotlib.pyplot as plt
    import sounddevice as sd

    root_path = "data/wizard"
    vad_path = join(root_path, "vad")
    audio_path = join(root_path, "audio")
    get_all_vads_wavs(root_path, vad_path, audio_path, save=True)

    # user_xml = join(root_path, "001_1_user.xml")
    # user_wav = join(root_path,"001_1_user.wav")
    # system_xml = join(root_path,"001_1_system.xml")
    # system_wav = join(root_path,"001_1_system.wav")

    # test
    # vad_path = join(vad_path, '001_1', 'vad.npy')
    # wav_path = join(audio_path, '001_1.wav')

    # y, sr = read_wav(wav_path)

    # vad = list(np.load(vad_path))

    # dur = get_duration_sox(wav_path)
    # n_frames = round(dur / 0.05)
    # vad_oh = list_percentage_to_onehot(vad, n_frames)
    # plt.close()
    # visualize_vad(vad_oh)
    # plt.xlim([0, vad_oh.shape[1]])
    # plt.tight_layout()
    # plt.pause(0.01)
    # sd.play(y, samplerate=sr)
