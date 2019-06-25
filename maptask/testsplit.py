from os.path import join, expanduser, split
from os import listdir, makedirs
import argparse
import shutil

# Familiarity and Eye-Contact In addition to the design variables relating to the maps
# themselves, two other variables were incorporated in the design of the corpus overall.

# Subjects are necessarily paired for the task. Each pair of familiar subjects
# was tested in coordination with another pair who were UNKNOWN To either member of the
# first pair. Two pairs formed a QUADRUPLE of subjects who used among them a different set
# of four map-pairs, with maps being assigned to pairs by Latin Square. Each subject
# participated in four dialogues, twice as Instruction Giver and twice as Instruction
# Follower, once in each case with a familiar partner, and once with an unfamiliar
# partner. As Instruction Giver they gave directions on the same map, but when following
# they used different maps each time. Half of the subjects gave instructions to a familiar
# partner first, the others to an unfamiliar partner first.

# The option of placing a small barrier between Map Task participants to prevent them
# from seeing each other's faces allowed us to control the availability of the visual
# channel for communication. Half of the subjects who took part in the task were able to
# make EYE-CONTACT with their partner, while the other half had NO EYE-CONTACT.
# Eye-contact [e]     q1ec2
# No Eye-contact [n]  q1nc2

# The experiment uses a Latin Squares design. Participants were asked to come to the
# experiment with someone they knew, thus forming familiar pairs.
# Two pairs make a quad q1, q2, q3.

# q2ecX - 2 males, 2 females, eye contact
# q4ncX - 2 males, 2 females, no eye contact
# 16 files total -> 12.5 % of total data


parser = argparse.ArgumentParser(description="Maptask Testplit")
parser.add_argument("--audio_path", default="data/audio")
parser.add_argument("--test_path", default="data/audio_test")
args = parser.parse_args()

test_files = []
train_files = []
for f in listdir(args.audio_path):
    if f.startswith("q2ec") or f.startswith("q4nc"):
        test_files.append(f)
    else:
        train_files.append(f)


print("Test files: ", len(test_files))
print("Training files: ", len(train_files))

ans = input("Write split to disk (.txt)? (y/n)")
if ans.lower() == "y":
    with open("data/maptask_test_files.txt", "w") as f:
        f.write("\n".join(test_files))

    with open("data/maptask_train_files.txt", "w") as f:
        f.write("\n".join(train_files))


ans = input(f"Move test files to {args.test_path}? (y/n)")
if ans.lower() == "y":
    makedirs(args.test_path)
    print("Moving test files -> ", args.test_path)
    src = join(args.audio_path, "info.json")  # info file
    dst = join(args.test_path, "info.json")
    shutil.move(src, dst)
    for f in test_files:  # features
        src = join(args.audio_path, f)
        dst = join(args.test_path, f)
        shutil.move(src, dst)
