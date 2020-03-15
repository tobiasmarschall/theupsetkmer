#include <iostream>
#include <fstream>
#include <bifrost/ColoredCDBG.hpp>

using namespace std;

int main(int argc, char *argv[])
{
	if (argc < 6){

		cout << "Usage: ./venn_classes <graph_file.gfa> <color_file.bfg_colors> <k> <threads> <output_file.txt>" << endl;
	}
	else {

		ColoredCDBG<> ccdbg(atoi(argv[3]));

		ccdbg.read(string(argv[1]), string(argv[2]), atoi(argv[4]), true);

		size_t nb_unitigs = 0;

		const size_t nb_colors = ccdbg.getNbColors(); // Get number of colors
		const size_t nb_classes = pow(2, nb_colors); // Get number of color classes for venn diagram

		cout << "Number of color classes is " << nb_classes << endl;

		vector<size_t> count_classes(nb_classes + 1, 0); // Create a counter (init. to 0) for each class

		for (const auto& um : ccdbg){ // Iterate over unitigs of the graph

			vector<Roaring> nb_colors_per_km(um.len); // Create a vector of color id containers (Roaring) for each kmer position

			const UnitigColors* cs = um.getData()->getUnitigColors(um); // Get color container of unitig

			UnitigColors::const_iterator it_s = cs->begin(um); // Start iterator of color container
			UnitigColors::const_iterator it_e = cs->end(); // End iterator of color container

			while (it_s != it_e){ // Iterate over each <k-mer position, color ID> in color container

				nb_colors_per_km[it_s.getKmerPosition()].add(it_s.getColorID()); // Add color ID to container for kmer position

				++it_s;
			}

			for (const auto& r : nb_colors_per_km){ // For each kmer position in unitig, get associated color ids

				size_t idx = 0; // Create index of the color class (assume 64 colors max) 

				for (const auto id : r) idx |= (0x1ULL << id);

				count_classes[idx] += 1; // Increment count of that class
			}

			++nb_unitigs;

			if (nb_unitigs%1000 == 0) cout << "Processed " << nb_unitigs << " unitigs." << endl;
		}

		// Display colors
		const vector<string> colors_names = ccdbg.getColorNames();

		// outputting results to a file
		ofstream output_file;
		output_file.open(argv[5]);

		// cout << endl << "=== COLOR NAMES === " << endl << endl;
		for (size_t i = 0; i < colors_names.size(); ++i){
			output_file << "color\t" << i << "\t" << colors_names[i] << endl;
		}

		// Display number of kmers for each color class
		// cout << endl << "=== COLOR CLASSES COUNTS === " << endl << endl;

		for (size_t idx = 1; idx < nb_classes; ++idx){
			output_file << "combination\t";
			int counter = 0;
			for (size_t i = 0; i < nb_colors; ++i){

				if (static_cast<bool>(idx & (0x1ULL << i))){
					if (counter == 0){
						output_file << i;
					} else {
						output_file << "-" << i;
					}
					counter += 1;
				}
			}

			output_file << "\t" << count_classes[idx] << endl;
		}
		output_file.close();
		return 0;
	}
}
