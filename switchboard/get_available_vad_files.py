from os.path import join, basename
from glob import glob
from utils import write_txt


def get_available_treebank():
    path = "data/annotation_treebank/data/alignments"
    vad_files = glob(join(path, "**/*.text"))
    print("Treebank transcript")
    print(f"Found {len(vad_files)} vad files")
    print(f"=> {len(vad_files)/2} sessions")


def get_available_manual():
    path = "data/annotation_manual/swb_ms98_transcriptions"
    vad_files = glob(join(path, "**/**/*word.text"))
    print("Manual transcript")
    print(f"Found {len(vad_files)} vad files")
    print(f"=> {len(vad_files)/2} sessions")


def get_available_icsi():
    path = "data/annotation_icsi/trans"
    pass


def get_all_extracted_vads():
    path = "data/vad"
    npy_files = glob(join(path, "**/vad.npy"))
    vad_files = [f.replace("data/vad/", "").replace("/vad.npy", "") for f in npy_files]
    all_wavs = [basename(f).strip(".wav") for f in glob(join("data/audio", "*.wav"))]
    missing_vad = [f for f in all_wavs if f not in vad_files]

    print(f"Found {len(vad_files)} vad files")
    print(f"Found {len(all_wavs)} wav files")
    print(f"Found {len(missing_vad)} missing vad")

    # sanity check
    assert len(all_wavs) == len(missing_vad) + len(vad_files)

    ans = input("\write vad files to disk (.txt)? (y/n)")
    if ans.lower() == "y":
        write_txt("data/vad.txt", vad_files)
        write_txt("data/vad_missing.txt", missing_vad)


if __name__ == "__main__":

    get_available_manual()
    get_available_treebank()
