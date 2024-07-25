from bson.objectid import ObjectId
try:
    from augimagesearch.mongo_connect import database
except:
    database = None
import re

product = {
    "title" : 'N/A', 
    "slug" : 'N/A',
    "price" : 0,
    "salePrice" : 0,
    "uploadedFiles": [],
    "outOfStockDate": None,
    "stockStatus": '',
    "productLabels": '',
    "categories": []
}
collection = database["products"]
collection_labels = database["productLabels"]
def mongo_filter_images(images, top_k):
    """ filter images using mongodb """
    empty_product = product.copy()
    if database is None:
        empty_product["uploadedFiles"] = [image[1] for image in images]
        return [empty_product]
    
    products = []
    prod_ids = {}
    for _, image in images:
        if len(products) >= top_k:
            break
        image = "".join(image.split('.')[:-1])
        regx = re.compile(f".*{image}.*", re.IGNORECASE)
        results = collection.find({
                "status": 'Published',
                "uploadedFiles": {
                    "$elemMatch": {
                    "fileUrl": regx 
                    }
                }
            })        
        for doc in results:
            if doc['_id'] not in prod_ids:
                prod_ids[doc['_id']] = 1
                file_urls = [uploaded_file["fileUrl"] for uploaded_file in doc["uploadedFiles"] ]
                empty_product["title"] = doc['title']
                empty_product["slug"] = doc['slug']
                empty_product["price"] = doc['price']
                empty_product["salePrice"] = doc['salePrice']
                empty_product["uploadedFiles"] = file_urls
                empty_product["outOfStockDate"] = '' if doc['outOfStockDate'] is None else doc['outOfStockDate']
                empty_product["stockStatus"] = doc['stockStatus']
                empty_product["productLabels"] = extract_productLabels(doc['productLabels'])
                empty_product["categories"] = doc['categories']
                products.append(empty_product)
                empty_product = product.copy()
    return products

def extract_productLabels(prodlabel):
    result = collection_labels.find_one({
                "_id": ObjectId(prodlabel),
            })
    if result is not None:
        return result['name']
    return ''
