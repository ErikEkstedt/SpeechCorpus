# Robot Human Datasets

Dataset containing dialogues between a human and a robot.

* [A Testbed for Examining the Timing of Feedback using a Map Task](http://www.speech.kth.se/prod/publications/files/3761.pdf)
  - data is called `training_set`
  - [Download](http://www.speech.kth.se/maptask/training_set_11Nov2014.zip)
* [Data-driven Models for timing feedback responses in a Map Task Dialogue System](http://www.sciencedirect.com/science/article/pii/S0885230814000151)
  - [Download](http://www.speech.kth.se/maptask/user_evaluation_set_11Nov2014.zip)


## Unzip and Organize

* Run `unzip_and_organize.py`
  - Extracts zip files and organize them into appropriate folder structure
* Run `resample_switchboard_format.py`
  - Creates audio_resample folder with 8k mulaw encoded .sph files (like switchboard)
  - There is one difference in bitrate (swb: 128k vs resampled 64.1k) which I don't know
    how to fix. It should not disrupt the feature extraction and listening is fine.




## Vad

Extract Vads
  - run `python annotations.py`
    - extract vads and saves in `data/training_set/vad/{filename}/vad.npy`
    - Moves audio into `data/training_set/audio`
  - run `fix_wavs.py`
    - some wavs have something wrong with header or the like
    - This script only runs soz and resamples the audio to the same samplerate -> fixes
      files


## CityCS

* system + user
* city questions from images, standing in a crossing etc
* City crowdsourcing

## CmpDSYSEval

* 

## Maptask + MatpaskUES 

maptask with a system + user evaluation study with model


## Tatsuro

Describe a trip you have made etc, toyota.


