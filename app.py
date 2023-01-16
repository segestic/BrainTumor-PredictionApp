import streamlit as st
import json
import requests
from PIL import Image
import os

#option 2
import numpy as np
from tensorflow.keras.models import load_model
import cv2



def load_image(image):
	img = Image.open(image)
	return img

def save_uploadedfile(uploadedfile):
     with open(os.path.join("images/img",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
         uploaded_location = os.path.join("images/img",uploadedfile.name)
     return uploaded_location#st.success("Saved File:{} to {}".format(uploadedfile.name, uploaded_location))

def image_predict (image_file):
    model_path = 'application/models/multi_3_brainTumor89.h5'  
    h5_model = load_model(model_path)
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (512, 512)) 
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)
    h5_prediction = h5_model.predict(image)
    answer = np.argmax(h5_prediction)
    classes = ['Meningioma tumor', 'Glioma tumor', 'Pituitary tumor']     
    prediction =classes[int(answer)-1]
    print ('Prediction is ', prediction )  
    print('Prediction from h5 model: {}'.format(prediction))
    return  prediction
         

st.title("🦠 Brain Tumor Prediction App from MRI Images")



col1, col2 = st.columns([6, 3], gap="medium")

with col1:

        image = st.file_uploader("Upload CT Scan", type=["png","jpg","jpeg"])



        if image is not None:
            # To See details
            file_details = {"filename":image.name, "filetype":image.type,
                "filesize":image.size}
            st.write(file_details)

            #View Uploaded Image
            st.image(load_image(image),width=512)
            #save image to disk
            saved = save_uploadedfile(image)

            #OPTION 1 - with F-API..
            #if st.button ('Analyze'):
                #test_file = open(os.path.join("images/img", image.name), "rb")
                #response = requests.post('http://127.0.0.1:8000/predict/image', files={'file': test_file })
                #prediction = response.json()##json_object["prediction"]
                #st.write(prediction)
                #st. subheader (f"Response from BrainTumor Analyzer API = {prediction}")


            #OPTION 2 - NON API..
            if st.button ('Analyze'):
                with st.spinner('Analyzing...'):
                    prediction = image_predict(saved)
                    #st.write(prediction)
                    st. subheader (f"Image Prediction = {prediction}")
                    st.success(f"Image Prediction = {prediction}", icon="✅")

with col2:
#with st.sidebar:    
    st.write("Developed by AI & IOT Lab https://iot.neu.edu.tr by Olusegun Odewole (oooladeleodewole(at)gmail)  ")
    #st.header("Sample MRI Image")
    st.image( "https://res.cloudinary.com/segestic/image/upload/v1670497190/covid/images/Y99_ntvrog.jpg", width=300, caption='Sample CT-Scan Image')#width=400



#streamlit run app.py
#RUN BOTH for F-API...
#uvicorn application.server.main:app

#if __name__ == "__main__":
    #import uvicorn
    #uvicorn.run("application.server.main:app", host="0.0.0.0", port=8000, reload=False, log_level="debug", workers=1, limit_concurrency=1, limit_max_requests=1)











