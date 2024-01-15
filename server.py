import json
import os
import random
import string

import qrcode
from flask import Flask, render_template, request, jsonify

from handlers.organization import Organization

app = Flask(__name__)
# fb = RealtimeDatabaseListener()
# admin = Admin()
app_name = 'QRVerify'
# fb = FirebaseOperations(app_name=app_name)
org = Organization(app_name=app_name)
# handler = ApiHandler(fb)

# List of protected URLs
if org.is_logged_in():
    protected_urls = org.get_url()
else:
    protected_urls = [
        "https://www.youtube.com",
    ]


# Function to generate dynamic QR code content
def generate_qr_code_content():
    # Include some dynamic data, e.g., timestamp or random token
    dynamic_data = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # JSON content for the QR code
    content_dict = {
        "type": ["VerifiableCredential", "Degree"],
        "token": dynamic_data,
        "next_url": getattr(app, 'next_url', ''),
    }
    content_json = json.dumps(content_dict)

    # Store the token in Firebase Realtime Database
    # fb.add_value(path='/Tokens', data={dynamic_data: content_dict})
    # fb.add_doc(collection_name='Tokens', doc=content_dict, doc_id=dynamic_data)
    org.firebaseHandler.add_doc(collection_name='Tokens', doc=content_dict, doc_id=dynamic_data)

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content_json)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    img_path = os.path.join("static", "dynamic_qr_code.png")
    img.save(img_path)

    # Broadcast the new QR code URL to connected clients
    with app.app_context():
        app.qr_code_img_path = img_path
        app.content = content_dict


@app.route('/check_url', methods=['POST'])
def protected_redirect():
    data = request.get_json()
    url = data.get('url', '')

    with app.app_context():
        app.next_url = url

    # Perform URL protection check
    protected = any(url.startswith(prefix) for prefix in protected_urls)

    return jsonify({'protected': protected})


@app.route('/qr_code', methods=['GET', 'POST'])
def qr_code():
    # Pass the dynamic QR code URL to the template
    generate_qr_code_content()
    qr_code_content = getattr(app, 'content', None)
    next_url = getattr(app, 'next_url', '')

    if request.method == 'POST':
        data = request.get_json()
        next_url = data.get('next_url', '')

    # Retrieve the latest token from Firebase Realtime Database
    # location = '/Tokens/' + qr_code_content['token']
    token = qr_code_content['token']

    # return render_template('qr_code.html', location=location, next_url=next_url)
    return render_template('qr_code.html', token=token, next_url=next_url)


@app.route('/check_value', methods=['GET'])
def check_value():
    # Retrieve the location from the query parameters
    token = request.args.get('token')

    result = org.firebaseHandler.get_updated_document(collection_name='Tokens', document_id=token)

    with app.app_context():
        app.next_url = result.get('next_url','')

    result = result.get('verified', False)

    org.firebaseHandler.close_connection()

    return jsonify({'verified': result})


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
        # sender_id = request.form['sender_id']
        # data = {
        #     "aadhar": request.form['adhar_number'],
        #     "name": request.form['name'],
        #     "email": request.form['gmail'],
        #     "role": "User",
        #     "dob": request.form['dob']
        # }
        # handler = Admin()
        # handler.issue_credentials(subjectDid=sender_id, fields=data)
    # collections=[fd.get_matching_doc(collection_name=collection) for collection in fd.get_all_collections()]
    # collections = handler.get_status()
    collections = ''
    # return render_template('index.html', collections=collections)
    return render_template('dashboard.html', collections=collections)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html')


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        pass
    else:
        return render_template('join.html')
# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         pass
#     return render_template('create.html')
#
#
# @app.route('/issue', methods=['GET', 'POST'])
# def issue():
#     if request.method == 'POST':
#         pass
#     return render_template('issue.html')




if __name__ == '__main__':
    app.run(debug=True)
