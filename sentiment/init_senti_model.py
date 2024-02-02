#from transformers import pipeline
#model_path = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
#sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax


def sentiment_task(text):
    # Preprocess text (username and link placeholders)
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    top_class = np.argmax(scores)
    return {"posting": config.id2label[top_class], "score": scores[top_class]}
    
    top_class = np.argmax(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        print(f"{i+1}) {l} {np.round(float(s), 4)}")
