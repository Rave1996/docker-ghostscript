import base64
import os
import subprocess
import tempfile
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024  # Customized upload filesize limit - 150mb


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
	response = None

	try:
		if 'file' not in request.files:
			return jsonify({'status': 'error', 'descr': 'No file found.'}), 400

		uploaded_file = request.files['file']

		if uploaded_file.filename == '':
			return jsonify({'status': 'error', 'descr': 'No selected file.'}), 400
		
		if '.' not in uploaded_file.filename:
			return jsonify({'status': 'error', 'descr': 'Unknown file format.'}), 400
		
		if uploaded_file.filename.split('.')[1].lower() != 'pdf':
			return jsonify({'status': 'error', 'descr': 'The uploaded file has an invalid format.'}), 400

		temp_input_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
		input_pdf_path = temp_input_pdf.name
		uploaded_file.save(input_pdf_path)

		temp_output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
		output_file = temp_output_pdf.name

		cmd = f'gs -sDEVICE=pdfwrite -sOutputFile={output_file} {input_pdf_path}'
		cmd = cmd.split()

		subprocess.run(cmd, check=True)

		pdf_content = None

		with open(output_file, 'rb') as f:
			pdf_content = f.read()

		pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

		os.remove(input_pdf_path)
		os.remove(output_file)

		response = jsonify({'status': 'ok', 'pdf': pdf_base64})
	except Exception as exc:
		return jsonify({'status': 'error', 'descr': str(exc)}), 500
	
	return response


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
	return render_template('uploader.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
