import keras.layers as layers
import keras.models as models
import keras.backend as k
import keras.optimizers as optimizers
import keras.regularizers as regularizers
import custom_layer as ndense

def fingerprint_model_layer(molecule_graph, layer_rep, fingerprint_len, feature_size):
    v = layers.Lambda(lambda x:k.dot(molecule_graph, x))(layer_rep)
    ego_size = k.sum(molecule_graph, axis=1)
    
    layer_rep = ndense.NdexDense(feature_size, index=ego_size)(v)
    
    layer_fp = layers.Dense(fingerprint_len, activation='softmax')(v)
    return layer_rep, layer_fp

def neural_graph_fingerprints(molecule_graph, layer_rep, radius, fingerprint_len, feature_size):
    input_graph = layers.Input(shape=(feature_size,))
    input_layer_rep = layers.Input(shape=(feature_size,))
    all_outputs = []
    for i in range(1,radius):
        input_layer_rep, layer_fp = fingerprint_model_layer(input_graph, input_layer_rep, fingerprint_len, feature_size)
        all_outputs.append(layer_fp)
    final_fp = layers.merge(all_outputs, mode='sum')

    neural_fp = models.Model(inputs = [input_graph, input_layer_rep], outputs = [final_fp])
    neural_fp.compile(optimizer = optimizers.Adam(), loss='categorical_crossentropy')
    return neural_fp
