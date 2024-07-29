

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from urllib.parse import quote_plus
import os
import time
#using flaskAPIs
app = Flask(__name__)

# MongoDB Atlas credentials
username = "pgkhadgi2002"
password = "Pgk#4321"
uri = f"mongodb+srv://pgkhadgi2002:Pgk#4321@cluster0.oaw7roj.mongodb.net/"
#mongodb+srv://pgkhadgi2002:Pgk#4321@cluster0.oaw7roj.mongodb.net/
client = MongoClient(uri)

# Specify the database and collection
db = client['pgkhadgi2002']
collection = db['peppermint_career_data']

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'public'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve static files from the "public" directory
@app.route('/public/<path:filename>', methods=['GET'])
def static_files(filename):
    return send_from_directory(STATIC_FOLDER, filename)

# Endpoint to handle form submission
@app.route('/apply', methods=['POST'])
def apply():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    position = request.form.get('position')
    coverLetter = request.form.get('coverLetter')
    resume = request.files.get('resume')

    if resume and allowed_file(resume.filename):
        filename = secure_filename(resume.filename)
        resume_filename = f"{int(time.time())}-{filename}"
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))
    else:
        resume_filename = None

    application_data = {
        'id': int(time.time()),
        'name': name,
        'email': email,
        'phone': phone,
        'position': position,
        'coverLetter': coverLetter,
        'resumePath': resume_filename
    }

    # Insert the application data into MongoDB
    try:
        result = collection.insert_one(application_data)
        application_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
    except Exception as e:
        print(f"Failed to save application data to MongoDB: {e}")
        return 'Failed to submit application. Please try again.', 500

    return jsonify(application_data), 200

# Start the server
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)


# #link to access ==> http://127.0.0.1:5000/public/index.html