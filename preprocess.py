import joblib

model_path = 'phishing.pkl'
phish_model = joblib.load(open(model_path, 'rb'))


def predictRes(url):
    # Perform prediction using the loaded model
    url = url.replace('https://', '')
    prediction = phish_model.predict([url])[0]
    return prediction