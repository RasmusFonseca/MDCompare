"""
gen_freqs determines the frequencies of residue pair contacts in 
molecular dynamics simulations. Given one or more MDContact outputs,
this script determines the frequency of each unique interaction of the
form (itype, residue 1, residue2), weighted by number of frames,
across all inputs.

The inputs are one or more MDContact output file paths as well as an
output path. The user may also specify a subset of interaction types
to compute frequencies for. The user may additionally provide a label
file to convert residue labelings into a generic nomeclature.

The output is a single tsv file comparing (itype, residue1, residue2)
instances (rows) to their corresponding frequencies.

Sample input:
$ python gen_freqs.py output_path.tsv input_path1.tsv [input_path2.tsv
[input_path3.tsv [...]]] -label label.csv -hb -sb -vdw
"""

from __future__ import division
from utils.utils import *
import json
import sys
import argparse

def get_res(atom):
    return ':'.join(atom.split(':')[1:3])

def gen_freqs(input_files, itype_subset=('hbbb', 'hbsb', 'hbss', 'sb',
    'pc', 'ps', 'ts', 'vdw', 'wb', 'wb2', 'hlb'), label=None):
    data = {'total_frames':0, 'itypes':{}}
    for itype in itype_subset:
        data['itypes'][itype] = {'contacts':{}}

    for input_file in input_files:
        seen_contacts = set()
        input_matrix = parse_matrix(input_file)
        header_line = input_matrix[0][0].split()
        num_frames_token = header_line[1]
        num_frames = int(num_frames_token.split(':')[1])
        data['total_frames'] += num_frames
        for input_line in input_matrix[2:]:
            frame = input_line[0]
            itype = input_line[1]
            atoms = input_line[2:]
            contact = tuple([get_res(atom) for atom in atoms])

            if itype not in itype_subset or (frame, contact) in seen_contacts:
                continue

            seen_contacts.add((frame, contact))

            if contact in data['itypes'][itype]['contacts']:
                data['itypes'][itype]['contacts'][contact] += 1
            else:
                data['itypes'][itype]['contacts'][contact] = 1

    return data

def main(args):
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('output_file',
                        nargs=1,
                        help="Path to gen_freqs output")
    parser.add_argument('input_files',
                        nargs='+',
                        help="Path to one or more MDContact outputs")
    parser.add_argument('--label', dest='label_file', nargs='?',
                        help="A correctly formatted label file for standardizing residue names between different proteins")

    # Adapted from MDContactNetworks (https://github.com/akma327/MDContactNetworks)
    class ITypeAction(argparse.Action):
        def __call__(self, parser, ns, values, option):
            if self.dest == "all":
                ns.itypes = set([])
            if not hasattr(ns, "itypes"):
                ns.itypes = set()
            ns.itypes.add(self.dest)
    parser.add_argument('--salt-bridge', '-sb', dest='sb', action=ITypeAction, nargs=0, help="Compute salt bridge interactions")
    parser.add_argument('--pi-cation', '-pc', dest='pc', action=ITypeAction, nargs=0, help="Compute pi-cation interactions")
    parser.add_argument('--pi-stacking', '-ps', dest='ps', action=ITypeAction, nargs=0, help="Compute pi-stacking interactions")
    parser.add_argument('--t-stacking', '-ts', dest='ts', action=ITypeAction, nargs=0, help="Compute t-stacking interactions")
    parser.add_argument('--vanderwaals', '-vdw', dest='vdw', action=ITypeAction, nargs=0, help="Compute van der Waals interactions (warning: there will be many)")
    parser.add_argument('--hbond-backbone-backbone', '-hbbb', dest='hbbb', action=ITypeAction, nargs=0, help="Compute hydrogen bond backbone backbone interactions")
    parser.add_argument('--hbond-backbone-sidechain', '-hbsb', dest='hbsb', action=ITypeAction, nargs=0, help="Compute hydrogen bond backbone sidechain interactions")
    parser.add_argument('--hbond-sidechain-sidechain', '-hbss', dest='hbss', action=ITypeAction, nargs=0, help="Compute hydrogen bond sidechain sidechain interactions")
    parser.add_argument('--ligand-hbond', '-lhb', dest='lhb', action=ITypeAction, nargs=0, help="Compute ligand hydrogen bond interactions")
    parser.add_argument('--all-interactions', '-all', dest='all', action='store_true', help="Compute all types of interactions")

    results, unknown = parser.parse_known_args()

    # Get itypes from command line
    if results.all:
        itypes = ["sb", "pc", "ps", "ts", "vdw", "hbss", "lhb", 'hbsb', 'hbbb']
    elif not hasattr(results, "itypes"):
        print("Error: at least one interaction type or '--all-interactions' is required")
        exit(1)
    else:
        itypes = results.itypes

    output_file = results.output_file[0]
    input_files = results.input_files
    label = None
    if results.label_file is not None:
        label = results.label_file[0]

    data = gen_freqs(input_files, itypes, label)

    with open(output_file, 'w+') as w_open:
        w_open.write('#\ttotal_frames:%d\tinteraction_types:%s\n' % (data['total_frames'], ','.join(itypes)))
        w_open.write('#\tColumns:\titype\tresidue_1,\tresidue_2[,\tresidue_3[,\tresidue_4]\tnum_frames\n')
        for itype in data['itypes']:
            for contact in data['itypes'][itype]['contacts']:
                w_open.write('%s\n' % '\t'.join([itype] + list(contact) + [str(data['itypes'][itype]['contacts'][contact])]))

if __name__ == '__main__':
    main(sys.argv)
