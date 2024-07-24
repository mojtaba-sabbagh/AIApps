from img2vec_pytorch.img_to_vec import Img2Vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from imagesearch.init_imagesearch import pics
import io

img2vec = Img2Vec()
def imagesearch_base(data):
    """ image search base function """
    vec = img2vec.get_vec(Image.open(io.BytesIO(data)).convert('RGB'))
    sims = {}
    for key in list(pics.keys()):
        sims[key] = cosine_similarity(vec.reshape((1, -1)), pics[key].reshape((1, -1)))[0][0]

    d_view = [(v, k) for k, v in sims.items()]
    d_view.sort(reverse=True)
    return d_view
