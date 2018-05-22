from flask import Flask, request, Response
import os

app = Flask(__name__)


@app.route('/predictions', methods=['GET'])
def prediction_page():
    with open('page.html', 'r') as f:
        page = f.read()
        return page


def start():
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    start()
