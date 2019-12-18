# Robot Human Datasets

Dataset containing dialogues between a human and a robot.


## Current


* [A Testbed for Examining the Timing of Feedback using a Map Task](http://www.speech.kth.se/prod/publications/files/3761.pdf)
  - data is called `training_set`
  - [Download](http://www.speech.kth.se/maptask/training_set_11Nov2014.zip)


* Dowload the zip file
* run `python process_robot_labeled.py`
    - Moves audio to `data/training_set/audio` (default)
    - Extracts annotations to `data/training_set/nlpt` (default)
* nlp folder
    - Function `organize_audio_and_nlp_data_train_set()` extracted using for example `data/train_labeled_words/training_set__1__session_001__track1.lab`
      - Contains time aligned words
        - `timed_words.npy`: arrays containing [start, end] in percentages and word
        - `words.npy`: list of the words spoken for each channel
        - `vad.npy`:  list of arrays only containing start, end of utterances
        - `duration.npy`:  float in seconds
    - Function `save_shift_holds_labels()` extracts from the dataset annotations
      - `events.npy`: array containing (end(in percentages), {0,1,2}(0-hold, 1-shift, 2-optional), 0(prev_speaker))
      - `events_names.npy`: shifts, holds, vad based on annotations 

----------------------------------



## Datasets

* [Data-driven Models for timing feedback responses in a Map Task Dialogue System](http://www.sciencedirect.com/science/article/pii/S0885230814000151)
  - [Download](http://www.speech.kth.se/maptask/user_evaluation_set_11Nov2014.zip)


### CityCS

* system + user
* city questions from images, standing in a crossing etc
* City crowdsourcing

### CmpDSYSEval

### Maptask + MatpaskUES 

maptask with a system + user evaluation study with model

### Tatsuro

Describe a trip you have made etc, toyota.


