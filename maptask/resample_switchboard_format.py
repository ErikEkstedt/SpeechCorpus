from os.path import join, expanduser, basename
from os import makedirs, listdir
from subprocess import call, DEVNULL
from tqdm import tqdm
from speechcorpus.utils import resample_wav2sph


def resample_audio_folder(audiofolder, to_dir):
    makedirs(to_dir)
    for wav in tqdm(listdir(audiofolder)):
        from_path = join(audiofolder, wav)
        to_path = join(to_dir, wav.replace(".wav", ".sph"))
        resample_wav2sph(from_path, to_path)


if __name__ == "__main__":

    audiofolder = "data/audio"
    to_path = "data/audio_resampled"
    resample_audio_folder(audiofolder, to_path)
