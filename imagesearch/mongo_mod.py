from core.mongo_connect import database
import re



def mongo_filter_images(images, top_k):
    """ filter images using mongodb """
    products = []
    prod_ids = {}
    collection = database["products"]
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
                products.append({"title" : doc['title'], 
                                 "slug" : doc['slug'],
                                 "price" : doc['price'],
                                 "salePrice" : doc['salePrice'],
                                 "uploadedFiles": file_urls})
    return products