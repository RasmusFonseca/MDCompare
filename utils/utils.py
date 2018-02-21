from __future__ import division
import os
import errno


def parse_matrix(filename, delimiter='\t'):
    with open(filename, 'r') as r_open:
        file_lines = [line.strip().split(delimiter) for line in
            r_open.readlines() if len(line.strip()) > 0]
    return file_lines


def clean_path(path):
    if path[-1] != '/':
        path += '/'
    return path


def get_file_descriptor(full_filename):
    return os.path.splitext(os.path.basename(full_filename))[0]


def open_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def listdir_files(path):
    all_files = [path + filename for filename in os.listdir(path) if os.path.isfile(path + filename)]
    for filex in all_files:
        if os.path.basename(filex)[0] == '.':
            all_files.remove(filex)
    return all_files


def listdir_dirs(path):
    return [clean_path(path + dirname) for dirname in os.listdir(path) if os.path.isdir(path + dirname)]
