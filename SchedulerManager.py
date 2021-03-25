from DataPreparation import DataPreparation


class SchedulerManager:
    data_preparation = DataPreparation()

    def get_model_parameters(self, model_name: str):
        pass

    def run_job(self, model_name: str, logs_queries: dict, prediction_variable: str, prediction_values: list, parameters: dict) -> list:
        self.data_preparation.create_data_directories(logs_queries, prediction_variable, prediction_values)
        self.data_preparation.prepare_data()
        pass

    def get_models_names(model_name: str) -> list:
        pass

    def get_model_parameters(model_name: str) -> list:
        pass


    def set_model_params_vals(params: dict) -> list:
        pass