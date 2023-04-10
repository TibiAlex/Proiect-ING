from flask import Flask, jsonify, render_template, request
import requests
import json

app = Flask(__name__)


@app.route('/liveness')
def liveness_response():
    return 'This is the liveness endpoint'


@app.route('/posts', methods=["GET"])
def get_dog_facts():
    url = 'https://jsonplaceholder.typicode.com/posts'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        return render_template('index.html', data=json.dumps(data, indent=4))
    else:
        return 'Failed to retrieve data from API'


@app.route('/post_a_post', methods=["GET", "POST"])
def create_user():
    url = 'https://jsonplaceholder.typicode.com/posts'

    uid = request.args.get('userID')
    id = request.args.get("id")
    title = request.args.get("title")
    body = request.args.get("body")

    data_to_post = {
        "userID": uid,
        "id": id,
        "title": str(title),
        "body": str(body)
    }

    post = requests.post(url, data=json.dumps(data_to_post))
    if post.status_code == 201:  # code for post on this api
        return "Created the new user"
    else:
        return "Failed to create user"


@app.route('/delete_post', methods=["GET", "DELETE"])
def delete_post():
    id_to_delete = int(request.args.get("id"))
    url = f'https://jsonplaceholder.typicode.com/posts/{id_to_delete}'

    delete = requests.delete(url)

    if delete.status_code == 200:
        return "Post deleted successfully"
    else:
        return "Couldn't delete post"


@app.route('/put_post', methods=["GET", "PUT"])
def put_post():
    id_to_update = int(request.args.get("id"))
    url = f'https://jsonplaceholder.typicode.com/posts/{id_to_update}'

    uid = request.args.get('userID')
    id = request.args.get("id")
    title = request.args.get("title")
    body = request.args.get("body")

    data_to_put = {
        "userID": uid,
        "id": id,
        "title": str(title),
        "body": str(body)
    }

    put = requests.put(url, data=json.dumps(data_to_put))

    if put.status_code == 200:
        return "The post has been updated with the new content"
    else:
        return "Couldn't update post"


@app.route('/patch_post', methods=["GET", "PATCH"])
def patch_post():
    id_to_update = int(request.args.get("id"))
    field_to_update = request.args.get("field")
    value = request.args.get("value")
    url = f'https://jsonplaceholder.typicode.com/posts/{id_to_update}'

    data = {
        field_to_update: value
    }

    patch = requests.patch(url, data=json.dumps(data))

    if patch.status_code == 200:
        return "The post has been updated with the new content"
    else:
        return "Couldn't update post"


if __name__ == '__main__':
    app.run()
