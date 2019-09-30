from os.path import join, expanduser, basename
from os import makedirs
import shutil
from glob import glob
import argparse

parser = argparse.ArgumentParser(description="Move CallFriend Audio")
parser.add_argument("--audiopath", default="data/audio")
args = parser.parse_args()


makedirs(args.audiopath)
for fpath in glob("data/cf_ameng_n/data/**/*.sph"):
    wav_name = basename(fpath)
    to_path = join(args.audiopath, wav_name)
    shutil.move(fpath, to_path)
