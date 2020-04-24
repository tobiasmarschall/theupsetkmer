#!/bin/bash

PREFIX=$CONDA_PREFIX

g++ -fexceptions -O3 -std=c++11 -march=native -Wno-c++98-compat -I $PREFIX/include -c venn_diagram.cpp -o venn_diagram.o
g++ -o venn_diagram venn_diagram.o -s -O3 -lbifrost -pthread -lz -L $PREFIX/lib -Wl,-rpath,$PREFIX/lib

