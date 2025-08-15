from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.userinput import UserInput
from model.predict import predict_output, model
import pickle


with open('model/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

app = FastAPI()


@app.get('/')
def home():
    return {'message': 'College Placement Prediction using Random Forest'}

#good practice to note model verson
MODEL_VERSION = 1.0


#machine readable (to make it deployable in cloud services)
@app.get('/health')
def health_check():
    return (
        {
            'status':'OK',
            'version':MODEL_VERSION,
            'model_loaded': model is not None
        }
    )


#API Endpoint
@app.post('/predict')
def predict_placement(data: UserInput):
    try:
        input_df = {
            'Prev_Sem_Result': data.Prev_Sem_Result,   #getting the variables from Pydantic model 'UserInput'
            'CGPA': data.CGPA,
            'Academic_Performance':data.Academic_Performance,
            'Internship_Experience': data.Internship_Experience,
            'Projects_Completed': data.Projects_Completed,
            'IQ_group': data.IQ_group,
            'extra_curr_score': data.extra_curr_score,
            'Comm_score':data.Comm_score
        }    
        
        prediction, confidence = predict_output(input_df)
        predicted_label = label_encoder.inverse_transform([prediction])[0]
    

        return JSONResponse(status_code=200, content={
            'response': {
                'predicted_category': predicted_label,
                'confidence': round(confidence, 3)
            }
        })
    
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})


    

