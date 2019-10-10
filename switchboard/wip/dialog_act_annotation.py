from os.path import join, expanduser
from swda import Transcript, Utterance, CorpusReader
from tqdm import tqdm
from collections import Counter
import matplotlib.pyplot as plt


def get_dialog_acts(dset_root):
    cr = CorpusReader(dset_root)
    act_tags = Counter()
    i = 0
    for utt in cr.iter_utterances():
        # print(utt.keys())
        # act_tags.append(utt.act_tag)
        act_tags.update([utt.act_tag])
    return act_tags


def plot_dialog_acts(act_tags, n=15):
    for i, (k, v) in enumerate(act_tags.most_common(n)):
        plt.bar(i, v, label=k)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    dset_root = join(expanduser("~"), "SpeechCorpus/switchboard/data/swda")
    swda_filename = join(dset_root, "sw00utt/sw_0001_4325.utt.csv")
    metadata = join(dset_root, "swda-metadata.csv")

    act_tags = get_dialog_acts(dset_root)

    plot_dialog_acts(act_tags, 30)
