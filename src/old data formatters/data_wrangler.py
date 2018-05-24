# Fun data wrangling

# This program gets the data from the data files
# and splits them into individual molecule files 
# molID_atom and molID_bond

# This data will feed into a data formatter that will
# format the data proper

import os

print "The NeuralGraph Data Formatter version 0.01\n-------------------------------"
prompted = raw_input("Atoms or bonds?\n")
data = open("../data/" + prompted + "d_dud.txt", "r")
moleculeList = open("../formatted_data/moleculeidlist.txt", "w")
moleculesInMolecList = []

counter = 0
justOpened = True

for line in data:
    #molcData = line.split()
    #if molcData[2] not in moleculesInMolecList:
    #    if justOpened:
    #        justOpened = False
    #    else:
    #        molecularData.close()

    #    moleculeList.write(molcData[2] + "\n")
    #    moleculesInMolecList.append(molcData[2])
    #    molecularData = open("../formatted_data/"+ molcData[2] + "_"+ prompted + ".txt", "w")
    #    molecularData.write(line)
    #else:
    #    molecularData.write(line)







    if counter == 0:
        moleculeID = line.split()[2]
        moleculeList.write(moleculeID + "\n")
        molecularData = open("../formatted_data/"+ moleculeID + "_"+ prompted + ".txt", "w")
        counter += 1
    
    if line.split()[2] == moleculeID:
        molecularData.write(line)
    else:
        molecularData.close()
        moleculeID = line.split()[2]
        counter += 1
        moleculeList.write(moleculeID + "\n")
        molecularData = open("../formatted_data/"+ moleculeID + "_"+ prompted + ".txt", "w")

moleculeList.close()    
data.close()