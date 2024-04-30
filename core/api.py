from typing import List
from ninja import NinjaAPI, Schema
from semanticsearch.init_search import util, embedder, corpus_embeddings, corpus
from imagesearch.init_imagesearch import pics
from img2vec_pytorch.img_to_vec import Img2Vec
from PIL import Image
from ninja import File
from ninja.files import UploadedFile
from sklearn.metrics.pairwise import cosine_similarity
import io
from chatbot.chat import chat_func
from sentiment.init_senti_model import sentiment_task

api = NinjaAPI()
img2vec = Img2Vec()
class Hit(Schema):
    posting: str
    score: float

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

@api.post("/imagesearch", response=List[Hit])
def image_search(request, file: UploadedFile = File(...)):
    data = file.read()
    vec = img2vec.get_vec(Image.open(io.BytesIO(data)).convert('RGB'))
    sims = {}
    for key in list(pics.keys()):
        sims[key] = cosine_similarity(vec.reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]

    d_view = [(v, k) for k, v in sims.items()]
    d_view.sort(reverse=True)
    top_k = min(10, len(d_view)) # Top_k for number of images found is set to 10
    hit_outs = []
    for v, k in d_view[:top_k]:
        hit_outs.append({"posting": f"{request.scheme}://{request.get_host()}/static/{k}", "score": v})
    return hit_outs

@api.get("/chatbot", response=Hit)
def chat(request, query: str):
    return chat_func(query)

@api.get("/sentiment", response=Hit)
def senti_func(request, query: str):
    #senti = sentiment_task(query)[0]
    return sentiment_task(query)