from flask import Flask, redirect, url_for, flash, send_from_directory, render_template, request
import urllib.request
from werkzeug.utils import secure_filename
import mainsud
import os

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	flash("Home")
	return render_template('index.html')

@app.route('/solve', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('Image successfully uploaded and displayed below')
		image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		paths, names = create_path_name(filename)
		result = mainsud.process_sudoku(image_path, paths)
		print("paths: ",paths)
		print("names: ",names)
		return render_template('solve.html', filename=names, result=result)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def create_path_name(name):
	paths = []
	names = []
	name_part = name.rsplit('.', 1)
	for i in range(1,5):
		names.append(f'{str(name_part[0])}_{str(i)}.png')
		paths.append(os.path.normpath(app.config['UPLOAD_FOLDER']+str(names[i-1])))

	return paths, names

def remove_files(filename,paths):
	os.unlink(os.path.join(app.config['UPLOAD_FOLDER'], ))

if __name__ == "__main__":
	app.run(debug=True)