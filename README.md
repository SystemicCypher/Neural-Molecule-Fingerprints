# Neural-Molecule-Fingerprints
## An implementation of a neural molecular fingerprint algorithm
This is based off the paper: Convolutional Networks on Graphs
for Learning Molecular Fingerprints (https://arxiv.org/pdf/1509.09292.pdf).
And some implementation was based off of https://github.com/HIPS/neural-fingerprint and the links provided by them.


## (Only Significant) Directory Structure
### Papers
This folder contains various pdfs and images of papers that were used to guide the implementation of this project. The key paper is listed above.
### SRC
This folder contains the implementation (in Python 2.7) and Jupyter notebooks used to test the implementation.


## Requirements
- Python 2.7

- Keras 

- TensorFlow (for Keras backend)

- NumPy (data storage and loading)

## Implementation Details
- Prototyping Neuralfingerprints.ipynb
This imports and tests the code from data_preprocessing.py, neuralPrint.py, and model.py
- model.py
This constructs the actual neural fingerprint model in Keras.
  * Fingerprint model layer takes as input an adjacency matrix (molecule graph), a layer representation (at first the atom features alone and later the x-hop network's representation), and feature size (the dimensionality of the data). It returns the layer's fingerprint (to be merged with the other layers' fingerprints), and the new layer representation ( which is passed in to the function again for the next layer of this network.
  * Neural graph fingerprints takes in a couple hyperparameters, such as radius (how many hops is this model going to count), fingerprint length (how long the fingerprint itself will be), and feature size (the dimensionality of the data which will be passed in to the fingerprint model layer). It returns a compiled Keras model, which takes as input an input graph (adjacency matrix) and an input layer representation (the atom features), which itself returns the molecular fingerprint. 
- neuralPrint.py
This provides a couple utility functions for the use of the neural fingerprint model
  * loadData which takes in two filepaths, the first is a folder where the molecule graphs are stored (individually) and the second is where the molecule features are stored (individually). This will likely be modified in the future to allow .npz files which compress all these matrices into a single file
  * one_hot is a depricated one_hot creator that takes in a feature matrix (of atoms) and returns a one_hot version of that matrix. It shouldn't be used and keras.utils.one_hot should instead.
- data_preprocessing.py 
This file provides utility functions that construct a molecule list, adjacency matrix, atom features matrix, and a bond features matrix (the ones currently used end in "_pandas_"). The construction of these is controlled by a function, process(). That function takes as input the filepath for the atoms data, the filepath for the bonds data, the filepath for a constructed molecule list, a filepath to save the constructed data to, and a flag that selects what functions will be performed.
  * 0 - Everything
  * 1 - Create Molecule list
  * 2 - Create Unweighted Graphs
  * 3 - Create Atom Matrices
  * 4 - Create Bond Matrices
  * 5 - Do nothing
- custom_layer.py
A custom Keras layer that is supposed to implement a dense layer that can be indexed by an ego matrix, for differing weights to be used with different layers. This is currently a work in progress.
