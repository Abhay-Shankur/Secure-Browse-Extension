# QRVerify
This Flask web app generates dynamic QR codes for verification. Users scan the QR codes, triggering data transmission to the app. It verifies the data against Firebase Realtime Database. On success (value=1), users are redirected to an external URL with a popup; otherwise, they return to the QR page.
