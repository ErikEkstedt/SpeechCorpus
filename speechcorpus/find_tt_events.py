from os.path import join, expanduser
from os import listdir, makedirs
from tqdm import tqdm
import numpy as np
from turntaking.utils import (
    read_json,
    find_nonzero_start_ends,
    time_to_frames,
    frames_to_time,
)


def feats_append_event(
    feat,
    pauses=[0.25, 0.5, 0.7],
    time_step=0.05,
    warm_up=0,
    time_after_event=2,
    verbose=False,
):
    if "events" in feat.keys():
        return feat

    warm_up_frames = time_to_frames(warm_up, time_step)
    frames_after_event = time_to_frames(time_after_event, time_step)

    vad1 = feat["vad"][0]
    vad2 = feat["vad"][1]
    # choose an arbitrary vector vad1
    # multiply vector with 2 -> zeros and 2
    # subtract other vad -> vector of 2, 1, 0 , -1
    # 2: only vad1 is speaking
    # 1: both are speaking
    # 0: both silent
    # -1: only vad 2 is speaking
    speaking = 2 * vad1 - vad2
    both_silent = (speaking == 0).astype(np.int)
    events = {"both_silent": both_silent}

    events["pauses"] = {}
    for p in pauses:
        events["pauses"][f"pause{p}"] = []
        events["pauses"][f"pause{p}_silence"] = []

    starts, ends = find_nonzero_start_ends(both_silent)
    for s, e in zip(starts, ends):
        if s < warm_up_frames:
            # print("skip start")
            continue  # skip pauses earlier than warmup time (beginning of audio)

        # diff = frames_to_time(e - s, time_step)
        diff = e - s
        if verbose:
            print("s: ", s)
            print("e: ", e)
            print("diff: ", diff)

        turntaker = (
            3
        )  # switch to 3 from None indicating no one taken the turn during vad pred
        for v1, v2 in zip(
            vad1[s + 1 : s + frames_after_event], vad2[s + 1 : s + frames_after_event]
        ):
            if any([v1, v2]) > 0:
                if v1 > 0:
                    turntaker = 0
                else:
                    turntaker = 1
                break

        for p in pauses:
            pf = time_to_frames(p, time_step)
            if diff > pf:
                # the event is after the pause -> start frame + pause
                # (the entire pause (e) might be longer)
                if turntaker < 3:
                    events["pauses"][f"pause{p}"].append((s + pf, turntaker))
                else:
                    events["pauses"][f"pause{p}_silence"].append((s + pf, turntaker))

                if verbose:
                    print("p: ", p)
                    print("pf: ", pf)
                    print("diff: ", diff)
                    input()
    feat["events"] = events
    return feat


def load_feats_append_events(feature_path, conf, verbose=False):
    feat_files = [f for f in listdir(feature_path) if f.endswith(".npy")]
    for f in tqdm(feat_files):
        fpath = join(feature_path, f)
        feat = np.load(fpath, allow_pickle=True).item()
        feat = feats_append_event(
            feat,
            pauses=conf["events"]["pauses"],
            time_step=conf["features"]["time_step"],
            time_after_event=conf["events"]["time_after_event"],
            verbose=verbose,
        )
        np.save(fpath, feat)


def find_events(
    feature_path=None,
    pauses=[0.25, 0.5],
    time_step=0.05,
    warm_up=0,
    max_time=2,
    verbose=False,
):
    warm_up_frames = time_to_frames(warm_up, time_step)
    max_frames = time_to_frames(max_time, time_step)
    feat_files = [f for f in listdir(feature_path) if f.endswith(".npy")]

    print("N files: ", len(feat_files))

    events = {}
    for f in tqdm(feat_files):
        feat = np.load(join(feature_path, f), allow_pickle=True).item()

        vad1 = feat["vad"][0]
        vad2 = feat["vad"][1]

        # choose an arbitrary vector vad1
        # multiply vector with 2 -> zeros and 2
        # subtract other vad -> vector of 2, 1, 0 , -1
        # 2: only vad1 is speaking
        # 1: both are speaking
        # 0: both silent
        # -1: only vad 2 is speaking
        speaking = 2 * vad1 - vad2
        both_silent = (speaking == 0).astype(np.int)
        events[f] = {"both_silent": both_silent, "vad1": vad1, "vad2": vad2}

        for p in pauses:
            events[f][f"pause{p}"] = []

        starts, ends = find_nonzero_start_ends(both_silent)
        for s, e in zip(starts, ends):
            if s < warm_up_frames:
                print("skip start")
                continue  # skip pauses earlier than warmup time (beginning of audio)
            # diff = frames_to_time(e - s, time_step)
            diff = e - s
            if verbose:
                print("s: ", s)
                print("e: ", e)
                print("diff: ", diff)

            for v1, v2 in zip(
                vad1[s + 1 : s + max_frames], vad2[s + 1 : s + max_frames]
            ):
                if any([v1, v2]) > 0:
                    if v1 > 0:
                        turntaker = 0
                    else:
                        turntaker = 1
                    break

            for p in pauses:
                pf = time_to_frames(p, time_step)
                if diff > pf:
                    # the event is after the pause -> start frame + pause
                    # (the entire pause (e) might be longer)
                    events[f][f"pause{p}"].append((s + pf, turntaker))
                    if verbose:
                        print("p: ", p)
                        print("pf: ", pf)
                        print("diff: ", diff)
                        input()
    return events


