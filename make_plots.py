import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import errno

def open_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def clean_path(path):
    if path[-1] != '/':
        path += '/'
    return path

def listdir_files(path):
    return [path + filename for filename in os.listdir(path) if os.path.isfile(path + filename)]

def main(argv):
    compiled_path = './MuscarinicReceptors_analysis/M5R_analysis/MDCompare_outputs/'
    outputs_path = './MuscarinicReceptors_analysis/M5R_analysis/MDCompare_outputs/heatmaps/'
    sns.set(color_codes = True)
    open_dir(outputs_path)

    for filename in listdir_files(compiled_path):
        file_descriptor = os.path.splitext(os.path.basename(filename))[0]
        print file_descriptor
        if file_descriptor in ['hbbb', 'wb', 'wb2', 'vdw', 'ts'] or file_descriptor[0] == '.':
            continue
        open_table = pd.read_csv(filename,index_col=0,header=0)
        # cluster = sns.clustermap(open_table, row_cluster = True, col_cluster = True)
        # plt.xticks(rotation=90)
        # plt.yticks(rotation=90)

        if open_table.empty:
            print "Warning: %s is empty, so a clustermap will not be produced for this file" % filename
            return
        try:
            cluster = sns.clustermap(open_table, row_cluster = True, col_cluster = True, figsize=(open_table.shape[1], open_table.shape[0]), annot=True)
        except ValueError:
            return
        plt.setp(cluster.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.setp(cluster.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
        plt.title(os.path.basename(filename))

        plt.savefig('%s%s.png' % (outputs_path, file_descriptor))


if __name__=='__main__':
    main(sys.argv)
