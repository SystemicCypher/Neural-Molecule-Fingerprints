import data_preprocessing as proc
import neuralPrint as neural

proc.process("../data/atomsd_dud.txt", "../data/bondsd_dud.txt", "", "../formatted_data/moleculelist.txt", "../formatted_data/features/", 2)
#all_molecule_atoms_raw_features, all_molecule_bonds_raw_features, all_adj_graphs, all_atom_counts, moleculelist = neural.loadData("../formatted_data/moleculelist.txt", "../formatted_data/features/")

