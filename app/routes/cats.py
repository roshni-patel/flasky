from flask import Blueprint, jsonify, request, abort, make_response
from app.models.cats import Cat 
from app import db 
# class Cat:
#     def __init__(self, id, name, age, color):
#         self.id = id
#         self.name = name 
#         self.age = age
#         self.color = color 


# cats = [
#     Cat(1, "Chidi", 0.5, "grey"),
#     Cat(2, "Siba", 3, "orange"),
#     Cat(3, "Tucker", 5, "black")
# ]

cats_bp = Blueprint("cats_bp", __name__, url_prefix="/cats")
@cats_bp.route('', methods=['POST'])
def create_one_cat():
    request_body = request.get_json()
    new_cat = Cat(name=request_body["name"],
                age=request_body["age"],
                color=request_body["color"],
                saying=request_body["saying"])

    # staging
    db.session.add(new_cat)
    db.session.commit()

    return {
        "id": new_cat.id,
        "msg": f"Successfully created cat with id {new_cat.id}"
    }, 201


@cats_bp.route('', methods=['GET'])
def get_all_cats():
    params = request.args
    if "color" in params and "age" in params:
        color_name = params["color"]
        age_value = params["age"]
        cats = Cat.query.filter_by(color=color_name, age=age_value)
    elif "color" in params: 
        color_name = params["color"]
        cats = Cat.query.filter_by(color=color_name)
    elif "age" in params:
        age_value = params["age"]
        cats = Cat.query.filter_by(age=age_value)
    else: 
        cats = Cat.query.all()
    
    cats_response = []

    for cat in cats:
        cats_response.append({
            'id': cat.id,
            'name': cat.name,
            'age': cat.age, 
            'color': cat.color, 
            'saying': cat.saying
        })

    return jsonify(cats_response)

def get_cat_or_abort(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {cat_id}"}
        return abort(make_response(jsonify(rsp), 400))

    chosen_cat = Cat.query.get(cat_id)

    if chosen_cat is None:
        rsp = {"msg": f"Could not find cat with id {cat_id}"}
        return abort(make_response(jsonify(rsp), 404))  

    return chosen_cat 

@cats_bp.route('/<cat_id>', methods=['GET'])
def get_one_cat(cat_id):
    chosen_cat = get_cat_or_abort(cat_id)
    # try:
    #     cat_id = int(cat_id)
    # except ValueError:
    #     rsp = {"msg": f"Invalid id: {cat_id}"}
    #     return jsonify(rsp), 400 

    # chosen_cat = Cat.query.get(cat_id)

    if chosen_cat is None:
        rsp = {"msg": f"Could not find cat with id {cat_id}"}
        return jsonify(rsp), 404 

    rsp = {
        "id": chosen_cat.id, 
        "name": chosen_cat.name,
        "age": chosen_cat.age,
        "color": chosen_cat.color, 
        "saying": chosen_cat.saying

    }

    return jsonify(rsp), 200
    
@cats_bp.route('/<cat_id>', methods=['PUT', 'PATCH'])
def put_one_cat(cat_id):
    try:
        cat_id = int(cat_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {cat_id}"}
        return jsonify(rsp), 400 

    chosen_cat = Cat.query.get(cat_id)

    if chosen_cat is None:
        rsp = {"msg": f"Could not find cat with id {cat_id}"}
        return jsonify(rsp), 404 

    request_body = request.get_json()

    try: 
        chosen_cat.name = request_body["name"]
        chosen_cat.age = request_body["age"]
        chosen_cat.color = request_body["color"]
        chosen_cat.saying = request_body["saying"]

    except KeyError:
        return {
            "msg": "name, age, and color are required"
        }, 400 

    db.session.commit()

    return {
        "msg": f"cat #{chosen_cat.id} successfully replaced"
    }, 200

@cats_bp.route('/<cat_id>', methods=['DELETE']) 
def delete_cat(cat_id): 
    try:
        cat_id = int(cat_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {cat_id}"}
        return jsonify(rsp), 400

    chosen_cat = Cat.query.get(cat_id)
    if chosen_cat is None:
        rsp = {"msg": f"Could not find cat witth id {cat_id}"}
        return jsonify(rsp), 404

    db.session.delete(chosen_cat)
    db.session.commit()

    return {
        "msg": f"cat #{chosen_cat.id} successfully destroyed"
    }, 200

# @cats_bp.route("", methods=["GET"])
# def get_all_cats():
#     cats_response = []
    
#     for cat in cats:
#         cats_response.append({
#             "id": cat.id,
#             "name": cat.name,
#             "age": cat.age, 
#             "color": cat.color
#         })

#     return jsonify(cats_response)

# @cats_bp.route('/<cat_id>', methods=['GET'])
# def get_one_cat(cat_id):
#     try:
#         cat_id = int(cat_id)
#     except ValueError:
#         rsp = {"msg": f"Invalid id: {cat_id}"}
#         return jsonify(rsp), 400 

#     chosen_cat = None 

#     for cat in cats:
#         if cat.id == cat_id:
#             chosen_cat = cat 
#             break 
    
#     if chosen_cat is None:
#         rsp = {"msg": f"Could not find cat with id {cat_id}"}
#         return jsonify(rsp), 404

#     rsp = {
#         'id': chosen_cat.id,
#         'name': chosen_cat.name,
#         'age': chosen_cat.age, 
#         'color': chosen_cat.color 
#     }

#     return jsonify(rsp), 200 


### diff between jsonify and make response
# make response explicitly makes that response - if you use make response and then return that value,
# flask will be like you already did that, throw it out
# can add headers to make response 

# abort is like raising an exception 
# we can pass a response object, it'll end the run of this endpoint and throw that response back
# one of the few places where we have to use make response

# env
# abort
# 