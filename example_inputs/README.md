# Example of comparing trajectories

The files `smalltrj1_interactions.tsv` and `smalltrj2_interactions.tsv` represent two simulations of the same molecule. 

To compute the average residue frequency across both simulations (for instance if they represented multiple runs of the same condition), run
```bash
../gen_freqs.py --input_files smalltrj?_interactions.tsv \
                --labels smalltrj_labels.tsv \
                -all \
                --output_file bothtrj_frequencies.tsv
```

To compare residue interaction frequencies between the two trajectories, run
```bash
../gen_freqs.py --input_files smalltrj1_interactions.tsv \
                --labels smalltrj_labels.tsv \
                -all \
                --output_file smalltrj1_resfreqs.tsv

../gen_freqs.py --input_files smalltrj2_interactions.tsv \
                --labels smalltrj_labels.tsv \
                -all \
                --output_file smalltrj2_resfreqs.tsv

../group_freqs.py --input_frequencies smalltrj1_resfreqs.tsv smalltrj2_resfreqs.tsv \
                  --table_output smalltrj_comparefreqs.tsv \
                  --plot_output smalltrj_comparefreqs.png
```
and then inspect the two output-files with a system viewer. If no `--plot_output` is specified the fingerprint heatmap will show up on screen.
