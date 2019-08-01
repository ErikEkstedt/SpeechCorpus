from subprocess import check_output


def read_txt(filename):
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            data.append(line.strip())
    return data


def write_txt(filename, data):
    """
    Argument:
        txt:    list of strings
        name:   filename
    """
    with open(filename, "w") as f:
        f.write("\n".join(data))


def get_duration_sox(fpath):
    out = (
        check_output(f"sox --i {fpath}", shell=True).decode("utf-8").strip().split("\n")
    )
    for line in out:
        if line.lower().startswith("duration"):
            l = [f for f in line.split(" ") if not f == ""]
            duration = l[2].split(":")
            hh, mm, ss = duration
            total = int(hh) * 60 * 60 + int(mm) * 60 + float(ss)
    return total


def get_sample_rate_sox(fpath):
    out = (
        check_output(f"sox --i {fpath}", shell=True).decode("utf-8").strip().split("\n")
    )
    for line in out:
        if line.lower().startswith("sample rate"):
            l = [f for f in line.split(" ") if not f == ""]
            return int(l[-1])
