from flask import Flask, request, redirect, render_template
import numpy as np
import io
import os
from IPython.display import display_png
from PIL import Image, ImageFile
from rembg.bg import remove
import base64
ImageFile.LOAD_TRUNCATED_IMAGES = True

api = Flask(__name__)
outDir = 'output'

@api.route('/')
def index():
  return render_template('index.html')

@api.route("/upload", methods = ["POST"])
def upload():
  if request.files['image']:
    stream = request.files['image'].stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

    try:
      result = remove(img_array,
          model_name="u2net",
          alpha_matting=True,
          alpha_matting_foreground_threshold=240,
          alpha_matting_background_threshold=10,
          alpha_matting_erode_structure_size=4)
      img = Image.open(io.BytesIO(result)).convert("RGBA")

      # local save
      if not os.path.exists(outDir):
        os.makedirs(outDir)
      output_path = outDir + '/cutout.png'
      img.save(output_path)

      # byte data
      buffer = io.BytesIO()
      img.save(buffer, format='PNG')
      binaryData = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

      return render_template('index.html', image=binaryData)
      # return redirect('/')

    except Exception as e:
      print(e)
      return render_template('index.html')


if __name__ == '__main__':
    api.debug = True
    api.run(host='0.0.0.0', port=5000)