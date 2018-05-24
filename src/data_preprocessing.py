# Preprocessing data utils
import numpy as np
import pandas as p



def process(atoms_fpath, bonds_fpath, dist_fpath, molecList_fpath, save_fpath, flag):
    if flag == 0 or flag == 1:
        create_molecule_list(atoms_fpath, molecList_fpath)
        print "Molecule list created..."
    if flag == 0 or flag == 2:
        #create_unweighted_graphs(molecList_fpath, bonds_fpath, save_fpath, "1")
        #create_unweighted_graphs(molecList_fpath, bonds_fpath, save_fpath, "0")
        create_unweighted_graphs_panda(molecList_fpath, bonds_fpath, atoms_fpath, save_fpath)
        print "Unweighted graphs created..."
    if flag == 0 or flag == 3:
        #create_atoms_arrays(atoms_fpath, molecList_fpath, save_fpath, "1")
        #create_atoms_arrays(atoms_fpath, molecList_fpath, save_fpath, "0")
        create_atoms_arrays_panda(atoms_fpath, molecList_fpath, save_fpath)
        print "Atom arrays created..."
    if flag == 0 or flag == 4:
        #create_bonds_arrays(bonds_fpath, molecList_fpath, save_fpath, "1")
        #create_bonds_arrays(bonds_fpath, molecList_fpath, save_fpath, "0")
        create_bonds_arrays_panda(atoms_fpath, bonds_fpath, molecList_fpath, save_fpath)
        print "Bonds arrays created..."
    if flag == 1 or flag == 2 or flag == 3 or flag == 4 or flag == 0:
        print "Done preprocessing!"
    if flag < 0 or flag > 4:
        print "No preprocessing done!"

def create_molecule_list(data_fpath, molecList_fpath):
    # Creates molecule list
    moleculeList = open(molecList_fpath, "w")
    # Opens data file (likely atoms)
    data = open(data_fpath, "r")

    previousLine = ""

    for line in data:
        # Gets the molecule ID
        moleculeID = line.split()[2]
        if previousLine == "":
            pass
        # If the molecule ID doesn't match the previous line's 
        # time to write the molecule ID, final atom number (the size), and the decoy/ligand status
        elif moleculeID != previousLine.split()[2]:
            moleculeList.write(previousLine.split()[2] + " " + previousLine.split()[4] + " " + previousLine.split()[1] + "\n")
        
        previousLine = line
    # Writes the very last line
    moleculeList.write(previousLine.split()[2] + " " + previousLine.split()[4] + " " + previousLine.split()[1] + "\n")
    data.close()
    moleculeList.close()


def create_unweighted_graphs(molecList_fpath, bonds_fpath, save_fpath, decoy_or_ligand_flag):
    # Opens the molecule list and the bonds data
    moleculeList = open(molecList_fpath, "r")
    bonds = open(bonds_fpath, "r")

    # Initialization of two dictionaries
    # Molecules will be indexed by moleculeID and 
    # have an adjacency matrix as its value
    molecules = {}
    # Counts will be indexed by moleculeID and
    # have the number of atoms in the molecule
    # as the value
    counts = {}

  
    for line in moleculeList:
        # If the flag matches the type we're looking for
        # do what needs to be done. Otherwise,
        # loop until you run into it.
        if line.split()[2] == decoy_or_ligand_flag:
            pass
        else:
            continue


        count = int(line.split()[1])
        if line.split()[2] == "1":
            molecules[line.split()[0] + "_l"] = [[False for x in range(count)] for y in range(count)] # pylint: disable=unused-variable
            counts[line.split()[0] + "_l"] = line.split()[1]
        else:
            molecules[line.split()[0] + "_d"] = [[False for x in range(count)] for y in range(count)] # pylint: disable=unused-variable
            counts[line.split()[0] + "_d"] = line.split()[1]
    moleculeList.close()

    for line in bonds:
        if line.split()[1] == decoy_or_ligand_flag:
            pass
        else:
            continue

        moleculeID = line.split()[2]
        if decoy_or_ligand_flag == "1":
            moleculeID += "_l"
        else:
            moleculeID += "_d"
        atom1 = int(line.split()[3])
        atom2 = int(line.split()[4])
        atom1 -= 1
        atom2 -= 2
        molecules[moleculeID][atom1][atom2] = True
        molecules[moleculeID][atom2][atom1] = True
    bonds.close()

    for molecule, adj in molecules.iteritems():
        adjMatrix = np.array(adj)
        filepth = save_fpath + molecule[:-2] + "_graph"

        if decoy_or_ligand_flag == "1":
            filepth = filepth + "_ligand"
        else:
            filepth = filepth + "_decoy"
        
        np.save(filepth, adjMatrix)
    
