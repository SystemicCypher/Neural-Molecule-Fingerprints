import data_preprocessing as proc
import neuralPrint as neural
import numpy as np
import model as n
from keras.models import Model

#proc.process("../data/atomsd_dud.txt", "../data/bondsd_dud.txt", "", "../formatted_data/moleculelist.txt", "../formatted_data/features/", 2)
all_molecule_atoms_raw_features, all_adj_graphs, all_atom_counts, moleculelist = neural.loadData("../formatted_data/moleculelist.txt", "../formatted_data/features/")
fingerprinter = n.neural_graph_fingerprints(6, 50, 0)
atom_f = neural.one_hot(all_molecule_atoms_raw_features["ZINC01535869"])
adj_graph = all_adj_graphs["ZINC01535869"]
adj_graph = np.eye(adj_graph.shape[0]) + adj_graph
x = fingerprinter.predict([adj_graph, atom_f])
print x
