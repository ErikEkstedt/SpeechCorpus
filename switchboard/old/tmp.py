from os.path import join, expanduser
from os import listdir
import shutil
from tqdm import tqdm
from speechcorpus.utils import read_txt, write_txt
from glob import glob


path = "data/audio"

path = join(expanduser("~"), "TurnTaking/data/switchboard")

files = glob(join(path, "**/*.npy"))

len(files)

for f in tqdm(files):
    # print(f)
    src = join(path, f)
    dst = src.replace("sw0", "sw")
    # print('src: ', src)
    # print('dst: ', dst)
    # input()
    shutil.move(src, dst)

# path = 'data/switchboard_test_files.txt'
# path = 'data/switchboard_train_files.txt'

path = join(expanduser("~"), "TurnTaking/turntaking/splits/switchboard/val_split.txt")
files = read_txt(path)
new_list = []
for f in files:
    new_list.append(f.replace("sw0", "sw"))
write_txt(path, new_list)
