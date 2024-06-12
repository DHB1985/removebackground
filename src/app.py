from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

def renaper_validation(data, image_base64):
  return data["renaper"]

def change_background(image):
  output = remove(image, bgcolor=[255,255,255,255])

  return output

def decorator_data_save(data, image):
  buffered = io.BytesIO()
  image.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
  return jsonify({
    "dni": data["dni"],
    "gender": data["gender"],
    "imgSrc": img_str
  })

def save_data(data):
  return True

def decorator_data(image):
  buffered = io.BytesIO()
  image.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
  return jsonify({
    "result": True,
    "imgSrc": img_str
  })

@app.route('/removebackground', methods=['POST'])
def process_img():
  try:

    payload = request.get_json()

    data = {
      "dni": payload["dni"],
      "gender": payload["gender"],
      "renaper": payload["renaper"]
    }
    image_base64 = payload["image"]

    image_data = base64.b64decode(image_base64)

    image = Image.open(io.BytesIO(image_data))

    validation = renaper_validation(data, image_base64)

    if validation == 'true':

      processed_image = change_background(image)

      response_data = decorator_data(processed_image)

      return response_data, 200

    return jsonify({"result": False}), 400
    
  except Exception as e:
    return jsonify({"error": str(e)}), 400

@app.route('/status', methods=['GET'])
def get_status():
  return jsonify({"status": 'ok'}), 200

if __name__ == '__main__':
  app.run(use_reloader=True, host='0.0.0.0')