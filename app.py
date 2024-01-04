import os
import time
import threading
import urllib
import asyncio
import qrcode
import json
import random
import string
from flask import Flask, render_template, request, redirect, url_for, jsonify

from firebase_operations import RealtimeDatabaseListener

app = Flask(__name__)
fb_rd = RealtimeDatabaseListener()

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {'databaseURL': 'https://detect-f07fd-default-rtdb.firebaseio.com'})

# List of protected URLs
protected_urls = [
    "https://www.youtube.com",
    # Add other URLs as needed
]

# Function to generate dynamic QR code content
def generate_qr_code_content():
    # Include some dynamic data, e.g., timestamp or random token
    dynamic_data = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # JSON content for the QR code
    content_dict = {
        "type": ["VerifiableCredential", "Degree"],
        "token": dynamic_data
    }
    content_json = json.dumps(content_dict)

    # Store the token in Firebase Realtime Database
    fb_rd.add_value(path='/Tokens', data={dynamic_data: -1})


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


@app.route('/qr_code')
def qr_code():
    # Pass the dynamic QR code URL to the template
    generate_qr_code_content()
    qr_code_content = getattr(app, 'content', None)
    next_url = getattr(app, 'next_url', '')
    
    # Retrieve the latest token from Firebase Realtime Database
    location = '/Tokens/'+qr_code_content['token']

    return render_template('qr_code.html', location=location, next_url=next_url)

@app.route('/check_value')
def check_value():
    # Retrieve the location from the query parameters
    location = request.args.get('location')
    result = fb_rd.start_listener(location=location)
    return jsonify({'value': result})


if __name__ == '__main__':
    app.run(debug=True)
