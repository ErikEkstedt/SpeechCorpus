# SpeechCorpus

A repository for multiple spoken dialog corpora:

[Open Speech & Language Resources](https://www.openslr.org/resources.php)

##  Installation

* create python environment (Conda is recommended)
* source environment
* `pip install -r requirements.txt`
* `pip install .` or `pip install -e .` in the repo root directory

## Collection of SpeechCorpus

* [Maptask](http://groups.inf.ed.ac.uk/maptask/)
  - Publicly Available
  - Download: `./download_maptask.py`
  - [Info](./info/MaptaskNotes.md)
* [LDC: Swithcboard](https://catalog.ldc.upenn.edu/topten):
  - Requires access 
  - Downloads .sph files
* [TiMit](https://catalog.ldc.upenn.edu/LDC93S1)
  - Not Implemented
  - Acoustic-Phonetic Continuous Speech Corpus
* [ZeroSpeech](https://zerospeech.com/2017/)
  - Not Implemented
* [Buckeye](http://buckeyecorpus.osu.edu/php/speech.php):
  - Requires License
  - One channel
  - Download: `./download_buckeye.py`
  - [Pip](https://nbviewer.jupyter.org/github/scjs/buckeye/blob/master/Quickstart.ipynb) Python
    - `pip install buckeye`
  - [Github](https://github.com/scjs/buckeye)
  - [Info](./info/BuckeyeCorpusmanual.pdf)

* [IEMOCAP](https://sail.usc.edu/iemocap/)
  - Not Implemted
  - Dyadic multimodal
  - Contains emotion


## Maptask
see [Maptask README](./maptask/README.md)
```bash

Input File     : 'q1ec2.wav'
Channels       : 2
Sample Rate    : 20000
Precision      : 16-bit
Duration       : 00:05:34.04 = 6680785 samples ~ 25052.9 CDDA sectors
File Size      : 26.7M
Bit Rate       : 640k
Sample Encoding: 16-bit Signed Integer PCM

```

## Switchboard
see [Maptask README](./maptask/README.md)
  ```
  .
  ├── docs
  ├── swb1_d1
  │   └── data
  ├── swb1_d2
  │   └── data
  ├── swb1_d3
  │   └── data
  └── swb1_d4
      └── data

  -----------------------------------

  Input File     : 'sw02005.sph'
  Channels       : 2
  Sample Rate    : 8000
  Precision      : 14-bit
  Duration       : 00:04:12.30 = 2018387 samples ~ 18922.4 CDDA sectors
  File Size      : 4.04M
  Bit Rate       : 128k
  Sample Encoding: 8-bit u-law

  ```


## Buckeye

see [Buckeye README](./buckeye/README.md)

## ZeroSpeech

see [ZeroSpeech README](./zerospeech/README.md)

## IEMOCAP
see [IEMOCAP README](./iemocap/README.md)

