import matplotlib
import numpy as np
import os
import sys

moleculeList = open("../formatted_data/numberedmoleculeidlist.txt", 'r')

for molLine in moleculeList:
    #print molLine
    name2 = molLine.split()[0]
    count = int(molLine.split()[1])
    count += 1
    #print name2 + molLine.split()[1]
    b = open("../formatted_data/"+ name2 +"_bonds.txt", 'r')
    unweightGraph = [[False for x in range(count)] for y in range(count)]

    for line in b:
        atom1 = line.split()[3]
        atom2 = line.split()[4]
        #print name2 + ":: atom 1: " + atom1 + "  atom 2: " + atom2 
        unweightGraph[int(atom1)][int(atom2)] = True
        unweightGraph[int(atom2)][int(atom1)] = True

    b.close()
    adjMatrix = np.array(unweightGraph)
    filepth = "../formatted_data/features/" + name2
    np.save(filepth, adjMatrix)


'''
    molGraph = open("../formatted_data/features/" + name2 + "_graph.txt", 'w')

    molGraph.write("   ")
    for i in range(1,count):
        if (i < 10):
            molGraph.write(str(i) + "  ")
        else:
            molGraph.write(str(i) + " ")

    molGraph.write("\n")

    for i in range(1,count):
        if (i < 10):
            molGraph.write(str(i) + "  ")
        else:
            molGraph.write(str(i) + " ")
        for j in range(1,count):
            if(unweightGraph[i][j]):
                molGraph.write("T  ")
            else:
                molGraph.write("F  ")
            if(j == count-1):
                molGraph.write("\n")
    molGraph.close()
'''