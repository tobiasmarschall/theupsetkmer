#!/usr/bin/python3
import sys
import os
import argparse
import itertools
import matplotlib.pyplot as plt
import upsetplot
import pdb

parser = argparse.ArgumentParser(description='make upset plots from k-mer content')

parser.add_argument("-i", "--input_file", dest="input_file", default=None,
                    type=str, help="The stats file outputted by venn_diagram")

parser.add_argument("-n", "--names_list", dest="names_list", default=None, type=str,
                    help="sample names in the same order as classes in input_file. Otherwise, full names will be used in the plot")

parser.add_argument("-k", "--kmer_size", dest="kmer_size", metavar="K", default=0,
                    type=int, help="K value of as an integer (optional: used for plot title)")

parser.add_argument("-c", "--combinations", dest="combinations", default=None, type=str,
                    help="combinations to plot (otherwise all). Each combination in a line in the same format as --input_file")

parser.add_argument("-r", "--remove_zeros", dest="no_zeros", action="store_true",
                    help="If given, the combinations with zero interaction will be disregarded")

parser.add_argument("-o", "--output_png", dest="output", default="output.png",
                    type=str, help="output plot file name")

args = parser.parse_args()


def all_combinations(samples_list):
    """
    returns all combinations in the list given
    """
    iterable = itertools.chain.from_iterable(itertools.combinations(samples_list, r) for r in range(len(samples_list) + 1))
    combinations = []
    for i in iterable:
        combinations.append(list(i))
    return combinations[1:]  # getting rid of the null set at first


def make_combination_list(colors, combinations):
    """
    returns a list of list with combinations

    """
    comb_list = []
    for key in combinations.keys():
        comb_list.append([colors[int(x)] for x in key.split("-")])

    return comb_list

def parse_venn_output(input_path):
    """
    parses the output from the cpp tool
    """

    if not os.path.exists(input_path):
        print("The file {} does not exist".format(input_path))
        sys.exti()

    colors = dict()
    combinations = dict()

    with open(input_path, "r") as in_file:
        for line in in_file:
            if line:
                line = line.strip().split()
                if line[0] == "color":
                    colors[int(line[1])] = line[2]
                else:
                    combinations[line[1]] = int(line[2])

    return colors, combinations


def read_list(file_path):
    """
    reads the sample names or combinations
    """
    if not os.path.exists(file_path):
        print("File {} does not exist".format(file_path))
        sys.exit()

    items = []
    with open(file_path, "r") as in_file:
        for line in in_file:
            items.append(line.strip())

    return items


if __name__ == "__main__":

    if args.input_file is None:
        print("ERROR! You need to give the input file -n, --input_file\n")
        parser.print_help()
        sys.exit()

    # reading colors and combinations
    colors, combinations = parse_venn_output(args.input_file)

    if args.names_list is not None:
        """
        This can be needed when the file names were too long
        As bifrost reports the colors back with the respective file names
        The upset plot will look too ugly (and sometimes not rendered correctly)
        whcn using too long sample names
        So an extra file with sample names is neater
        """
        sample_names = read_list(args.names_list)
        # in theory this should be ordered the same as the colors
        # so I will keep this hacky assumption
        for k in colors.keys():
            try:
                colors[k] = sample_names[int(k)]
            except IndexError:
                print("The list of samples provided in {} does not have the same numbers as classes in {}".format(args.names_list, args.input_file))


    if args.combinations is not None:
        """
        Bifrost will return all possible combinations which is fine
        for 5 to 6 samples, but we have a 2^n_samples combinations
        So if there are many samples together, it's better to choose
        the combinations that you'd like to visualize, otherwise it will crash
        The plot won't work
        """
        user_comb = read_list(args.combinations)
        tmp = dict()
        # I am also assuming that 
        for c in user_comb:
            try:
                tmp[c] = combinations[c]
            except KeyError:
                print("the combination {} does not exist in {}".format(c, args.input_file))
        combinations = tmp

    if args.no_zeros:
        """
        If there are many combinations but most of them are zero
        You can remove them easily instead of providing combinatiosn
        """
        keys = list(combinations.keys())
        for k in keys:
            if combinations[k] == 0:
                del combinations[k]


    """
    The idea is that upset plot will take two input
    a list of lists with combinations of sample names
    e.g. [["s1"], ["s2"], ["s1", "s2"]]
    which I will be constructing here from the ["0", "1", "1-2"]

    then takes the corrisponding values for these combinations
    e.g. [50, 40, 100]
    this means that sample 1 has 50 uniue items, s2 has 40 and the intersection is 10
    """
    combinations_list = make_combination_list(colors, combinations)

    # all_sets = return_subsets(labels, samples)
    tf_frame = upsetplot.from_memberships(combinations_list, data=list(combinations.values()))
    upsetplot.plot(tf_frame, sort_by="cardinality")
    current_figure = plt.gcf()

    if args.kmer_size is not None:
        title = "K-mers of {} samples with k-mer size of {}".format(len(colors), args.kmer_size)
    else:
        title = "K-mers of {} samples".format(len(colors))

    if len(combinations) <= 25:
        font_size = "15"
    else:
        font_size = "20"

    plt.title(title, loc='left', fontsize=font_size)
    current_figure.savefig(args.output, dpi=400)
