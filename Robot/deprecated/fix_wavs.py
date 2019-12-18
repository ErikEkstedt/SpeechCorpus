from os.path import join, basename
from os import makedirs, listdir
from subprocess import check_output
import shutil


path = "data/training_set/audio"
new_path = "data/training_set/audio2"
makedirs(new_path)


for fname in listdir(path):
    check_output(f"sox {join(path,fname)} -r 16000 {join(new_path, fname)}", shell=True)

ans = input("remove old files? (y/n)")
if ans.lower() == "y":
    shutil.rmtree(path)
    shutil.move(new_path, path)
