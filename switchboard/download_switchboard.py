from os import system, makedirs, listdir
from os.path import join, expanduser, exists, abspath, basename
from glob import glob

"""
REQUIRES LICENCE and ACCESS. 
Go to https://catalog.ldc.upenn.edu/LDC97S62 for further information.
"""


def download(datapath, url):
    tar_path = join(datapath, "switchboard_word_alignments.tar.gz")

    print("Downloading annotations")
    if not exists(tar_path):
        wget_cmd = ["wget", "-P", datapath, url, "-q", "--show-progress"]
        system(" ".join(wget_cmd))

    print("Extracting")
    system(f"tar xjf {tar_path} -C {datapath}")

    print("Remove {tar_path}? (y/n)")
    ans = input()
    if ans.lower() == "y":
        system(f"rm {tar_path}")
        print("Deleted")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process Switchboard Audio")
    parser.add_argument("--url", default=None)
    parser.add_argument("--path", default="data")
    args = parser.parse_args()

    download(args.path, args.url)
