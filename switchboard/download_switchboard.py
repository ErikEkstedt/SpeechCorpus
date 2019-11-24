from os import system, makedirs, listdir
from os.path import join, expanduser, exists, abspath, basename
from glob import glob

"""
REQUIRES LICENCE and ACCESS for the audio
Go to https://catalog.ldc.upenn.edu/LDC97S62 for further information.


Annotations are freely avaliable.
"""


def download(datapath, anno_type):
    if anno_type.lower() == "treebank":
        url = "https://www.isip.piconepress.com/projects/switchboard/releases/ptree_word_alignments.tar.gz"
        datapath = join(datapath, "annotation_treebank")
    elif anno_type.lower() == "manual":
        url = "https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz"
        datapath = join(datapath, "annotation_manual")
    elif anno_type.lower() == "icsi":
        url = "https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_icsi_phone.tar.gz"
        datapath = join(datapath, "annotation_icsi")

    makedirs(datapath, exist_ok=True)
    tar_path = join(datapath, basename(url))

    print("Downloading annotations")
    if not exists(tar_path):
        wget_cmd = ["wget", "-P", datapath, url, "-q", "--show-progress"]
        system(" ".join(wget_cmd))

    print("Extracting")
    system(f"tar xzf {tar_path} -C {datapath}")

    print(f"Remove {tar_path}? (y/n)")
    ans = input()
    if ans.lower() == "y":
        system(f"rm {tar_path}")
        print("Deleted")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Process Switchboard Audio")
    parser.add_argument("--path", default="data")
    parser.add_argument("--treebank", action="store_true")
    parser.add_argument("--manual", action="store_true")
    parser.add_argument("--icsi", action="store_true")
    args = parser.parse_args()

    if args.treebank:
        anno_type = "treebank"
    elif args.manual:
        anno_type = "manual"
    elif args.icsi:
        anno_type = "icsi"
    else:
        print("Treebank, Manual or ICSI annotations?")
        print("python download_switchboard.py --trebank")
        print("python download_switchboard.py --manual")
        print("python download_switchboard.py --icsi")
        sys.exit()

    download(args.path, anno_type)
