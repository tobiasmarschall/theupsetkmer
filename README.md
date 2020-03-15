# theupsetkmer
Create Upset diagrams from k-mer sets. Experimental code, not yet functional.

Install Bifrost into a conda environment and compile:
```
conda create -n bifrost-dev pkg-config cmake
conda activate bifrost-dev
git clone git@github.com:pmelsted/bifrost.git
cd bifrost
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX ..
make
make install
./compile.sh
```

For the python script that makes the upset plots, you need matplotlib and [UpSetPlot](https://pypi.org/project/UpSetPlot/) to be installed.
You can do that after the previous steps using the following
```
pip install matplotlib
pip install UpSetPlot
```
I tested with both Python 2 and 3 and it seems to work.

## Using the python script
The following options are available
```
usage: upset_plots.py [-h] [-i INPUT_FILE] [-n NAMES_LIST] [-k K]
                      [-c COMBINATIONS] [-r] [-o OUTPUT]

make upset plots from k-mer content

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        The stats file outputted by venn_diagram
  -n NAMES_LIST, --names_list NAMES_LIST
                        sample names in the same order as classes in
                        input_file. Otherwise, full names will be used in the
                        plot
  -k K, --kmer_size K   K value of as an integer (optional: used for plot
                        title)
  -c COMBINATIONS, --combinations COMBINATIONS
                        combinations to plot (otherwise all). Each combination
                        in a line in the same format as --input_file
  -r, --remove_zeros    If given, the combinations with zero interaction will
                        be disregarded
  -o OUTPUT, --output_png OUTPUT
                        output plot file name
```

It takes the output of venn_diagram which will be a tab separated text file, with rows starting with color which will give the color id and the sample or file it came from when Bifrost was ran. And rows starting with rows, then the combinations separated by a dash "-" followed by an integer with the number of k-mers present in that combination. Example:
```
color	0	sample_1_genome.fasta
color	1	sample_2_genome.fasta
color	3	sample_3_genome.fasta
combination 	0	50
combination 	1	40
combination 	2	70
combination 	0-1	10
combination 	0-2 13
combination 	1-2	20
combination 	0-2-3	100
```
### Giving sample names
The option `-n, --names_list` is used in case you want to substitute the usage of the full sample file name in the plot to only the sample name, as Bifrost will output the original files' name. Example of the names list is a text file with:
```
sample_1
sample_2
sample_3
```
Make sure the order here matches the order in the input file.

### Giving certain combinations
In case you had many samples (e.g. pangenome of some bacteria species with many strains), it's unfeasable to plot all possible combinations, as it will be 2 to the power of number of samples. The combinations list file is just a text file with combinations similar to the first input file with a combination per line. Example:
```
0
1
2
0-1-2
```
This will only plot 4 combinations out of the original 7.
Make sure the combinations here are valid according to the first input file (dash separated and the sample ids are the same).

### Removing zero intersection
In case there weren't many combinations, or there were many but most of them have a k-mer intersection of 0, the `-r, --remove_zeros` can be used, and combinations with intersection 0 will be thrown out.
