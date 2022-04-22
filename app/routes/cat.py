from flask import Blueprint, jsonify

class Cat:
    def __init__(self, id, name, age, color):
        self.id = id
        self.name = name 
        self.age = age
        self.color = color 


cats = [
    Cat(1, "Chidi", 0.5, "grey"),
    Cat(2, "Siba", 3, "orange"),
    Cat(3, "Tucker", 5, "black")
]

cats_bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

@cats_bp.route("", methods=["GET"])
def get_all_cats():
    cats_response = []
    
    for cat in cats:
        cats_response.append({
            "id": cat.id,
            "name": cat.name,
            "age": cat.age, 
            "color": cat.color
        })

    return jsonify(cats_response)