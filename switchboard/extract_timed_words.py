from os import makedirs, listdir
from os.path import join, basename
from glob import glob
from tqdm import tqdm
import numpy as np
from speechcorpus.utils import read_txt, get_duration_sox


class WordExtractor(object):
    def __init__(
        self,
        audio_path="data/audio",
        anno_path="data/swb_ms98_transcriptions",
        save_path="data/nlp",
    ):
        self.audio_path = audio_path
        self.anno_path = anno_path
        self.save_path = save_path

        self.audio_files = glob(join(audio_path, "*.sph"))
        self.all_anno_paths = glob(join(anno_path, "**/**/*word.text"))
        self.all_anno_paths.sort()

        makedirs(save_path, exist_ok=True)

    def extract_channel_text(self, wav_path):
        name = basename(wav_path).replace(".sph", "")
        anno = [f for f in self.all_anno_paths if name in f]

        anno_channel0 = [f for f in self.all_anno_paths if name + "A" in f][0]
        anno_channel1 = [f for f in self.all_anno_paths if name + "B" in f][0]

        duration = get_duration_sox(wav_path)

        vad, words, timed_words, silence, noise = self.extract_text(
            anno_channel0, duration
        )
        vad1, words1, timed_words1, silence1, noise1 = self.extract_text(
            anno_channel1, duration
        )

        self.save_lists(
            name,
            [vad, vad1],
            [words, words1],
            [timed_words, timed_words1],
            [silence, silence1],
            [noise, noise1],
        )

    def save_lists(self, name, vad, words, timed_words, silence, noise):
        # Paths
        session_path = join(self.save_path, name)
        makedirs(session_path, exist_ok=True)
        word_path = join(session_path, "words.npy")
        tw_path = join(session_path, "timed_words.npy")
        vad_path = join(session_path, "vad.npy")
        noise_path = join(session_path, "noise.npy")
        silence_path = join(session_path, "silence.npy")
        np.save(word_path, words, allow_pickle=True)
        np.save(tw_path, timed_words, allow_pickle=True)
        np.save(vad_path, vad, allow_pickle=True)
        np.save(noise_path, noise, allow_pickle=True)
        np.save(silence_path, silence, allow_pickle=True)

    def extract_text(self, anno_word_path, duration):
        transcript = read_txt(anno_word_path)
        silence = []
        noise = []
        vad = []
        words = []
        for line in transcript:
            l = line.split()
            start = float(l[1])
            end = float(l[2])
            utt = l[3]
            if "[silence]" in utt:
                silence.append((start, end))
            elif "[noise]" in utt:
                noise.append((start, end))
            else:
                """ Includes [vocalized-noise], [laughter], I- (restart) """
                # tokens specifically used to indicate that the speaker is talking to someone else
                # "honey, I don't know I am on the phone"
                if utt == "<b_aside>" or utt == "<e_aside>":
                    continue
                words.append(utt)
                vad.append((start, end))

        vad = np.array(vad).astype(np.float32) / duration
        silence = np.array(silence).astype(np.float32) / duration
        noise = np.array(noise).astype(np.float32) / duration

        timed_words = []
        for w, (s, e) in zip(words, vad):
            timed_words.append((s, e, w))
        return vad, words, timed_words, silence, noise

    def run(self):
        for wpath in tqdm(self.audio_files):
            self.extract_channel_text(wpath)


if __name__ == "__main__":
    audio_path = "data/audio"
    print("Extracting Manual VAD")

    ext = WordExtractor()
    ext.run()
