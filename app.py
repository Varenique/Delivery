from flask import Flask, request
import json


app = Flask(__name__)
with open("restaurants.json", "r") as read_file:
    data = json.load(read_file)

restaurants = data['restaurants']


@app.route('/api/restaurants', methods=['GET', 'POST'])
def all_restaurants():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        print(type(content))
        if content is not None:
            print(content)
            restaurants.append(content['restaurant_name'])
        response = app.response_class(
            response=json.dumps({'restaurants': restaurants}),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response = app.response_class(
            response=json.dumps({'restaurants': restaurants}),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET', 'PUT'])
def get_info(restaurant_id):
    if request.method == 'PUT':
        content = request.get_json(silent=True)
        if content is not None:
            restaurants[restaurant_id] = content['restaurant_name']
        response = app.response_class(
            response=json.dumps({'restaurants': restaurants}),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response = app.response_class(
            response=json.dumps({'info': restaurants[restaurant_id]}),
            status=200,
            mimetype='application/json'
        )
        return response


if __name__ == '__main__':
    app.run()
