import keras.layers as layers
import keras.models as models
import keras.backend as k
import keras.optimizers as optimizers
import keras.regularizers as regularizers
import custom_layer as ndense
import numpy as np
import sklearn.preprocessing as sk

def fingerprint_model_layer(molecule_graph, layer_rep, fingerprint_len, feature_size):
    
    adj_by_rep = layers.Lambda(lambda x:k.batch_dot(molecule_graph, x, axes=(2,1)))(layer_rep)
    adj_by_rep = layers.Reshape((-1, feature_size))(adj_by_rep)
    ego_size = layers.Lambda(lambda x:k.sum(x, axis=1))(molecule_graph)

    layer_rep_1 = layers.Dense(feature_size, use_bias=False)(adj_by_rep)
    layer_rep_2 = layers.Dense(feature_size, use_bias=False)(adj_by_rep)
    layer_rep_3 = layers.Dense(feature_size, use_bias=False)(adj_by_rep)
    layer_rep_4 = layers.Dense(feature_size, use_bias=False)(adj_by_rep)
    layer_rep_5 = layers.Dense(feature_size, use_bias=False)(adj_by_rep)

    #layer_rep = layers.Lambda(lambda x: k.stack(x, axis=3))([layer_rep_1, layer_rep_2, layer_rep_3, layer_rep_4, layer_rep_5])
    #ego_one_hot = layers.Lambda(lambda x: k.one_hot(x, 5))(ego_size)
    #ego_one_hot = layers.Lambda(lambda x: k.transpose(x))(ego_one_hot)
    #layer_rep = layers.Reshape((-1, feature_size))(layer_rep)
    #layer_rep = layers.Lambda(lambda x: k.batch_dot(x, ego_one_hot))(layer_rep)
    #layer_rep = layers.Lambda(lambda x: x[:,0])(layer_rep)
    #layer_rep = layers.Reshape((-1, feature_size))(layer_rep)

    layer_fp = layers.Dense(fingerprint_len, activation='softmax', use_bias = False)(layer_rep_1)
    print(layer_fp.shape)
    #layer fp should be size batch, fingerprint_len
    return layer_rep_1, layer_fp

# Might not be needed: molecule_graph, layer_rep
def neural_graph_fingerprints(radius, fingerprint_len, feature_size):
    input_graph = layers.Input(shape=(None, None))
    input_layer_rep = layers.Input(shape=(None, feature_size))
    all_outputs = []

    for i in range(1, radius):
        input_layer_rep, layer_fp = fingerprint_model_layer(input_graph, input_layer_rep, fingerprint_len, feature_size)
        layer_fp = layers.Lambda(lambda x:k.sum(x, axis=1))(layer_fp)
        all_outputs.append(layer_fp)

    #final_fp = layers.merge(all_outputs, mode='sum', name="final_merge")
    final_fp = layers.Lambda(lambda x : k.sum(x, axis=1))(all_outputs)
    
    neural_fp = models.Model(inputs = [input_graph, input_layer_rep], outputs = [final_fp])
    neural_fp.compile(optimizer = optimizers.Adam(), loss='categorical_crossentropy')
    return neural_fp
