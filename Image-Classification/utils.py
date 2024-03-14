import numpy as np
from PIL import Image, ImageTk
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('tf_models/classification.keras')

# Constants
IMAGE_SIZE = model.layers[0].input_shape[1]

# Label encoding
prediction_map = {
    0: 'buildings',
    1: 'forest',
    2: 'glacier',
    3: 'mountain',
    4: 'sea',
    5: 'street'
}

def get_image(image_path, scale_factor=1.5):
    # Open the image
    image = Image.open(image_path)
    
    # Return Image as "ImageTk" object
    return ImageTk.PhotoImage(image.resize((int(image.width * scale_factor), int(image.height * scale_factor))))

def get_image_and_pred_label(image_path, scale_factor=1.5):
    # Open the image
    image = Image.open(image_path)
    
    # Resize the image to fit the input shape of the model
    resized_image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    
    # Converting to numpy array
    image_numpy = np.array(resized_image) / 255 # Normalizing pixel color values

    # Throw exception in case if size or color channels do not fit the input shape
    if image_numpy.shape != (IMAGE_SIZE, IMAGE_SIZE, 3):
        raise Exception(f'Image should have dimensions ({IMAGE_SIZE}, {IMAGE_SIZE}, 3)')
    
    # Reshaping the array
    image_numpy = np.expand_dims(image_numpy, axis=0)
    
    # Getting model predictions
    raw_predictions = model.predict(image_numpy, verbose=0) 
    prediction = np.argmax(raw_predictions, axis=1).item()
    
    # Return rescaled image as "ImageTk" object along with the predicted label string 
    tk_image = ImageTk.PhotoImage(image.resize((int(image.width * scale_factor), int(image.height * scale_factor))))
    return tk_image, prediction 

