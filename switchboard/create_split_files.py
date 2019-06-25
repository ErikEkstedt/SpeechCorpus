from os.path import join
from os import listdir
import numpy as np
from utils import write_txt

"""
As of now just randomly creates a test/train set.

For reproducability use the existing:
    'data/switchboard_test_files.txt' 
    'data/switchboard_train_files.txt' 
"""


def create_testsplit(filepath, testsplit=0.15):
    all_files = [f for f in listdir(filepath) if f.endswith(".wav")]
    n_test = int(len(all_files) * testsplit)
    test_files = list(np.random.choice(all_files, size=n_test, replace=False))
    train_files = [f for f in all_files if f not in test_files]

    print("Total files: ", len(all_files))
    print("Train files: ", len(train_files))
    print(f"Test files: {len(test_files)}  ~{testsplit*100}%")

    test_path = "data/switchboard_test_files.txt"
    train_path = "data/switchboard_train_files.txt"
    write_txt(test_path, test_files)
    write_txt(train_path, train_files)
    print("test files saved at -> ", test_path)
    print("train files saved at -> ", train_path)


if __name__ == "__main__":
    filepath = "data/audio"
    testsplit = 0.15
    create_testsplit(filepath, testsplit)
