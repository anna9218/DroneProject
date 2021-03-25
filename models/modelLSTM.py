from models.model import model
import tensorflow as tf


class modelLSTM(model):

    def __init__(self):
        self.params = {'model_name': "",
                       'optimizer': "",
                       'metrics': "",
                       'iterations': 0,
                       'batch_size': 0,
                       'epochs': 0,
                       'neurons_in_layer': 0}

    def create_model(self, model_name, _units, input_dim, output_size):
        super(model_name)
        lstm_layer = tf.keras.layers.LSTM(_units, input_shape=(None, input_dim))
        self.model = tf.keras.models.Sequential([
            lstm_layer,
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(output_size)]
        )
        self.model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                           optimizer=self.params['optimizer'],
                           metrics=self.params['metrics'])


