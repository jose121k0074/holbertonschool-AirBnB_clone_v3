#!/usr/bin/python3
"""Flask app to manipulate Amenity objects"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieves_all_amenities():
    """Returns the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """Returns amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", 
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    elif "name" not in amenity_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    amenity_data = request.get_json()
    if not amenity:
        abort(404)
    elif not amenity_data:
        abort(400, "Not a JSON")

    for key, value in amenity_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
