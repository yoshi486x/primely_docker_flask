import os
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

from primely.controller import controller
from primely.views import response
from tools import remover

UPLOAD_FOLDER = 'data/input/'
DOWNLOAD_FOLDER = 'data/output/json/paycheck_timechart.json'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""Checks"""
# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

"""API"""
@app.route('/')
@app.route('/api', methods=['GET', 'POST', 'DELETE'])
def home():
    return render_template(
        'index.html'
    )

@app.route('/api/convert', methods=['GET'])
def run_conversion():
    if request.method == 'GET':
        conversion = controller.paycheck_analysis()
        if not conversion:
            return "No", 404

        return 'conversion success', 200

@app.route('/api/reset', methods=['DELETE'])
def reset_report():
    if request.method == 'DELETE':
        reset = remover.remove_report()
        if not reset:
            return "No", 404

        return 'Report deleted', 200

@app.route('/api/delete', methods=['DELETE'])
def delete_pdf():
    if request.method == 'DELETE':
        reset = remover.remove_pdf()
        if not reset:
            return "No", 404

        return 'PDF deleted', 200


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the name of the uploaded files
        print('request:', request.files)
        print('request.form:', request.form)
        
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


@app.route('/test/uploads', methods=['GET', 'POST'])
def test_upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print('request.files:', request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            return 'Upload success', 200
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple=multiple>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/report', methods=['GET'])
def download_file():
    if request.method == 'GET':
        res = response.get_json_timechart()
        if not res:
            return "No", 404

        return jsonify(res), 200

@app.route('/ajax/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/ajax')
def ajax():
    return render_template('ajax.html')

def main():
    app.debug = True
    app.run()



if __name__ == "__main__":
    main()