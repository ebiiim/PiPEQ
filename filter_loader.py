import re


def _parse_roomeq(path):
    eq = []
    try:
        with open(path, 'r') as f:
            for l in [re.sub(' +', ' ', s).split(' ') for s in f.read().splitlines()]:
                if len(l) == 12 and l[0] == 'Filter' and l[2] == 'ON' and l[3] == 'PK' and l[4] == 'Fc':
                    eq.append([l[5], l[8], l[11]])
    except FileNotFoundError:
        pass
    return eq


def _build_eq(parser):
    sox_eq = []
    for eq in parser:
        sox_eq.append('equalizer')
        sox_eq.append(eq[0])
        sox_eq.append(eq[2] + 'q')
        sox_eq.append(eq[1])
    return sox_eq


def build_eq_by_type(eq_type, path):
    if eq_type == 'roomeq':
        return _build_eq(_parse_roomeq(path))
    return []


def format_eq_plot(eq_list):
    arg = ''
    for i in range(0, len(eq_list), 4):
        arg += ' "'+' '.join(eq_list[i:i+4]) + '"'
    return arg


if __name__ == '__main__':
    import sys
    print(format_eq_plot(build_eq_by_type(sys.argv[1], sys.argv[2])))
