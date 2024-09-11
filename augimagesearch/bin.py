import torch
from img2vec_pytorch.img_to_vec import Img2Vec
from PIL import Image
import io
from augimagesearch.mongo_mod import mongo_filter_images
from pathlib import Path
import os
from augimagesearch.classification_model import NeuralNetwork
from bson.objectid import ObjectId
softmax = torch.nn.Softmax()

Classifier_Model = os.path.join(Path(__file__).resolve().parent, "image_classification.pt")

img2vec = Img2Vec()
default_classes = ['footware-m', 'shoes-w', 'abaya-w', 'accessories-m', 'accessories-w', 'bags-w', 'jewelry-w', 'clothing-w', 'clothing-m','cosmatic-w']
class_map = {
	"footware-m":[ObjectId("60c87d01ee31952720fffd79"), ObjectId("612485b55c1f5e0fc039361d"), ObjectId("618e2ed9c8b3841218a4fff9")],
	"shoes-w":[ObjectId("60c87bb0ee31952720fffd78"), ObjectId("61234d9256cc6d05dc20117a")],
	"abaya-w":[ObjectId("668d220228231a01e33b5664"), ObjectId("618bb860f874370f109e7cf8")],
	"accessories-m":[ObjectId("618e30e7c8b3841218a5002b"), ObjectId("612486185c1f5e0fc0393621"), ObjectId("6193a179ae2f5c09a807d3cc")],
	"accessories-w":[ObjectId("66644e0735ade925eff6c0a0"), ObjectId("665837f9c610c06f936f17ce")],
                  
	"bags-w":[ObjectId("612484d45c1f5e0fc0393615"), ObjectId("618bb292f874370f109e7b3d")], 
	"jewelry-w":[ObjectId("66644ec735ade925eff6c0cf")],
	"clothing-w":[ObjectId("6126259f7335225914b7ff11"), ObjectId("6126266e7335225914b7ff32"),
                 ObjectId("6194ca346b8e340f681c3704")],
	"clothing-m":[ObjectId("6194c5666b8e340f681c3411")]
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
            print(prod["categories"])
            print(allowed_cats)
            if self.__intersection(prod["categories"], allowed_cats):
                filtered_products.append(prod)
        return filtered_products

