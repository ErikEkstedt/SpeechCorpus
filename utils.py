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
