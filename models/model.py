class model:
    model = None
    model_name: str = ""
    params: dict = {}
    prediction_variable: dict = {}

    def __init__(self):
        pass

    def get_parameters(self) -> list:
        """
            1. Returns the model's parameters list
        """
        return self.params.keys()

    def set_parameters_vals(self, params_val: dict) -> bool:
        """
            2. Set values to the model's parameters
        :param params_val: {param1: val1, param2: val2}
        """
        for key in params_val.keys():
            self.params[key] = params_val[key]


    def set_prediction_variable(self, variable_name: str, variable_values: list) -> bool:
        """
            3. set prediction variable's name and values
        :param variable_name:
        :param variable_values:
        :return:
        """
        self.prediction_variable = {'variable_name': variable_name, 'variable_values': variable_values}

    def select_data(self):
        """
            4. Select subset of the data according to the... TODO:
        :return:
        """
        pass

    # def data_preparations(self):
    #     """
    #         5. data preparations
    #     :return:
    #     """
    #     pass
    #
    # def split_data_to_train_and_test(self):
    #     """
    #         6. Split the data to 2 datasets
    #         train_dataset: 80% of the data
    #         test_dataset: 20% of the data
    #     :return: train_dataset and test_dataset
    #     """
    #     pass

    def train_model(self, data_directory):
        """
            7. Train the model on the selected train_dataset and test_dataset
        :return:
        """
        self.model.train()

    def predict(self):
        """
            8. Predict
        :return:
        """
        self.model.predict()



    # def calc_generic_model_average_succes(input_dim, features, labels, optimizer, metrics,
    #                                       output_size, iterations, batch_size, epochs, model_name,
    #                                       neurons_in_layer, training_features=None, training_labels=None,
    #                                       test_features=None, test_labels=None, verbose=0):
    #     eval_sum = 0
    #     is_random_split = (training_features is None)
    #     results = []
    #     for i in range(iterations):
    #         first_layer = ""
    #         if model_name == "LSTM":
    #             first_layer = tf.keras.layers.LSTM(neurons_in_layer, input_shape=(None, input_dim))
    #         if model_name == "GRU":
    #             first_layer = tf.keras.layers.GRU(neurons_in_layer, input_shape=(None, input_dim))
    #         if model_name == "DENSE":
    #             first_layer = tf.keras.layers.Dense(neurons_in_layer, input_shape=(None, input_dim))
    #         if is_random_split:
    #             # split the dataset randomly to training and testing
    #             training_features, training_labels, test_features, test_labels = get_features_and_labels(features,
    #                                                                                                      labels,
    #                                                                                                      number_of_features=int(
    #                                                                                                          features.shape[
    #                                                                                                              0] * 0.8))
    #         model = build_generic_model(first_layer, optimizer, metrics, output_size)
    #         model.fit(training_features, training_labels,
    #                   # validation_data=(test_LSTM_features, test_LSTM_labels),
    #                   batch_size=batch_size,
    #                   verbose=0,
    #                   epochs=epochs)
    #         model_evaluation = model.evaluate(test_features, test_labels, verbose=verbose)
    #         eval_sum += model_evaluation[1] * 100
    #         results.append(model_evaluation[1] * 100)
    #
    #     results_np = np.array(results)
    #     sumery_str = ""
    #     sumery_str += ("mean = " + "%.5f" % results_np.mean())
    #     sumery_str += (", std: " + "%.5f" % results_np.std())
    #     sumery_str += (", model_name:" + model_name)
    #     sumery_str += (", optimizer:" + optimizer)
    #     sumery_str += (", iterations:" + str(iterations))
    #     sumery_str += (", batch_size:" + str(batch_size))
    #     sumery_str += (", epochs:" + str(epochs))
    #     sumery_str += (", neurons_in_layer:" + str(neurons_in_layer))
    #     sumery_str += (", min: " + "%.5f" % results_np.min())
    #     sumery_str += (", max: " + "%.5f" % results_np.max())
    #     sumery_str += (", results: " + str(list(map(lambda x: "%.5f" % x, results))))
    #     print(sumery_str)
