from io import BytesIO
import uuid
import app as solver 
import base64
from flask import Flask, redirect, request, jsonify
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def predict():
    data = request.json.get('newPath')
    equ = request.json.get('equ')
    if equ == "multiple": 

        try:
            solver.predict_all(data)
            return jsonify({"success": "success"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        public = "public/"
        image_filename = "upload_images/"+ str(uuid.uuid4()) + ".jpg" # Provide a filename for the saved image
        image = Image.open(data)
        image.save(public + image_filename)
        try:
            equ,result = solver.solution(public + image_filename)
            return jsonify({"Image": image_filename, "Equation": equ, "Result": result})
        except Exception as e:
            return jsonify({"Error": str(e)})
    
@app.route('/solve', methods=['POST'])
def solve():
    data = request.json.get('dataURL')
    #print(data)
    _,  encoded_data = data.split(",", 1)
    image_data = base64.b64decode(encoded_data)
    public = "public/"
    image_filename = "saved_images/"+ str(uuid.uuid4()) + ".jpg" # Provide a filename for the saved image
    image = Image.open(BytesIO(image_data))
    image.save(public + image_filename)


    try:
        equ,result = solver.solution(public + image_filename)
        return jsonify({"Image": image_filename, "Equation": equ, "Result": result})
    except Exception as e:
        return jsonify({"Error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)