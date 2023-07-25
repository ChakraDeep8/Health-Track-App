import time
import streamlit as st
import pandas as pd
from Classifier_Models import Classifier_model_builder_heart as cmb
import pickle
import numpy as np


def app():
    st.title("Type2 Diabetes Detector")
    st.info("This app predicts whether a person have any type2 diabetes or not")

    st.sidebar.header('User Input Features')
    # st.sidebar.markdown("""
    # [Import input CSV file](https://github.com/ChakraDeep8/Heart-Disease-Detector/tree/master/res)""")

    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
    else:
        def patient_details():
            # Change the values below use Slider for int value and selectbox for catagorical value
            # ___________________________________________________________________________________
            # Here, I collect the live data from webpage and store in variables'
            # Change variable according your need, and you can decide what should be top in option
            sex = st.sidebar.selectbox('Sex', ('M', 'F'))
            ChestPainType = st.sidebar.selectbox('Chest Pain Type', ('TA', 'ASY', 'NAP'))
            RestingECG = st.sidebar.selectbox('Resting Electrocardiogram', ('Normal', 'ST', 'LVH'))
            ExerciseAngina = st.sidebar.selectbox('ExerciseAngina', ('Y', 'N'))
            ST_Slope = st.sidebar.selectbox('ST Slope', ('Up', 'Flat', 'Down'))
            Age = st.sidebar.slider('Age', 28, 77)
            RestingBP = st.sidebar.slider('Resting Blood Pressure', 0, 200)
            Cholesterol = st.sidebar.slider('Cholesterol', 0, 603)
            MaxHR = st.sidebar.slider('Maximum Heart Rate', 60, 202)
            Oldpeak = st.sidebar.slider('Old peak', -2, 6)
            FastingBS = st.sidebar.slider('Fasting Blood Sugar', 0, 1)
            # ___________________________________________________________________________________

            # Here, be careful on assigning the values
            # What is in ' ',that should be same as dataset key names
            # For example: 'Age' is also in dataset 'Age'
            data = {'Age': Age,
                    'Sex': sex,
                    'ChestPainType': ChestPainType,
                    'RestingBP': RestingBP,
                    'Cholesterol': Cholesterol,
                    'FastingBS': FastingBS,
                    'RestingECG': RestingECG,
                    'MaxHR': MaxHR,
                    'ExerciseAngina': ExerciseAngina,
                    'Oldpeak': Oldpeak,
                    'ST_Slope': ST_Slope, }

            features = pd.DataFrame(data, index=[0])
            return features

        input_df = patient_details()

    Type2_Diabetes_raw = pd.read_csv('res/diabetes.csv')
    Type2_Diabetes = Type2_Diabetes_raw.drop(columns=['Outcome'])
    df = pd.concat([input_df, Type2_Diabetes], axis=0)

    if uploaded_file is not None:
        st.write(df)
    else:
        st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
        df = df.loc[:, ~df.columns.duplicated()]
        st.write(df)

    # Load the classification models
    load_clf_NB = pickle.load(open('res/type_2_diabetes_classifier_NB.pkl', 'rb'))
    load_clf_KNN = pickle.load(open('res/type_2_diabetes_classifier_KNN.pkl', 'rb'))
    load_clf_DT = pickle.load(open('res/type_2_diabetes_classifier_DT.pkl', 'rb'))
    load_clf_LR = pickle.load(open('res/type_2_diabetes_classifier_LR.pkl', 'rb'))
    load_clf_RF = pickle.load(open('res/type_2_diabetes_classifier_RF.pkl', 'rb'))

    # Apply models to make predictions
    prediction_NB = load_clf_NB.predict(df)
    prediction_proba_NB = load_clf_NB.predict_proba(df)
    prediction_KNN = load_clf_KNN.predict(df)
    prediction_proba_KNN = load_clf_KNN.predict_proba(df)
    prediction_DT = load_clf_DT.predict(df)
    prediction_proba_DT = load_clf_DT.predict_proba(df)
    prediction_LR = load_clf_LR.predict(df)
    prediction_proba_LR = load_clf_LR.predict_proba(df)
    prediction_RF = load_clf_RF.predict(df)
    prediction_proba_RF = load_clf_RF.predict_proba(df)

    def NB():
        st.subheader('Naive Bayes Prediction')
        NB_prediction = np.array([0, 1])
        if NB_prediction[prediction_NB] == 1:
            st.write("<p style='font-size:20px;color: orange'><b>You have Type2 Diabetes</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Naive Bayes Prediction Probability')
        st.write(prediction_proba_NB)
        cmb.plt_NB()

    def KNN():
        st.subheader('K-Nearest Neighbour Prediction')
        knn_prediction = np.array([0, 1])
        if knn_prediction[prediction_KNN] == 1:
            st.write("<p style='font-size:20px;color: orange'><b>You have Type2 Diabetes</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('KNN Prediction Probability')
        st.write(prediction_proba_KNN)
        cmb.plt_KNN()

    def DT():
        st.subheader('Decision Tree Prediction')
        DT_prediction = np.array([0, 1])
        if DT_prediction[prediction_DT] == 1:
            st.write("<p style='font-size:20px; color: orange'><b>You have Type2 Diabetes</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Decision Tree Prediction Probability')
        st.write(prediction_proba_DT)
        cmb.plt_DT()

    def LR():
        st.subheader('Logistic Regression Prediction')
        LR_prediction = np.array([0, 1])
        if LR_prediction[prediction_LR] == 1:
            st.write("<p style='font-size:20px; color: orange'><b>You have Type2 Diabetes<b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Logistic Regression Probability')
        st.write(prediction_proba_LR)
        cmb.plt_LR()

    def RF():
        st.subheader('Random Forest Prediction')
        RF_prediction = np.array([0, 1])
        if RF_prediction[prediction_RF] == 1:
            st.write("<p style='font-size:20px; color: orange'><b>You have Type2 Diabetes</b></p>",
                     unsafe_allow_html=True)
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)
        st.subheader('Random Forest Probability')
        st.write(prediction_proba_RF)
        cmb.plt_RF()

    def predict_best_algorithm():
        if cmb.best_model == 'Naive Bayes':
            NB()

        elif cmb.best_model == 'K-Nearest Neighbors (KNN)':
            KNN()

        elif cmb.best_model == 'Decision Tree':
            DT()

        elif cmb.best_model == 'Logistic Regression':
            LR()

        elif cmb.best_model == 'Random Forest':
            RF()
        else:
            st.write("<p style='font-size:20px;color: green'><b>You are fine.</b></p>", unsafe_allow_html=True)

    # Displays the user input features
    with st.expander("Prediction Results"):
        # Display the input dataframe
        st.write("Your input values are shown below:")
        st.dataframe(input_df)
        # Call the predict_best_algorithm() function
        st.caption('Here, The best algorithm is selected among all algorithm')
        predict_best_algorithm()

    # Create a multiselect for all the plot options
    selected_plots = st.multiselect("Select plots to display",
                                    ["Naive Bayes", "K-Nearest Neighbors", "Decision Tree", "Logistic Regression",
                                     "Random Forest"])

    # Check the selected plots and call the corresponding plot functions

    placeholder = st.empty()

    # Check the selected plots and call the corresponding plot functions
    if "Naive Bayes" in selected_plots:
        with st.spinner("Generating Naive Bayes...."):
            cmb.plt_NB()
            time.sleep(1)

    if "K-Nearest Neighbors" in selected_plots:
        with st.spinner("Generating KNN...."):
            cmb.plt_KNN()
            time.sleep(1)

    if "Decision Tree" in selected_plots:
        with st.spinner("Generating Decision Tree...."):
            cmb.plt_DT()
            time.sleep(1)

    if "Logistic Regression" in selected_plots:
        with st.spinner("Generating Logistic Regression...."):
            cmb.plt_LR()
            time.sleep(1)

    if "Random Forest" in selected_plots:
        with st.spinner("Generating Random Forest...."):
            cmb.plt_RF()
            time.sleep(1)

    # Remove the placeholder to display the list options
    placeholder.empty()
