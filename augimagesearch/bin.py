import torch
from img2vec_pytorch.img_to_vec import Img2Vec
from PIL import Image
import io
from augimagesearch.mongo_mod import mongo_filter_images
from pathlib import Path
import os
from augimagesearch.classification_model import NeuralNetwork
softmax = torch.nn.Softmax()

Classifier_Model = os.path.join(Path(__file__).resolve().parent, "image_classification.pt")

img2vec = Img2Vec()

def filter_images(images, top_k):
    products = mongo_filter_images(images, top_k)
    return products

class ImageCLSBase(object):

    def __init__(self, CLSPATH=Classifier_Model, classes=['footware-m', 'shoes-w', 'abaya-w', 'accessories-m', 'accessories-w', 'bags-w', 'jewelry-w', 'clothing-w', 'clothing-m']):
        self.clsmodel = NeuralNetwork()
        self.clsmodel.load_state_dict(torch.load(CLSPATH))
        self.clsmodel.eval()
        self.classes = classes

    def __call__(self, data):
        """ image classification base function """
        vec = img2vec.get_vec(Image.open(io.BytesIO(data)).convert('RGB'))
        pred = softmax(self.clsmodel(torch.from_numpy(vec)))
        return (self.classes[pred.argmax()], pred.max())
    

