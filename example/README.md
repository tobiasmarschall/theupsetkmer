The example here is from building a colored Debruijn graph using 10 *Myxococcus xanthus* strains assembled, downloaded from NCBI FTP server.

### Constructing the GFA and colors files
Bifrost was given the 10 assemblies and a .gfa file and a .bfg_colors was outputted (the option `-c` was used to get he colors).
```
bifrost build -s files.txt -o m_xanthus -t 20 -k 31 -c
```

### Constructing the k-mer intersection counts
These two files were given to venn_diagram script with the following command:
```
./venn_diagram m_xanthus.gfa m_xanthus.bfg_colors 31 20 output.tsv
```
The 20 after the k-mer size is the number of threads.

### Making the plot
As there are too many samples and the assembly files had long names, both `-n` and `-c` options were used with `strains.txt` and `combinations.txt` respectevly. The command with the python script was:
```
./upset_plot -i output.tsv -n strains.txt -c combinations.txt -o upset_plot.png -k 31
```

