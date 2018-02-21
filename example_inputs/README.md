# Example of comparing trajectories

The files `smalltrj1_interactions.tsv` and `smalltrj2_interactions.tsv` represent two simulations of the same molecule. 

To compute the average residue frequency across both simulations (for instance if they represented multiple runs of the same condition), run
```bash
../gen_freqs.py --input_files smalltrj?_interactions.tsv \
                --labels smalltrj_labels.tsv \
                -all \
                --output_file bothtrj_frequencies.tsv
```
The output-file will contain
```
#	total_frames:6	interaction_types:sb,pc,ps,ts,vdw,hbss,lhb,hbsb,hbbb
#	Columns:	residue_1,	residue_2	frame_count	contact_frequency
A1	C3	6	1.000
A1	M2	4	0.667
C3	M2	1	0.167
```

