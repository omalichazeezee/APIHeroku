from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class model_input(BaseModel):
    Age: int
    EstimatedSalary: int


# loading the saved model
RFC_model = pickle.load(open("RFC_model.pkl", "rb"))

@app.post('/purchase_prediction')
def purchase_pred(input_parameters: model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    Age = input_dictionary['Age']
    EstimatedSalary = input_dictionary['EstimatedSalary']


    input_list = [Age, EstimatedSalary]

    prediction = RFC_model.predict([input_list])

    if prediction[0] == 0:
        return 'The customer did not purchase'

    else:
        return 'The customer purchased'