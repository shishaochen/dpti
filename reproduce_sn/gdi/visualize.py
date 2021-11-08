import argparse
import os

from collections import namedtuple
from matplotlib import pyplot


CurveRecord = namedtuple('CurveRecord', ['temperature', 'pressure'])


def load_lcurve_file(path):
    with open(path, 'r') as fin:
        lines = fin.readlines()
    lcurve = []
    for item in lines:
        line = item.strip()
        if not line or line.startswith('#'):
            continue
        fields = line.split()
        one = CurveRecord(
            temperature=float(fields[0]),
            pressure=float(fields[1])/1e4
        )
        lcurve.append(one)
    return lcurve


def draw_one_line(path, mark):
    name = os.path.basename(path).split('.', 1)[0]
    lcurve = load_lcurve_file(path)
    p_vals = []
    t_vals = []
    for idx in range(0, len(lcurve)):
        item = lcurve[idx]
        p_vals.append(item.pressure)
        t_vals.append(item.temperature)
    pyplot.plot(p_vals, t_vals, mark, label=name)
    pv = p_vals[0]
    tv = t_vals[0]
    pyplot.text(pv, tv, '%.1f' % tv)


def run(FLAGS):
    pyplot.figure(figsize=(6,10))
    pyplot.title('Phase diagram of Sn')
    pyplot.xlabel('Pressure (GPa)')
    pyplot.ylabel('Temperature (K)')
    pyplot.xlim(left=0., right=30.)
    pyplot.ylim(bottom=0., top=2000.)

    mark_list = ['-gD', '-bo', '-rv']
    for idx, path in enumerate(FLAGS.input_path.split(',')):
        draw_one_line(path, mark_list[idx])
    pyplot.legend()
    pyplot.grid()

    output_path = FLAGS.output_path
    if os.path.isfile(output_path):
        os.remove(output_path)
    pyplot.savefig(output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Draw lines from a lcurve file.')
    parser.add_argument('-i', '--input_path', default='pb.out', help='Where to read boundary.')
    parser.add_argument('-o', '--output_path', default='phase_diagram.png', help='Where to write image.')
    FLAGS = parser.parse_args()
    run(FLAGS)