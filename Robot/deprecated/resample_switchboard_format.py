from os.path import join, expanduser, basename
from os import makedirs, listdir
from subprocess import call, DEVNULL
from speechcorpus.utils import resample_wav2sph


"""
WAV -> SPH

WAV
---
Input File     : 'session_001.user.wav'
Channels       : 1
Sample Rate    : 16000
Precision      : 16-bit
Duration       : 00:02:02.78 = 1964480 samples ~ 9208.5 CDDA sectors
File Size      : 3.93M
Bit Rate       : 256k
Sample Encoding: 16-bit Signed Integer PCM

SPH
---
Input File     : 'session_001.user.sph'
Channels       : 1
Sample Rate    : 8000
Precision      : 14-bit
Duration       : 00:02:02.78 = 982240 samples ~ 9208.5 CDDA sectors
File Size      : 983k
Bit Rate       : 64.1k
Sample Encoding: 8-bit u-law


SWB SPH
-------
Input File     : '../switchboard/data/audio/sw2020.sph'
Channels       : 2
Sample Rate    : 8000
Precision      : 14-bit
Duration       : 00:09:45.55 = 4684377 samples ~ 43916 CDDA sectors
File Size      : 9.37M
Bit Rate       : 128k
Sample Encoding: 8-bit u-law

Differs in Bit rate 64.1k vs 128k

But downsampling to the same levels and using mu-law encoding should be good enough?
"""


def resample_audio_folder(audiofolder, to_dir):
    makedirs(to_dir)
    for wav in listdir(audiofolder):
        from_path = join(audiofolder, wav)
        to_path = join(to_dir, wav.replace(".wav", ".sph"))
        resample_wav2sph(from_path, to_path)


if __name__ == "__main__":

    root = "data/robot_labeled"

    # training
    audiopath = join(root, "training_set/audio")
    to_path = join(root, "training_set/audio_resampled")
    resample_audio_folder(audiopath, to_path)

    # eval
    audiopath = join(root, "user_evaluation_set/audio")
    to_path = join(root, "user_evaluation_set/audio_resampled")
    resample_audio_folder(audiopath, to_path)

    # wizard
    audiopath = join(root, "wizard/audio")
    to_path = join(root, "wizard/audio_resampled")
    resample_audio_folder(audiopath, to_path)

    # wizard eval random
    audiopath = join(root, "wizard_eval_random/audio")
    to_path = join(root, "wizard_eval_random/audio_resampled")
    resample_audio_folder(audiopath, to_path)

    # wizard eval model
    audiopath = join(root, "wizard_eval_model/audio")
    to_path = join(root, "wizard_eval_model/audio_resampled")
    resample_audio_folder(audiopath, to_path)
