from flask import Flask, request, jsonify
import json


app = Flask(__name__)
with open("restaurants.json", "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


@app.route('/api/restaurants', methods=['GET', 'POST'])
def all_restaurants():
    if request.method == 'POST':
        content = request.json
        if content is not None:
            restaurants[str(len(restaurants))] = content['restaurant_info']
        return jsonify({'restaurants': restaurants}), 201
    else:
        return jsonify({'restaurants': restaurants}), 200


@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET', 'PUT'])
def get_info(restaurant_id):
    if request.method == 'PUT':
        content = request.json
        if content is not None:
            restaurants[restaurant_id] = content['restaurant_name']
        return jsonify({'restaurants': restaurants}), 200
    else:
        return jsonify({'info': restaurants[restaurant_id]}), 200


if __name__ == '__main__':
    app.run()
