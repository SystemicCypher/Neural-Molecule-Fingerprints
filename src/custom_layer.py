from keras import backend as K
from keras.engine.topology import Layer
import numpy as np

class NdexDense(Layer):
    def __init__(self, output_dim, activation = 'relu', kernel_initializer='glorot_uniform', index=[1], **kwargs):
        self.output_dim = output_dim
        self.activation = activation
        self.kernel_initializer = kernel_initializer
        self.index = index

        super(NdexDense, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        self.kernel = []
        if len(self.index) == 1:
            self.kernel.append(self.add_weight(name='kernel_{}'.format(self.index[0]), 
                                          shape=(input_shape[-1], self.output_dim),
                                          initializer=self.kernel_initializer,
                                          trainable=True))
        elif len(self.index) > 1:
            for i in range(len(self.index)):
                self.kernel.append(self.add_weight(name='kernel_{}'.format(self.index[i]), 
                                          shape=(input_shape[-1], self.output_dim),
                                          initializer=self.kernel_initializer,
                                          trainable=True))
        super(NdexDense, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        if len(self.index) == 1:
            return K.dot(x, self.kernel[0])
        elif len(self.index) > 1:
            output_tensor = []
            for i in range(len(self.index)):
                output_tensor.append(K.dot(x[i],self.kernel[self.index[i]]))
            output_tensor = np.array(output_tensor)
            output_tensor = K.variable(output_tensor)
            return output_tensor


    def compute_output_shape(self, input_shape):
        #return (input_shape[0], self.output_dim)
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = self.output_dim
        return tuple(output_shape)
