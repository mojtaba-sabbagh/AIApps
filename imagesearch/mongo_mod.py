from core.mongo_connect import database
image_prefix = "https://anah-v2.s3.amazonaws.com"

def mongo_filter_images(images, top_k):
    """ filter images using mongodb """
    products = []
    prod_ids = {}
    collection = database["products"]
    for image, _ in images:
        if len(products) >= top_k:
            break

        results = collection.find({
                "status": 'Published',
                "uploadedFiles": {
                    "$elemMatch": {
                    "fileUrl": f"{image_prefix}/{image}"
                    }
                }
            })        
        for doc in results:
            if doc['_id'] not in prod_ids:
                prod_ids[doc['_id']] = 1
                products.append({"title" : doc['title'], 
                                           "slug" : doc['slug'],
                                           "price" : doc['price'],
                                           "salePrice" : doc['salePrice']})
    return products