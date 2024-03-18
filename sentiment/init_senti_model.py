#from transformers import pipeline
#model_path = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
#sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

POSITIVE = 'positive'
NEGATIVE = 'negative'
NEUTRAL = 'neutral'
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"

class SentimentTask(object):
    def __init__(self, MODEL) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.config = AutoConfig.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        return
    def __call__(self, text):
        # Preprocess text (username and link placeholders)
        total_score = 0
        top_class = NEUTRAL
        no_comm = 0
        for comm in text.split('|||'):
            no_comm += 1
            comm_class, comm_score = self.calculate_sent(comm)
            if comm_class == POSITIVE:
                total_score += comm_score
            elif comm_class == NEGATIVE:
                total_score -= comm_score

        if total_score > 0:
            top_class = POSITIVE
        elif total_score < 0:
            top_class = NEGATIVE

        return {"posting": top_class, "score": abs(total_score) / no_comm}
    
    def calculate_sent(self, text):
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        top_class = np.argmax(scores)
        return self.config.id2label[top_class], scores[top_class]

sentiment_task = SentimentTask(MODEL)