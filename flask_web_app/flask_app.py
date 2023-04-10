from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)


@app.route('/liveness')
def liveness_response():
    return 'This is the liveness endpoint'


@app.route('/posts', methods=["GET"])
def get_posts():
    if os.path.exists('main_page_data.json'):
        with open('main_page_data.json', 'r') as file:
            json_file = json.load(file)  # list of dictionaries
            indented_data = json.dumps(json_file, indent=4)
        return render_template('index.html', data=indented_data)
    else:
        url = 'https://jsonplaceholder.typicode.com/posts'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            indented_data = json.dumps(data, indent=4)

            with open('main_page_data.json', 'w') as file:
                file.write(indented_data)

            return render_template('index.html', data=indented_data)
        else:
            return 'Failed to retrieve data from API'


@app.route('/post_a_post', methods=["GET", "POST"])
def create_user():
    url = 'https://jsonplaceholder.typicode.com/posts'

    uid = int(request.args.get('userID'))
    id = int(request.args.get("id"))
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
        with open('main_page_data.json', 'r+') as file:
            json_dict = json.load(file)
            json_dict.append(data_to_post)
            file.seek(0)
            json.dump(json_dict, file, indent=4)

        return "Created the new user"
    else:
        return "Failed to create user"


@app.route('/delete_post', methods=["GET", "DELETE"])
def delete_post():
    id_to_delete = int(request.args.get("id"))
    url = f'https://jsonplaceholder.typicode.com/posts/{id_to_delete}'

    delete = requests.delete(url)
    if delete.status_code == 200:
        with open("main_page_data.json", "r+") as file:
            dict_list = json.load(file)
            for index in range(len(dict_list)):
                if dict_list[index]["id"] == id_to_delete:
                    del dict_list[index]
                    break
            file.truncate(0)  # sterg ce aveam in fisier pentru ca imi va ramane ceva la sfarsit daca suprascriu
            file.seek(0)
            json.dump(dict_list, file, indent=4)

        return "Post deleted successfully"
    else:
        return "Couldn't delete post"


@app.route('/put_post', methods=["GET", "PUT"])
def put_post():
    id_to_update = int(request.args.get("pid"))
    url = f'https://jsonplaceholder.typicode.com/posts/{id_to_update}'

    uid = int(request.args.get('userID'))
    id = int(request.args.get("id"))
    title = request.args.get("title")
    body = request.args.get("body")

    data_to_put = {
        "userId": uid,
        "id": id,
        "title": str(title),
        "body": str(body)
    }

    put = requests.put(url, data=json.dumps(data_to_put))

    if put.status_code == 200:
        with open("main_page_data.json", "r+") as file:
            dict_list = json.load(file)
            for index in range(len(dict_list)):
                if dict_list[index]["id"] == id_to_update:
                    dict_list[index]["userId"] = uid
                    dict_list[index]["id"] = id
                    dict_list[index]["title"] = title
                    dict_list[index]["body"] = body
            file.truncate(0)
            file.seek(0)
            json.dump(dict_list, file, indent=4)
        return "The post has been updated with the new content"
    else:
        return "Couldn't update post"


@app.route('/patch_post', methods=["GET", "PATCH"])
def patch_post():
    id_to_update = int(request.args.get("id"))
    field_to_update = str(request.args.get("field"))
    value = request.args.get("value")
    url = f'https://jsonplaceholder.typicode.com/posts/{id_to_update}'
    types = {
        "userID": "int",
        "id": "int",
        "title": "str",
        "body": "str"
    }

    data = {
        field_to_update: eval(f"{types[field_to_update]}")(value)
    }

    patch = requests.patch(url, data=json.dumps(data))

    if patch.status_code == 200:
        with open("main_page_data.json", "r+") as file:
            dict_list = json.load(file)
            for index in range(len(dict_list)):
                if dict_list[index]["id"] == id_to_update:
                    dict_list[index][field_to_update] = data[field_to_update]
            file.truncate(0)
            file.seek(0)
            json.dump(dict_list, file, indent=4)
        return "The post has been updated with the new content"
    else:
        return "Couldn't update post"


if __name__ == '__main__':
    app.run()