def plot_maptask_vs_custom_events(anno_events, events):
    import matplotlib.pyplot as plt

    files = [f for f in listdir(datapath) if f.endswith(".npy")]
    f = files[110]
    s, e = 500, 1000
    plt.subplot(2, 1, 1)
    plt.plot(anno_events[f][s:e], label="maptask")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(events[f][s:e], label="custom")
    plt.legend()
    plt.show()
    plt.close("all")


def test_events(anno_events=None, custom_events=None):
    import matplotlib.pyplot as plt

    if anno_events is not None:
        events = np.load(anno_events).item()
        print("Annotation events")
    elif custom_events is not None:
        events = np.load(custom_events).item()
        print("Custom events")

    for k, v in events.items():
        for pause in v["pause0.5"]:
            pause_end = pause[0]
            turntaker = pause[1]
            fig = plt.figure()
            warm_up = time_to_frames(conf["events"]["warm_up"]) - 1
            print("turntaker: ", turntaker)
            plt.title(f"turntaker: {turntaker}")
            plt.subplot(3, 1, 1)
            plt.plot(v["vad1"][pause_end - warm_up : pause_end + 100], label="vad1")
            plt.legend()
            plt.subplot(3, 1, 2)
            plt.plot(v["vad2"][pause_end - warm_up : pause_end + 100], label="vad2")
            plt.legend()
            plt.subplot(3, 1, 3)
            plt.plot(
                v["both_silent"][pause_end - warm_up : pause_end + 100],
                label="both silent",
            )
            plt.axvline(x=warm_up, color="r")
            plt.axvline(x=warm_up - 10, color="r")
            plt.legend()
            # plt.pause(0.01)
            # input()
            plt.show()


if __name__ == "__main__":
    from turntaking.utils import read_json
    import argparse

    datapath = join(expanduser("~"), "TurnTaking/data/features")
    outpath = join(expanduser("~"), "TurnTaking/data/events")
    annotations = join(expanduser("~"), "TurnTaking/data/features_annotation")
    confpath = join(expanduser("~"), "TurnTaking/turntaking/CONFIGS.json")

    parser = argparse.ArgumentParser(description="Process data")
    parser.add_argument("--datapath", default=datapath)
    parser.add_argument("--annotations", default=annotations)
    parser.add_argument("--outpath", default=outpath)
    parser.add_argument("-c", "--config", default=confpath)
    args = parser.parse_args()

    conf = read_json(args.config)

    ans = input("Extract Features separetely? (y/n)")
    if ans.lower() == "y":
        makedirs(args.outpath)
        ans = input("Extract annotation events? (y/n)")
        if ans.lower() == "y":
            print("Extracting annotation events")
            anno_events = find_events(
                args.annotations,
                pauses=conf["events"]["pauses"],
                time_step=conf["features"]["time_step"],
                warm_up=conf["events"]["warm_up"],
                max_time=conf["features"]["vad_prediction_time"],
            )
            print("Saving events -> ", args.outpath)
            np.save(join(args.outpath, "annotation_events.npy"), anno_events)

        ans = input("Extract custom events? (y/n)")
        if ans.lower() == "y":
            print("Extracting custom events")
            events = find_events(args.datapath)
            print("Saving events -> ", args.outpath)
            np.save(join(args.outpath, "events.npy"), events)

        print("Done!")

    ans = input("Append Features? (y/n)")
    if ans.lower() == "y":
        ans = input("Extract custom events? (y/n)")
        if ans.lower() == "y":
            print("Appending custom events")
            events = load_feats_append_events(args.datapath, conf)

    # anno_ev_path = join(args.outpath, "annotation_events.npy")
    # custom_ev_path = join( args.outpath, "events.npy")
    # test_events(anno_ev_path, custom_ev_path)
