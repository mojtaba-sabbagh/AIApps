from typing import List
from ninja import NinjaAPI, Schema
from semanticsearch.init_search import util, embedder, corpus_embeddings, corpus
from img2vec_pytorch.img_to_vec import Img2Vec
from ninja import File
from ninja.files import UploadedFile
from augimagesearch.bin import filter_images, ImageCLSBase
from imagesearch.bin import imagesearch_base

from chatbot.chat import chat_func
from sentiment.init_senti_model import sentiment_task

api = NinjaAPI()
img2vec = Img2Vec()
MAX_TOPK = 10

class Hit(Schema):
    posting: str
    score: float

class PRODUCT(Schema):
    title: str
    slug: str
    price: int
    salePrice: int
    uploadedFiles: List[str]
    outOfStockDate: str
    stockStatus: str
    productLabels: str

@api.get("/", response=str)
def home(request, query: str):
    return "<h1> Hello World </h1>"

@api.get("/search", response=List[Hit])
def search(request, query: str):
    hit_outs = []
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    top_k = min(10, len(corpus)) #
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k)
    hits = hits[0]
    for hit in hits:
        hit_outs.append({"posting": corpus[hit['corpus_id']], "score": hit['score']})
    return hit_outs

image_prefix = "https://anah-v2.s3.amazonaws.com"

@api.post("/imagesearch", response=List[Hit])
def image_search(request, file: UploadedFile = File(...)):
    data = file.read()
    d_view = imagesearch_base(data)
    top_k = min(MAX_TOPK, len(d_view)) # Top_k for number of images found is set to 10
    hit_outs = []
    for v, k in d_view[:top_k]:
        hit_outs.append({"posting": f"{image_prefix}/{k}", "score": v})
    return hit_outs

@api.post("/productimagesearch", response=List[PRODUCT])
def image_search(request, file: UploadedFile = File(...)):
    data = file.read()
    d_view = imagesearch_base(data)
    top_k = min(MAX_TOPK, len(d_view)) # Top_k for number of images found is set to 10
    products = filter_images(d_view, top_k)
    return products

@api.get("/chatbot", response=Hit)
def chat(request, query: str):
    return chat_func(query)

@api.get("/sentiment", response=Hit)
def senti_func(request, query: str):
    #senti = sentiment_task(query)[0]
    return sentiment_task(query)                                                                                                          

@api.post("/imagecls", response=Hit)
def image_cls(request, file: UploadedFile = File(...)):
    data = file.read()
    classifier = ImageCLSBase()
    predicted = classifier(data)
    hit_out = {"posting": predicted[0], "score": predicted[1]}
    return hit_out
