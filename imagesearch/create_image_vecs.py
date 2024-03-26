import os
from img2vec_pytorch.img_to_vec import Img2Vec
from PIL import Image
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
input_path = 'images'
vectors_file = 'image_vectors.pkl'
print("Getting vectors for test images...\n")
img2vec = Img2Vec()

# For each test image, we store the filename and vector as key, value in a dictionary
pics = {}

def image2vectors():
    for file in os.listdir(input_path):
        filename = os.fsdecode(file)
        img = Image.open(os.path.join(BASE_DIR, input_path, filename)).convert('RGB')
        vec = img2vec.get_vec(img)
        pics[filename] = vec

    with open(vectors_file, 'wb') as outp:
        pickle.dump(pics, outp, pickle.HIGHEST_PROTOCOL)
    return


if __name__ == "__main__":
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "semanticsearch.settings")
    image2vectors()




