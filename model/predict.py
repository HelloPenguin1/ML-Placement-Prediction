import pickle
import pandas as pd

with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)


def predict_output(user_input: dict):

    input_df = pd.DataFrame([user_input])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    return prediction, confidence