# Here the neural fingerprint algorithm is implemented (algorithm 2)
import numpy as np
import tensorflow as tf


def loadData(molecule_fpath, features_fpath):
    listm = open(molecule_fpath, "r")
    
    graphs = {}
    atoms = {}
    counts = {}
    #bonds = {}
    
    moleculeList = []
    
    for molecule in listm:
        molID = molecule.split()[0]
        number = int(molecule.split()[1])
        ligOrDec = molecule.split()[2]

        #moleculeList.append(molID + "_l")
        #moleculeList.append(molID + "_d") 
        
        if ligOrDec == "1":
            moleculeList.append(molID + "_l")
            graphs[molID + "_l"] = np.load(features_fpath + molID + "_graph_ligand.npy")
            atoms[molID + "_l"] = np.load(features_fpath + molID + "_atoms_ligand.npy")
            #bonds[molID + "_l"] = np.load(features_fpath + molID + "_bonds_ligand.npy")
            counts[molID + "_l"] = number
        else:
            moleculeList.append(molID + "_d") 
            graphs[molID + "_d"] = np.load(features_fpath + molID + "_graph_decoy.npy")      
            atoms[molID + "_d"] = np.load(features_fpath + molID + "_atoms_decoy.npy")
            #bonds[molID + "_d"] = np.load(features_fpath + molID + "_bonds_decoy.npy")
            counts[molID + "_d"] = number
    return atoms, graphs, counts, moleculeList

def one_hot(molecule_atoms_features):
    '''
    Order for this one hot is in order of atomic number
    so, hydrogen, carbon, nitrogen, oxygen
    '''
    encoding = {
        "H" : [0,0,0,0,1],
        "C" : [0,0,0,1,0],
        "N" : [0,0,1,0,0],
        "O" : [0,1,0,0,0],
        "S" : [1,0,0,0,0]
    }
    oneHot = []
    for atoms in np.nditer(molecule_atoms_features):
        atom = str(atoms)
        if atom.find("H") != -1:
            oneHot.append(encoding["H"])
        elif atom.find("C") != -1:
            oneHot.append(encoding["C"])
        elif atom.find("N") != -1:
            oneHot.append(encoding["N"])
        elif atom.find("O") != -1:
            oneHot.append(encoding["O"])
        elif atom.find("S") != -1:
            oneHot.append(encoding["S"])

    oneHot = np.array(oneHot)
    return oneHot

    
