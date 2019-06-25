#!/usr/bin/env python

from os import system, makedirs

"""
Requires Licence! 

Please visit https://buckeyecorpus.osu.edu for further instructions.
"""


def download_corpora(url, savepath="data/Buckeye"):
    makedirs(savepath)
    print("Downloading corpora -> ", savepath)
    for i in range(1, 41):
        n = str(i).zfill(2)
        print(f"Download {i}/40")
        url = url + f"/s{n}.zip"
        wget_cmd = " ".join(["wget", "-P", savepath, url, "-q", "--show-progress"])
        system(wget_cmd)
    print("Download complete!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Buckeye Audio")
    parser.add_argument("--url", default=None)
    parser.add_argument("--path", default="data")
    args = parser.parse_args()

    download_corpora(args.url, args.path)
