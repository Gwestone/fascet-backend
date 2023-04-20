from flask import Flask, request, make_response

from mosaic import generate_mosaics

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/mosaics/voronoi', methods=['POST'])
def voronoi():
    # print(request.json['base64_image'])
    image = request.json['base64_image']
    responce = make_response(generate_mosaics(image), 200)
    responce.mimetype = "text/plain"
    return responce

if __name__ == '__main__':
    app.run(host="0.0.0.0")
