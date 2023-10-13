from flask import Flask, render_template, request
from imageai.Detection import ObjectDetection
import os

# from twilio.rest import Client
# account_sid = "ACd53f4368502ea1c5141fcef7de856330"
# auth_token = "7723e9148f7a045ae2129020258fd717"
# client = Client(account_sid, auth_token)
#ngrok.set_auth_token("2Nh78bFZhR8aS8keQvkPijLQjGd_mTieoMb9koTxqfgkmKzY")
#port_no = 5000 






detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
if(os.path.isfile("tiny-yolov3.pt")): print("file is read") 
else: print("file is not there") 
detector.setModelPath("tiny-yolov3.pt")
detector.loadModel()
app = Flask(__name__)



import base64
  
@app.route("/hello")
def index():
  return render_template('home.html')


@app.route('/upload',methods=["POST"])
def uploadfile():
    if(request.method=="POST"):
        data = request.data.decode('utf-8')
        decoded_data=base64.b64decode((data))
        img_file = open('image.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()
        detections = detector.detectObjectsFromImage(input_image="image.jpeg", output_image_path="image2.jpeg", minimum_percentage_probability=30)
        for eachObject in detections:
            print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
            if(eachObject["name"] in ["person"]):
                #print("There is a human in that image") 
                return "1" 
        #do something with the data received
        
        return "0"
    
@app.route('/check',methods=["POST"])
def checkfile():
    print("CHECKFILE IS CALLED")
    if(request.method=="POST"):
        #data = request.data.decode('utf-8')
        #decoded_data=base64.b64decode((data))
        if(request.files['upload']): print("file is there") 
        else: print("file is not there")  
        
        #print(request.files['upload'].read())
        img_file = open('image.jpeg', 'wb')
        img_file.write(request.files['upload'].read())
        img_file.close()
        detections = detector.detectObjectsFromImage(input_image="image.jpeg", output_image_path="image2.jpeg", minimum_percentage_probability=30)
        for eachObject in detections:
            print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
            if(eachObject["name"] in ["person"]):
                return "1" 
                # message = client.messages.create(
                # body=eachObject["name"],
                # from_="+16206588938",
                # to="+919445079858")
                # print(message.sid)
        #do something with the data received
        
        return "0"
    

@app.route("/")
def indexFile():
  return "this is the index string" 




if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
# #print("To access the site click the link " ,  public_url) 
# app.run(port=port_no)


# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'