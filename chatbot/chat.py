import random
import json

import torch
import os
module_dir = os.path.dirname(__file__)  # get current directory


from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize
THERESHOLD = 0.40

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

file_path = os.path.join(module_dir, 'intents.json')
with open(file_path, 'r') as json_data:
    intents = json.load(json_data)

FILE = os.path.join(module_dir, "./data.pth")
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Aria"
def chat_func(sentence):
    # sentence = "do you use credit cards?"
    if sentence == "quit":
        return {"posting": "Good bye!", "score": 1.0}

    sentence = tokenize(sentence) 
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > THERESHOLD:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return {"posting": f"{bot_name}: {random.choice(intent['responses'])}", "score": prob.item()}
    else:
        return {"posting": f"{bot_name}: I do not understand...", "score": prob.item()}