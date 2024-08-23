from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
from PIL.ExifTags import TAGS
import os
import io
import base64

app = Flask(__name__)

def get_exif_data(image):
    exif_data = {}
    if hasattr(image, '_getexif'):
        exif_info = image._getexif()
        if exif_info:
            for tag_id, value in exif_info.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = str(value)
    return exif_data

def remove_exif(image):
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    return image_without_exif

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        image = Image.open(file.stream)
        exif_data = get_exif_data(image)
        
        # Convert image to base64 for display
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'exif_data': exif_data,
            'image': img_str
        })

@app.route('/remove_exif', methods=['POST'])
def remove_exif_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        image = Image.open(file.stream)
        image_without_exif = remove_exif(image)
        
        # Generate new filename
        file_name, file_extension = os.path.splitext(file.filename)
        new_filename = f"{file_name}_new{file_extension}"
        
        # Save the image without EXIF (in memory for now)
        buffered = io.BytesIO()
        image_without_exif.save(buffered, format=image.format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'image': img_str,
            'filename': new_filename
        })

if __name__ == '__main__':
    app.run(debug=True)