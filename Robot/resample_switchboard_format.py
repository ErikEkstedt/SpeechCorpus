from os.path import join, expanduser, basename
from subprocess import call, DEVNULL


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


def resample_wav2sph(audiopath, to_path):
    """ Resample from .wav ->  .sph and mu-law encoding using sox """
    # ffmpeg_cmd = ["ffmpeg", "-i", audiopath, "-acodec", "pcm_mulaw", "-ar", str(8000), to_path]
    cmd = ["sox", audiopath, "-e", "mu-law", "-r", str(8000), "-c", str(1), to_path]
    call(cmd, stdout=DEVNULL)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resample audio")
    parser.add_argument("--audio_folder", default="")
    parser.add_argument("--to_folder", default="")
    args = parser.parse_args()

    audiopath = "session_001.user.wav"
    to_path = "session_001.user.sph"

    resample_wav2sph(audiopath, to_path)
