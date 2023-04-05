from flask import Flask

app = Flask(__name__)


@app.route('/liveness')
def liveness_response():
    return 'This is the liveness endpoint'


@app.route('/game_prices', methods=["GET"])
def get_game_price():
    pass


if __name__ == '__main__':
    app.run()
