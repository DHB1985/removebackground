import io
import os
import base64
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image

app = Flask(__name__)
CORS(app)

def apikey_required(f):
  @wraps(f)
  def decorator(*arg, **kwargs):
    apikey = request.headers.get('apikey')
    try:
      if apikey and os.getenv('VALID_APIKEY') == apikey:
        return f(*arg, **kwargs)
      return jsonify({'message': 'Not ApiKey or invalid'}),401
    except:
      return jsonify({'message': 'Not ApiKey or invalid'}),401
  return decorator

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

@app.route('/status', methods=['GET'])
@apikey_required
def get_status():
  return jsonify({"status": 'ok'}), 200

@app.route('/removebackground', methods=['POST'])
@apikey_required
def process_img():
  try:
    payload = request.get_json()
    image_base64 = payload["image"]
    image_data = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_data))

    processed_image = change_background(image)
    response_data = decorator_data(processed_image)

    return response_data, 200

  except Exception as e:
    return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
  app.run(use_reloader=True, host='0.0.0.0')