def create_atoms_arrays(data_fpath, molecList_fpath, save_fpath, decoy_or_ligand_flag):
    data = open(data_fpath, "r")
    moList = open(molecList_fpath, "r")

    molecules = {}
    count = {}
    for mol in moList:
        if mol.split()[2] == decoy_or_ligand_flag:
            pass
        else:
            continue

        if mol.split()[2] == "1":
            molecules[mol.split()[0] + "_l"] = []
            count[mol.split()[0] + "_l"] = int(mol.split()[1])
        else:
            molecules[mol.split()[0] + "_d"] = []
            count[mol.split()[0] + "_d"] = int(mol.split()[1])
    moList.close()


    counter = 0
    prevID = ""
    for line in data:
        if line.split()[1] == decoy_or_ligand_flag:
            pass
        else:
            continue
        
        conformer = line.split()[3]
        molID = line.split()[2]
        if decoy_or_ligand_flag == "1":
            molID += "_l"
        else:
            molID += "_d"
        atom = line.split()[8]

        if conformer == "1" and counter < count[molID]:
            molecules[molID].append(atom)
            prevID = molID
            counter += 1
        if conformer == "1" and molID != prevID:
            molecules[molID].append(atom)
            prevID = molID
            counter = 1
    
    for mol, atomarr in molecules.iteritems():
        arrayAt = np.array([atomarr])
        filepth = save_fpath + mol[:-2] + "_atoms"
        if decoy_or_ligand_flag == "1":
            filepth = filepth + "_ligand"
        else:
            filepth = filepth + "_decoy"
        np.save(filepth, arrayAt)
        
def create_bonds_arrays(data_fpath, molecList_fpath, save_fpath, decoy_or_ligand_flag):
    data = open(data_fpath, "r")
    moList = open(molecList_fpath, "r")

    molecules = {}
    for mol in moList:
        if mol.split()[2] == decoy_or_ligand_flag:
            pass
        else:
            continue
        
        if decoy_or_ligand_flag == "1":
            molecules[mol.split()[0] + "_l"] = []
        else:
            molecules[mol.split()[0] + "_d"] = []
    moList.close()
    
    for line in data:
        if line.split()[1] == decoy_or_ligand_flag:
            pass
        else:
            continue
        
        molID = line.split()[2]
        if decoy_or_ligand_flag == "1":
            molID += "_l"
        else:
            molID += "_d"

        bondType = line.split()[5]
        molecules[molID].append(bondType)
    
    for mol, bonds in molecules.iteritems():
        arrBond = np.array([bonds])
        filepth = save_fpath + mol[:-2] + "_bonds"
        if decoy_or_ligand_flag == "1":
            filepth = filepth + "_ligand"
        else:
            filepth = filepth + "_decoy"
        np.save(filepth, arrBond)

'''
Below are the pandas implementations of my data formatters
'''

def create_unweighted_graphs_panda(molecList_fpath, bonds_fpath, atoms_fpath, save_fpath):
    moleculeList = open(molecList_fpath, "r")
    bonds = p.read_table(bonds_fpath, engine='python', sep=r'\s', names=['tarNam', "D_L", "molID", "atom1", "atom2", "bondType"], usecols=['D_L','molID','atom1','atom2'])
    atoms = p.read_table(atoms_fpath, engine='python', sep=r'\s', names=['tarNam', 'D_L', 'molID', 'conf', 'atomNo', 'X', 'Y', 'Z', 'atomTyp'], usecols=['D_L', 'molID', 'conf', 'atomNo', 'atomTyp'])


    molecules = {}
    #counts = {}
    counter = 0
    lines = []
    for line in moleculeList:
        lines.append(line)
    total = len(lines)
    number_complete = 0
    '''
    for line in lines:
        molecule = line.split()[0]
        ligand = line.split()[2]
        if ligand == "1":
            count = len(bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)])
            atomCount = len(atoms[(atoms['molID'] == molecule) & (atoms['conf'] == 1) & (atoms['D_L'] == 1)])
            counts[molecule + "_l"] = (count, atomCount)
        else:
            count = len(bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)])
            atomCount = len(atoms[(atoms['molID'] == molecule) & (atoms['conf'] == 1) & (atoms['D_L'] == 0)])
            counts[molecule + "_d"] = (count, atomCount)
    '''

    for line in lines:
        molecule = line.split()[0]
        ligand = line.split()[2]
        print str(number_complete) +  " out of " + str(total)
        number_complete += 1
        if ligand == "1":
            count = len(bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)])
            atomCount = len(atoms[(atoms['molID'] == molecule) & (atoms['conf'] == 1) & (atoms['D_L'] == 1)])
            molecules[molecule + "_l"] = [[False for x in range(atomCount)] for y in range(atomCount)]
            for i in range(count):
                ind = counter + i
                atom1 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)]['atom1'][ind] - 1
                atom2 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)]['atom2'][ind] - 1
                molecules[molecule + "_l"][atom1][atom2] = True
                molecules[molecule + "_l"][atom2][atom1] = True
            counter += count
        else:
            count = len(bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)])
            atomCount = len(atoms[(atoms['molID'] == molecule) & (atoms['conf'] == 1) & (atoms['D_L'] == 0)])
            molecules[molecule + "_d"] = [[False for x in range(atomCount)] for y in range(atomCount)]
            for i in range(count):
                ind = counter + i
                atom1 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)]['atom1'][ind] - 1
                atom2 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)]['atom2'][ind] - 1
                molecules[molecule + "_d"][atom1][atom2] = True
                molecules[molecule + "_d"][atom2][atom1] = True
            counter += count
        for molecule, adj in molecules.iteritems():
            adjMatrix = np.array(adj)
            filepth = save_fpath + molecule[:-2] + "_graph"
            if molecule[-1] == "l":
                filepth = filepth + "_ligand"
            else:
                filepth = filepth + "_decoy"
            np.save(filepth, adjMatrix)

