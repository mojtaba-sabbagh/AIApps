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
default_classes = ['footware-m', 'shoes-w', 'abaya-w', 'accessories-m', 'accessories-w', 'bags-w', 'jewelry-w', 'clothing-w', 'clothing-m']
class_map = {
	"footware-m":["618e2ed9c8b3841218a4fff9"],
	"shoes-w":["618bb3abf874370f109e7c45","618bb62cf874370f109e7c80"],
	"abaya-w":["668d220228231a01e33b5664"],
	"accessories-m":["612486185c1f5e0fc0393621"],
	"accessories-w":["665837f9c610c06f936f17ce"],
	"bags-w":["612484d45c1f5e0fc0393615","618bb26ff874370f109e7b39","618bb292f874370f109e7b3d"],
	"jewelry-w":["id:66644ec735ade925eff6c0cf"],
	"clothing-w":["6126259f7335225914b7ff11s","6126266e7335225914b7ff32","6194ca346b8e340f681c3704"],
	"clothing-m":["6194c5666b8e340f681c3411"]
}
def filter_images(images, top_k):
    products = mongo_filter_images(images, top_k)
    return products

class ImageCLSBase(object):

    def __init__(self, CLSPATH=Classifier_Model, classes=default_classes, class_map=class_map):
        self.clsmodel = NeuralNetwork()
        self.clsmodel.load_state_dict(torch.load(CLSPATH, map_location=torch.device('cpu')))
        self.clsmodel.eval()
        self.classes = classes
        self.class_map = class_map

    def __call__(self, data):
        """ image classification base function """
        vec = img2vec.get_vec(Image.open(io.BytesIO(data)).convert('RGB'))
        pred = softmax(self.clsmodel(torch.from_numpy(vec)))
        return (self.classes[pred.argmax()], pred.max())
    
    def predict(self, data):
        """ image classification base function """
        vec = img2vec.get_vec(Image.open(io.BytesIO(data)).convert('RGB'))
        pred = self.clsmodel(torch.from_numpy(vec))
        return self.classes[pred.argmax()]
    
    def __intersection(self, list1, list2):
        for value in list1:
            if value in list2:
                return True
        return False
    
    def filter_by_type(self, products, data):
        filtered_products = []
        image_cls = self.predict(data)
        allowed_cats = self.class_map[image_cls]
        for prod in products:
            if self.__intersection(prod["categories"], allowed_cats):
                filtered_products.append(prod)
        return filtered_products

