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

    # try:
    #     if 3 <= prediction <=8:
    #         return prediction
    #     else:
    #         raise NotInRange
    # except NotInRange:
    #     return "Unexpected result"

    return prediction


def get_schema(shema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema


def validate_input(value_list, col):
    print("this is validate_input")

    def _validate_cols(col):
        print("this is validate_cols")
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(value_list, col):
        schema = get_schema()
        # print(schema[col]["min"])
        # print(dict_request[col][0])
        # print(schema[col]["max"])
        # print()
        print(col)
        print(f"min: {schema[col]['min']} val: {float(val)} max: {schema[col]['max']}")
        
        if not (schema[col]["min"] <= float(val) <=schema[col]["max"]):
            raise NotInRange
    
    

    for col_name in col:
        print("this is for col_name")
        _validate_cols(col_name)
    
    for val,column_name in zip(value_list,col):
        print("this is for val,col_name")
        _validate_values(val, column_name)

    
    return True

def form_response(value_list, col):
    print("this is form_response out")
    if validate_input(value_list, col):
        print("This is form_response")
        # data = dict_request.values()
        data = [list(map(float, value_list))]
        # data = dict_request.values()
        # data = [i[0] for i in list(data)]
        # print(data)
        # data = [list(map(float,data))]
        print(data)
        response = predict(data)
        return response


def api_response(value_list, col):
    try:
        if validate_input(value_list, col):
            data = np.array([value_list])
            response = predict(data)
            response = {"response": response}
            print(response)
            return response

    except Exception as e:
        response = {"the_expected_range": get_schema(), "response": str(e)}
        return response