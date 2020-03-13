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
