# MDCompare

Example command:
```
> python mdcompare.py -i /scratch/PI/rondror/augustine/muscarinic.input -g /scratch/PI/rondror/augustine/muscarinic.csv -o /scratch/PI/rondror/augustine/MuscarinicReceptors_analysis/M5R_analysis/MDCompare_outputs/
```

Where:
-i flag corresponds to a correctly formatted input file
-g flag corresponds to a correctly formatted generic dictionary file (this command is optional if only one protein appears in the input file)
-o flag corresponds to an empty output directory

See examples directory for examples of input file and generic dictionary formatting.

TO BE UDPATED SOON!

## Dependencies

The `group_freqs.py` script depends on the python libraries `seaborn` and `pandas`. They can be installed with `pip` or `conda`:
```
pip install seaborn pandas
conda install seaborn pandas  # Dont run both
```
