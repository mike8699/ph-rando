from io import BytesIO

from flask import Flask, render_template, request, jsonify, send_file

from randomize import randomize

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/randomize', methods=['POST'])
def randomize_game():
    if 'file' not in request.files:
        return jsonify('Error: no game supplied'), 400
    file = request.files['file']
    new_rom = randomize(file.read())
    # print(new_rom)
    # return jsonify('Success')
    return send_file(BytesIO(new_rom), as_attachment=True, attachment_filename="ph_rando.nds")
