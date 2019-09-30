from os import system, makedirs
from subprocess import call, DEVNULL
from os.path import join, expanduser


MARTIN = "data/all_martin_audio.zip"
TRAINING = "data/training_set_11Nov2014.zip"
TRAINING_EVAL = "data/user_evaluation_set_11Nov2014.zip"
WIZARD = "data/wizard.zip"
WIZARD_EVAL = "data/wizard_eval.zip"


def unzip_robot_with_labels(to_dir):
    call(["unzip", TRAINING, "-d", to_dir], stdout=DEVNULL)
    call(["unzip", TRAINING_EVAL, "-d", to_dir], stdout=DEVNULL)
    call(["unzip", WIZARD, "-d", join(to_dir, "wizard")], stdout=DEVNULL)
    call(["unzip", WIZARD_EVAL, "-d", join(to_dir, "wizard_eval")], stdout=DEVNULL)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Unzip robot files")
    parser.add_argument("--datapath", default="data/robot_labeled")
    args = parser.parse_args()

    unzip_robot_with_labels(args.datapath)

    to_dir = args.datapath
