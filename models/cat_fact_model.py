from models.cat_fact_detail_model import Verified

class CatFactModel():
    
    def __init__(self, json):
        self.status = Verified(json['status'])
        self.id = json['_id']
        self.text = json['text']
        self.updatedAt = json['updatedAt']
        self.type = json['type']
        self.createdAt = json['createdAt']