import os
from PIL import Image


class LOADER:
    @staticmethod
    def get_image(id):
        path = os.path.join(os.getcwd(), "res", "images", str(id) + ".jpg")

        return Image.open(path)
    
    def get_image_path(id):
        path = os.path.join(os.getcwd(), "res", "images", str(id) + ".jpg")

        return path
    
    @staticmethod
    def get_path():
        return os.path.join(os.getcwd(), "res", "images\\")
    
    def get_eating():
        return os.path.join(os.getcwd(), "res", "eating.csv")
    
    @staticmethod
    def get_new_index(): 
        index = 0 
        images_path = os.path.join(os.getcwd(), "res", "images")
        
        for file in os.listdir(images_path): 
            full_path = os.path.join(images_path, file)
            if os.path.isfile(full_path): 
                index += 1 
            
        return index