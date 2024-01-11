import pickle
import os
from .create_image_vecs import vectors_file
module_dir = os.path.dirname(__file__)  # get current directory

print("loading vectors from pickle file ...\n")

# For each test image, we store the filename and vector as key, value in a dictionary
pics = {}
with open(os.path.join(module_dir, vectors_file), 'rb') as inp:
    pics = pickle.load(inp)
