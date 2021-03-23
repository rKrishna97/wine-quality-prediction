from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import numpy as np
from prediction_service import prediction

# params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

# def read_params(config_path):
#     with open(config_path) as yaml_file:
#         config = yaml.safe_load(yaml_file)
#     return config

# def predict(data):
#     config = read_params(params_path)
#     model_dir_path = config["webapp_model_dir"]
#     model = joblib.load(model_dir_path)
#     prediction = model.predict(data)
#     print(prediction)
#     return prediction[0]

# def api_response(request):
#     try:
#         data = np.array([list(request.json.values())])
#         response = predict(data)
#         response = {"response":response}
#         return response
#     except Exception as e:
#         print(e)
#         error = {"error": "Something went wrong!! Try again"}
#         return error

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                print("this is request.form")
                # data = dict(request.form).values()
                # data = [i[0] for i in list(data)]
                # data = [list(map(float,data))]
                # print(data)
                data_req = request.form
                data_req = dict(data_req)
                col = data_req.keys()
                data_req = data_req.values()
                print(data_req)
                data_req = [float(i[0]) for i in list(data_req)]
                print(data_req)
                response = prediction.form_response(value_list=data_req, col=col)
                return render_template("index.html", response=response)

            elif request.json:
                print(request.json)
                df_json = request.json
                value_list = list(df_json.values())
                print(value_list)
                col = list(df_json.keys())
                print(col)
                response = prediction.api_response(value_list, col)
                return jsonify(response)

        except Exception as e:
            print("this is exception")
            print(e)
            error = {"error test": e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")

# run app
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)