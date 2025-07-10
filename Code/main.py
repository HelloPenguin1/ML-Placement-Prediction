from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

app = FastAPI()


#Pydantic Model to validate upcoming User Data 

class UserInput(BaseModel):
    Prev_Sem_Result : Annotated[float, Field(..., gt=5, lt=10, description="Previous Semester's GPA")]
    IQ_group: Annotated[Literal['Low', 'Below Average', 'Average', 'Above Average', 'High'], Field(..., description="IQ/Critical-Thinking Skills")]
    CGPA: Annotated[float, Field(..., gt=5, lt=10, description="Current CGPA of Student")]
    Academic_Performance: Annotated[int, Field(..., gt=0, le=10, description="Academic Performance Rating on a scale of 1-10")]
    Internship_Experience: Annotated[Literal['Yes', 'No'], Field(..., description="Does the student have internship experience")]
    Projects_Completed: Annotated[int, Field(..., ge=0, le=5, description="How many projects have the student completed?")]
    extra_curr_score: Annotated[Literal['None', 'Low', 'Moderate', 'High'], Field(..., description="Student's Involvement in Extra_Curricular Activities")]
    Comm_score: Annotated[Literal['Poor', 'Fair', 'Good', 'Excellent'], Field(..., description="Student's Communication/Soft Skill Rating")]


#API Endpoint
@app.post('/predict')
def predict_placement(data: UserInput):
    try:
        input_df = pd.DataFrame([{
            'Prev_Sem_Result': data.Prev_Sem_Result,
            'CGPA': data.CGPA,
            'Academic_Performance':data.Academic_Performance,
            'Internship_Experience': data.Internship_Experience,
            'Projects_Completed': data.Projects_Completed,
            'IQ_group': data.IQ_group,
            'extra_curr_score': data.extra_curr_score,
            'Comm_score':data.Comm_score
        }])    

        prediction = model.predict(input_df)[0]
        predicted_label = label_encoder.inverse_transform([prediction])[0]

        return JSONResponse(status_code=200, content={'predicted_category': predicted_label})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})


    

