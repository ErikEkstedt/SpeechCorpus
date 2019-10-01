from os import system, makedirs, listdir, walk
from os.path import join, expanduser, basename, isdir
from subprocess import call, DEVNULL
from glob import glob
import shutil


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


def move_audio_annotations_training_eval_set(root="data/robot_labeled/training_set"):
    wav_files = glob(join(root, "**/**/*.wav"))
    to_dir = join(root, "audio")
    makedirs(to_dir)

    for fpath in wav_files:
        wav_name = basename(fpath)
        to_path = join(to_dir, wav_name)
        shutil.move(fpath, to_path)

    anno_files = glob(join(root, "**/**/*.xml"))
    to_dir = join(root, "annotations")
    makedirs(to_dir)

    for fpath in anno_files:
        wav_name = basename(fpath)
        to_path = join(to_dir, wav_name)
        shutil.move(fpath, to_path)

    # remove empty folders
    dirs = [
        f
        for f in listdir(root)
        if isdir(join(root, f)) and f not in ["audio", "annotations"]
    ]

    for d in dirs:
        shutil.rmtree(join(root, d))

    print("Done!")
    print("Moved all training_set audio -> training_set/audio")
    print("Moved all training_set annotations -> training_set/annotations")


def move_audio_annotations_wizard(root="data/robot_labeled/wizard"):
    wav_files = glob(join(root, "*.wav"))
    to_dir = join(root, "audio")
    makedirs(to_dir)
    for fpath in wav_files:
        wav_name = basename(fpath)
        to_path = join(to_dir, wav_name)
        shutil.move(fpath, to_path)

    anno_files = glob(join(root, "*.xml"))
    to_dir = join(root, "annotations")
    makedirs(to_dir)
    for fpath in anno_files:
        wav_name = basename(fpath)
        to_path = join(to_dir, wav_name)
        shutil.move(fpath, to_path)


def move_audio_annotations_wizard_eval(root="data/robot_labeled/wizard_eval"):
    """ move audio robot and random """

    # rename xml files as audio
    random_audio = join(root, "audio_random")
    random_anno = join(root, "annotations_random")
    model_audio = join(root, "audio_model")
    model_anno = join(root, "annotations_model")
    makedirs(random_audio)
    makedirs(random_anno)
    makedirs(model_audio)
    makedirs(model_anno)

    for root_dir, dirs, files in walk(root):
        user_audio, system_audio, anno = None, None, None
        if root_dir in [random_audio, random_anno, model_audio, model_anno]:
            continue
        if root_dir.endswith("random"):
            for f in files:
                if f.endswith(".wav"):
                    name = f.split(".")[0]
                    if "user" in f:
                        user_audio = f
                    elif "system" in f:
                        system_audio = f
                if f.endswith(".xml") and not "_e" in f:
                    anno = f

            xml_name = name + ".xml"
            # print('root:', root_dir)
            # print('anno: ', anno)
            # print('new anno: ', xml_name)
            # print('user: ', user_audio)
            # print('sys: ', system_audio)
            if user_audio is not None:
                shutil.move(join(root_dir, user_audio), join(random_audio, user_audio))
            if system_audio is not None:
                shutil.move(
                    join(root_dir, system_audio), join(random_audio, system_audio)
                )
            if anno is not None:
                shutil.move(join(root_dir, anno), join(random_anno, xml_name))

        elif root_dir.endswith("model"):
            for f in files:
                if f.endswith(".wav"):
                    name = f.split(".")[0]
                    if "user" in f:
                        user_audio = f
                    elif "system" in f:
                        system_audio = f
                if f.endswith(".xml"):
                    anno = f

            xml_name = name + ".xml"
            # print('root:', root_dir)
            # print('anno: ', anno)
            # print('new anno: ', xml_name)
            # print('user: ', user_audio)
            # print('sys: ', system_audio)
            if user_audio is not None:
                shutil.move(join(root_dir, user_audio), join(model_audio, user_audio))
            if system_audio is not None:
                shutil.move(
                    join(root_dir, system_audio), join(model_audio, system_audio)
                )
            if anno is not None:
                shutil.move(join(root_dir, anno), join(model_anno, xml_name))

    for root_dir, dirs, files in walk(root):
        if not root_dir in [random_audio, random_anno, model_audio, model_anno, root]:
            shutil.rmtree(root_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Unzip robot files")
    parser.add_argument("--datapath", default="data/robot_labeled")
    args = parser.parse_args()

    ans = input("Unzip? (y/n)\n> ")
    if ans.lower() == "y":
        unzip_robot_with_labels(args.datapath)

    # Move all robot files
    ans = input("Move all robot files? (y/n)\n> ")
    if ans.lower() == "y":
        root = "data/robot_labeled/training_set"
        move_audio_annotations_training_eval_set(root)
        root = "data/robot_labeled/user_evaluation_set"
        move_audio_annotations_training_eval_set(root)
        move_audio_annotations_wizard()
        move_audio_annotations_wizard_eval()
