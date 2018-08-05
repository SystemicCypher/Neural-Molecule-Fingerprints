import keras.layers as layers
import keras.models as models
import keras.backend as k
import keras.optimizers as optimizers
import keras.regularizers as regularizers
import custom_layer as ndense
import keras.utils as utils
import numpy as np
import sklearn.preprocessing as sk

def create_predictor():
    input_fp = layers.Input(shape=50, name="Fingerprint Input")
    density = layers.Dense(50)(input_fp)
    hidden = layers.Dense(50)(density)
    output = layers.Dense(2, activation='softmax')(hidden)
    predictor = models.Model(inputs=[input_fp], outputs=[output])
    predictor.compile(optimizer = optimizers.Adam(), loss='categorical_crossentropy')
    return predictor