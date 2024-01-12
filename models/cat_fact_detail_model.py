class Verified():
    def __init__(self, json):
        self.verified = json["verified"]
        self.sentCount = json["sentCount"]

class User():
    def __init__(self, json):
        self.first = json["name"]["first"]
        self.last = json["name"]["last"]
        self.id = json["_id"]
        self.photo = json["photo"]
        
class CatFactDetailModel():
    def __init__(self, json):
        print(json["user"]) if "user" in json else User({
            "name": {
                "first": "Unknown",
                "last": "Unknown"
            },
            "_id": "Unknown",
            "photo": "Unknown"
        })
        self.user = User(json["user"])
        self.id = json["_id"]
        self.text = json["text"]
        self.source = json["source"] if "source" in json else ""
        self.updatedAt = json["updatedAt"]
        self.type = json["type"]
        self.createdAt = json["createdAt"]
        self.deleted = json["deleted"]
        self.status = Verified(json["status"])

