from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Load the trained model
model = load_model('model/dog_breed.h5')

# Define the breed labels (replace with your own labels)
breed_labels = ['Labrador', 'German Shepherd', 'Bulldog', 'Poodle', 'Beagle']

def predict_breed(image_path):
    img = load_img(image_path, target_size=(224, 224))  # Adjust target size as per your model
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize if required
    prediction = model.predict(img_array)
    breed_index = np.argmax(prediction)
    return breed_labels[breed_index]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            breed = predict_breed(filepath)
            return render_template('index.html', breed=breed, image_path=filepath)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
