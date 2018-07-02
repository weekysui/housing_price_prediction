from flask import render_template, request, flash, redirect, Flask
from forms import HouseForms
import pickle
import pandas as pd
import os.path
import numpy as np
# from flask_wtf.csrf import CSRFProtect
# from config import SECRET_KEY

app = Flask(__name__)

# csrf = CSRFProtect()

# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)
# create_app()

current_path = os.path.split(os.path.abspath(__file__))[0]
with open(os.path.join(current_path,"clf_model.pkl"),"rb")as f:
    model = pickle.load(f)

def default_none(input_data):
    if input_data != None:
        return input_data
    else:
        return None

@app.route("/")
def root():
    global model
    form = HouseForms(csrf_enabled=False)  
    return render_template("index1.html",
    title = "House Price Prediction",
    form = form)

@app.route("/calculate", methods = ["POST"])
def index():
    global model
    form = HouseForms(csrf_enabled=False)
    # if (request.method == "POST") and (form.validate()):
    test_case = pd.DataFrame.from_dict({
        "Overall Quality": [float(form.overallQuality.data)],
        "Squarefeet": [float(form.area.data)],
        "Bedrooms":[float(form.bedrooms.data)],
        "Full Baths":[float(form.bathrooms.data)],
        "Garage Cars":[float(form.garage.data)],
        "Year Built":[float(form.yearBuilt.data)],
    })
    dummylist = []
    dummylist = 15*[0]
    dummy_df = pd.DataFrame([dummylist])
    test_case[["BldgType_1Fam",'BldgType_2fmCon', 'BldgType_Duplex', 'BldgType_Twnhs',
    'BldgType_TwnhsE', 'CentralAir_N', 'CentralAir_Y', 'HouseStyle_1.5Fin',
    'HouseStyle_1.5Unf', 'HouseStyle_1Story', 'HouseStyle_2.5Fin',
    'HouseStyle_2.5Unf', 'HouseStyle_2Story', 'HouseStyle_SFoyer',
    'HouseStyle_SLvl']]=dummy_df
    test_case.loc[0, form.buildingType.data] = 1
    test_case.loc[0, form.houseStyle.data] = 1
    test_case.loc[0, form.centralAir.data] = 1
    
    prediction = model.predict(test_case)
    p = round(prediction[0],2)
    print(p)
    # else:
    #     prediction = "N/A"
    #     print("what")
    
    return render_template("index1.html",
    title = "House Price Prediction",
    form = form,
    prediction = p)

if __name__ == ("__main__"):
    app.run(debug=True)