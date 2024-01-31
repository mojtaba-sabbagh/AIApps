# -*- coding: utf-8 -*-
import os

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

embedder = SentenceTransformer ('all-MiniLM-L6-V2')
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'items.txt')
fp = open(file_path, encoding='UTF-8')

corpus = fp.readlines()
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
top_k = min(5, len(corpus))

"""
queries = ['shoulder bag zara.', 'bag zara.', 'wallet gucci.', 'shoe.' , 'pack sack.' , 'backpack.' , 'adidas.', 'bosch', 'samsung', 'Motorola' , 'cap' , 'Shirt', 'jeans', 'Mobile', 'phone', 'Flash disk', 'Hard disk', 'Phillips', 'Mouse']
top_k = min(5, len(corpus))
for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")
    print("\n\n========== semantic search ============\n\n")
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
"""