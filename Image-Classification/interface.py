import tkinter as tk
import os
import random

# Simple interface that includes image and a predicted label.

# Disabling TensorFlow warnings before it is imported into the project
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from utils import get_image, get_image_and_pred_label, prediction_map

# Paths to dataset folder and to the data that is new to the convolutional model
main_path = 'intel_image_dataset'
pred_path = 'seg_pred/seg_pred'
path_to_images = os.path.join(main_path, pred_path)

# Amount of different images to be loaded from a directory 
IMAGE_COUNT = 200
counter = 0

# Time in seconds until the new image is displayed
seconds = 2.5
time_between = int(seconds * 1000)

# Font used for the text label 
font_tuple = ('Roboto', 14, 'bold')


# Dictionary is used to avoid making repeated predictions for the same image (memoization)
image_label_dict = {}

for filename in os.listdir(path_to_images):
    # Path to current image
    path = os.path.join(path_to_images, filename)
    
    # Filling dictionary
    image_label_dict[path] = -1
    
    counter += 1
    if counter >= IMAGE_COUNT:
        break


class ImageLabelUpdater:
    def __init__(self, root):
        # Attribute referring to the master element of the Tkinter application
        self.root = root
        
        # Choosing the new image path randomly
        idx_random = random.randrange(IMAGE_COUNT)
        self.image_path = list(image_label_dict)[idx_random]
        
        tk_image, prediction = get_image_and_pred_label(self.image_path)
        image_label_dict[self.image_path] = prediction
        
        # Name of the class
        label = prediction_map[prediction]
        
        self.image_label = tk.Label(master=self.root, image=tk_image)
        self.image_label.image = tk_image
        self.predicted_label = tk.Label(root, text=f"Prediction: '{label}'")
        self.predicted_label.configure(font=font_tuple, bg='white')
        
        self.pack_widgets()
        

    def update_image(self):
        # Choosing the new image path randomly
        idx_random = random.randrange(IMAGE_COUNT)
        self.image_path = list(image_label_dict)[idx_random]
        
        # Memoization
        if image_label_dict[self.image_path] > -1:
            tk_image, prediction = get_image(self.image_path), image_label_dict[self.image_path]
        else:
            tk_image, prediction = get_image_and_pred_label(self.image_path)
            image_label_dict[self.image_path] = prediction
        
        label = prediction_map[prediction]
        self.image_label.image = tk_image
        
        # Configuration
        self.image_label.configure(image=tk_image)
        self.predicted_label.configure(text=f"Prediction: '{label}'")
        
        self.root.after(time_between, self.update_image)

    def pack_widgets(self):
        # Displaying GUI components on a Tkinter window
        self.image_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.predicted_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)


if __name__ == "__main__":
    # Creating the Tkinter window 
    root = tk.Tk()
    root.title("Classification")
    root.geometry('300x300')
    root.configure(bg='white')

    # Declaring a new instance of the ImageLabelUpdater class and starting a routine to update image and label
    updater = ImageLabelUpdater(root)
    root.after(time_between, updater.update_image)
    
    root.mainloop()