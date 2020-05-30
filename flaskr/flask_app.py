import os
import pathlib
import sqlite3

from flask import flash
from flask import Flask
from flask import g
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
from flask import url_for
from werkzeug.utils import secure_filename

# from primely.controller import controller
# from primely.tools import utils
# from primely import controller, cli
import primely.controller
import primely.cli


UPLOAD_FOLDER = 'data/input/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""Checks"""
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""API"""
@app.route('/')
@app.route('/api', methods=['GET', 'POST', 'DELETE'])
def home():
    return render_template(
        'index.html'
    )

#Upload
@app.route('/api/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the name of the uploaded files
        # print('request:', request.files)
        # print('request.form:', request.form)

        # Create data/input directory
        primely.cli.create_data_dir()
        
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Save the filename into a list, we'll use it later
                filenames.append(filename)
                # Redirect the user to the uploaded_file route, which
                # will basicaly show on the browser the uploaded file
        # Load an html page with a link to each uploaded file
        return redirect('/')
        # return 'Upload complete', 200

#Run
@app.route('/api/convert', methods=['GET'])
def run_conversion():
    if request.method == 'GET':
        conversion = primely.controller.paycheck_analysis('object')
        if not conversion:
            return "No", 404

        return 'conversion success', 200

#View
@app.route('/api/report', methods=['GET'])
def download_file():
    if request.method == 'GET':
        res = primely.cli.get_json_timechart()
        if not res:
            return "No", 404

        return jsonify(res), 200

#Reset
@app.route('/api/reset', methods=['DELETE'])
def reset_report():
    if request.method == 'DELETE':
        reset = primely.cli.remove_report()
        if not reset:
            return "No", 404

        return 'Report deleted', 200

#Delete
@app.route('/api/delete', methods=['DELETE'])
def delete_pdf():
    if request.method == 'DELETE':
        reset = primely.cli.remove_pdf()
        if not reset:
            return "No", 404

        return 'PDF deleted', 200


def main():
    app.debug = True
    app.run()



if __name__ == "__main__":
    main()