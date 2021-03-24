import yaml 
import os 
import json
import joblib
import numpy as np 

params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json")


class NotInRange(Exception):
    def __init__(self, message = "Values entered are not in range"):
        self.message = message
        super().__init__(self.message)


class NotInCols(Exception):
    def __init__(self, message="Not in columns"):
        self.message = message
        super().__init__(self.message)

def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]

    try:
        if 3 <= prediction <=8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result"



def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema


def validate_input(value_list, col):
   
    def _validate_values(val, col):
        schema = get_schema()
        col = col.replace(" ","_")
        if not (schema[col]["min"] <= float(val) <=schema[col]["max"]):
            raise NotInRange
        
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols 
    
    for val,column_name in zip(value_list,col):
        _validate_values(val, column_name)


    for column_name in col:
        _validate_cols(col=column_name)
   
    return True


def form_response(value_list, col):
    if validate_input(value_list, col):
        data = [list(map(float, value_list))]
        response = predict(data)
        return response
        


def api_response(value_list, col):
    try:
        if validate_input(value_list, col):
            data = np.array([value_list])
            response = predict(data)
            response = {"response": response}
            return response


    except NotInRange as e:
        response = {"the_expected_range": get_schema(), "response": str(e)}
        return response

    except NotInCols as e:
        response = {"response": str(e)}
        return response