import os
from PIL import Image


class LOADER:
    @staticmethod
    def get_image(id):
        path = os.path.join(os.getcwd(), "res", "images", id)

        return Image.open(path)
    
    @staticmethod
    def get_path():
        return os.path.join(os.getcwd(), "res", "images\\")
    
    @staticmethod
    def get_new_index(): 
        index = 0 
        images_path = os.path.join(os.getcwd(), "res", "images")
        
        for file in os.listdir(images_path): 
            full_path = os.path.join(images_path, file)
            if os.path.isfile(full_path): 
                index += 1 
            
        return index