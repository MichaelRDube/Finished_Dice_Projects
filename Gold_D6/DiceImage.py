from tkinter import *
from PIL import Image, ImageTk

class DiceImage:
    
    def __init__(self, rollnum, photo_path, label, confidence, flagged):
        self.rollnum = rollnum #roll id in database
        self.photo_path = photo_path #path to photo
        self.label = label #digit identified
        self.confidence = confidence
        self.flagged = flagged #1 if the predictive model could not properly identify digit
        
    def load_image(self):
        # Open the image and convert it to a Tkinter-compatible PhotoImage
        
        try:
            image = Image.open(self.photo_path)
            
            #resize it
            original_width, original_height = image.size
            ratio = original_height/original_width
            
            new_width = 500
            new_height = round(new_width*ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            
            return ImageTk.PhotoImage(image)
        
        except Exception as e:
            print("Could not load picture.")
