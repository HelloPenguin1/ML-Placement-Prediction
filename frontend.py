import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/predict'  ##noted from FASTAPI /docs

st.title("College Student Placement Prediction")
st.markdown("Based on a realistic synthetic Kaggle dataset of 10,000 students designed to analyze factors affecting college placements.")

#input 
Prev_Sem_Result=st.number_input("Previous Semester GPA (out of 10)", min_value=5.00, max_value=10.00, step=0.1, format="%.2f")
CGPA=st.number_input("Current CGPA (out of 10)", min_value=5.00, max_value=10.00, step=0.1, format="%.2f")
Academic_Performance=st.slider("Rate your Academic Performance on a scale of 1 to 10", min_value=1, max_value=10)
Internship_Experience=st.selectbox("Do you have any internship experience", ['Yes', 'No'])
Projects_Completed=st.selectbox("How many technical/field relevant projects completed?", ['0','1','2','3','4','5'])
IQ_group = st.selectbox(
    "How would you rate your cognitive/critical thinking skills?",
    ['Low', 'Below Average', 'Average', 'Above Average', 'High'], index=2, 
    help="Definition of categories:\n- Low: IQ 41–69\n- Below Average: IQ 80–89\n- Average: IQ 90–109\n- Above Average: IQ 110–129\n- High: IQ 130–158"
)
extra_curr_score=st.selectbox("Rate your involvement in extra-curricular activites", ['None', 'Low', 'Moderate', 'High'])
Comm_score=st.selectbox("Rate your Soft Skills/Communication Skills", ['Poor', 'Fair', 'Good', 'Excellent'])



if st.button("Predict Placement"):
    input_data={
        'Prev_Sem_Result': Prev_Sem_Result,
        'CGPA': CGPA,
        'Academic_Performance':Academic_Performance,
        'Internship_Experience': Internship_Experience,
        'Projects_Completed': int(Projects_Completed),
        'IQ_group': IQ_group,
        'extra_curr_score': extra_curr_score,
        'Comm_score':Comm_score
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Placement Prediction: **{prediction['predicted_category']}**")
            st.write("Confidence:", prediction["confidence"])
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Make sure it's running.")