def create_atoms_arrays_panda(data_fpath, molecList_fpath, save_fpath):
    moleculeList = open(molecList_fpath, "r")
    atoms = p.read_table(data_fpath, engine='python', sep=r'\s', names=['tarNam', 'D_L', 'molID', 'conf', 'atomNo', 'X', 'Y', 'Z', 'atomTyp'], usecols=['D_L', 'molID', 'conf', 'atomNo', 'atomTyp'])

    molecules = {}
    counter = 0
    number_complete = 0.0
    lines = []
    for line in moleculeList:
        lines.append(line)
    total = float(len(lines))
    for molecule in lines:
        moleculeID = molecule.split()[0]
        ligand = molecule.split()[2]
        percent = number_complete/total * 100
        print str(percent) + "%"
        if ligand == "1":
            molecules[moleculeID + "_l"] = []
            count = len(atoms[(atoms['molID'] == moleculeID) & (atoms['conf'] == 1) & (atoms['D_L'] == 1)])
            for i in range(count):
                ind = counter + i
                atom = atoms[(atoms['molID'] == moleculeID) & (atoms['conf'] == 1) & (atoms['D_L'] == 1)]['atomTyp'][ind]
                molecules[moleculeID + "_l"].append(atom)
            counter += count
        else:
            molecules[molecule + "_d"] = []
            count = len(atoms[(atoms['molID'] == moleculeID) & (atoms['conf'] == 1) & (atoms['D_L'] == 0)])
            for i in range(count):
                ind = counter + i
                atom = atoms[(atoms['molID'] == moleculeID) & (atoms['conf'] == 1) & (atoms['D_L'] == 0)]['atomTyp'][ind]
                molecules[moleculeID + "_d"].append(atom)
            counter += count

    for mol, atomarr in molecules.iteritems():
        arrayAt = np.array([atomarr])
        filepth = save_fpath + mol[:-2] + "_atoms"

        if mol[-1] == "l":
            filepth = filepth + "_ligand"
        else:
            filepth = filepth + "_decoy"
        np.save(filepth, arrayAt)

def create_bonds_arrays_panda(atom_data_fpath, bond_data_fpath, molecList_fpath, save_fpath):
    moleculeList = open(molecList_fpath, "r")
    bonds = p.read_table(bond_data_fpath, engine='python', sep=r'\s', names=['tarNam', "D_L", "molID", "atom1", "atom2", "bondType"], usecols=['D_L','molID','atom1','atom2'])
    atoms = p.read_table(atom_data_fpath, engine='python', sep=r'\s', names=['tarNam', 'D_L', 'molID', 'conf', 'atomNo', 'X', 'Y', 'Z', 'atomTyp'], usecols=['D_L', 'molID', 'conf', 'atomNo', 'atomTyp'])

    molecules = {}
    counter = 0

    lines = []
    for line in moleculeList:
        lines.append(line)

    for line in lines:
        molecule = line.split()[0]
        ligand = line.split()[2]

        if ligand == "1":
            count = len(bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)])
            atomCount = len(atoms[(atoms['molID'] == molecule) & (atoms['conf'] == 1) & (atoms['D_L'] == 1)])
            molecules[molecule + "_l"] = [["0" for x in range(atomCount)] for y in range(atomCount)]
            for i in range(count):
                ind = counter + i
                atom1 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)]['atom1'][i] - 1
                atom2 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)]['atom2'][i] - 1
                molecules[molecule + "_l"][atom1][atom2] = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)]['bondType'][ind]
                molecules[molecule + "_l"][atom2][atom1] = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 1)]['bondType'][ind]
            counter += count
        else:
            count = len(bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)])
            atomCount = len(atoms[(atoms['molID'] == molecule) & (atoms['conf'] == 1) & (atoms['D_L'] == 0)])
            molecules[molecule + "_d"] = [["0" for x in range(atomCount)] for y in range(atomCount)]
            for i in range(count):
                ind = counter + i
                atom1 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)]['atom1'][i] - 1
                atom2 = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)]['atom2'][i] - 1
                molecules[molecule + "_d"][atom1][atom2] = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)]['bondType'][ind]
                molecules[molecule + "_d"][atom2][atom1] = bonds[(bonds['molID'] == molecule) & (bonds['D_L'] == 0)]['bondType'][counter + i]
            counter += count

        for mol, bonds in molecules.iteritems():
            arrBond = np.array([bonds])
            filepth = save_fpath + mol[:-2] + "_bonds"
            if mol[-1] == "l":
                filepth = filepth + "_ligand"
            else:
                filepth = filepth + "_decoy"
            np.save(filepth, arrBond)