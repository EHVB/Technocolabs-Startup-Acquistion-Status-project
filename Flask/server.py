import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("project.html")


@app.route('/predict', methods=['POST'])
def predict():
    model = pickle.load(open('SVM_pipeline.pkl', 'rb'))

    int_features = request.form.to_dict()
    final_features = list(int_features.values())
    final_features = list(map(float, final_features))
    print(final_features)
    final_features = np.array(final_features).reshape(1, len(final_features))
    prediction = model.predict(final_features)

    if prediction == 1:
        result = 'operating'
    elif prediction == 2:
        result = 'acquired'
    elif prediction == 3:
        result = 'closed'
    elif prediction == 4:
        result = 'ipo'
    else:
        result = 'error'

    return render_template("project.html", prediction_text=result)


if __name__ == "__main__":
    app.run(debug=True)
