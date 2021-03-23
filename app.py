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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                data_req = request.form
                data_req = dict(data_req)
                col = list(data_req.keys())
                value_list = list(data_req.values())
                value = []
                for i in value_list:
                    value.append(i)
                print(value)
                response = prediction.form_response(value_list=value, col=col)
                return render_template("index.html", response=response)

            elif request.json:
                df_json = request.json
                value_list = list(df_json.values())
                col = list(df_json.keys())
                response = prediction.api_response(value_list, col)
                return jsonify(response)

        except Exception as e:
            error = {"error":e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)