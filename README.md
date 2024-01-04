# QRVerify
The project is a Flask web application designed to serve as a verification system. The application generates a dynamic QR code on a dedicated page. Users can scan this QR code with a mobile application, triggering the transmission of data to the web page. The application then verifies the received data, particularly checking a value in the Firebase Realtime Database associated with the scanned QR code.

If the verification is successful (the value in the database is 1), the user is redirected to a specified external URL, accompanied by a popup notification. In case of unsuccessful verification, the user is redirected back to the original QR code page.

Key features include periodic regeneration of the QR code, storage of verification tokens in Firebase Realtime Database, and an asynchronous mechanism for checking and handling verification results. The project aims to provide a secure and dynamic verification system with real-time interaction between the web application and external QR-scanning devices.
