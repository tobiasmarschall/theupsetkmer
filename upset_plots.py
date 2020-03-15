import sys
import os
import argparse
import subprocess
import itertools
import matplotlib.pyplot as plt
import upsetplot

parser = argparse.ArgumentParser(description='make upset plots from k-mer content')

parser.add_argument("-f", "--files_list", dest="files_list", default=None,
                    type=str, help="input file of files path")

parser.add_argument("-n", "--names_list", dest="names_list", default=None, type=str,
                    help="same as names but in a file, each name in a line")

parser.add_argument("-t", "--thread", dest="threads", default=1, type=int,
                    help="number of threads to use for calculating the k-mers")

parser.add_argument("-k", "--k_mer", dest="k_mer", metavar="K", default=0,
                    type=int, help="K value of as an integer")

parser.add_argument("-c", "--combinations", dest="combinations", default=None, type=str,
                    help="file with combinations, combinatino per line with sample names comma separated (default is all possible combinations")

parser.add_argument("-o", "--output_png", dest="output", default="output.png",
                    type=str, help="output plot file name")

args = parser.parse_args()


def all_combinations(samples_list):
    """
    returns all combinations in the list given

    :param samples_list: a list of sample names
    :return: list of lists of combinations
    """
    iterable = itertools.chain.from_iterable(itertools.combinations(samples_list, r) for r in range(len(samples_list) + 1))
    combinations = []
    for i in iterable:
        combinations.append(list(i))
    return combinations[1:]  # getting rid of the null set at first


def parse_venn_output(output_path):
    """
    parses the output from the cpp tool

    :param output_path: the file with the intersection information path
    """

    pass

if __name == "__main__":
    # I need to take the inputs and turn them into a command
    bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    # then run the command as a subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # I need then to parse the output file and build the plot
    # shouldn't be too hard