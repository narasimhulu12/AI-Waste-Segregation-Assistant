from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("waste_dataset.csv")

# HTML frontend
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI-Based Waste Segregation Assistant</title>
</head>
<body>
    <h2>AI-Based Waste Segregation Assistant</h2>

    <form method="post">
        <input type="text" name="item" placeholder="Enter waste item" required>
        <button type="submit">Classify Waste</button>
    </form>

    {% if result %}
        <h3>Result:</h3>
        <p><b>Input Item:</b> {{ result.item }}</p>
        <p><b>Category:</b> {{ result.category }}</p>
        <p><b>Disposal:</b> {{ result.disposal }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        item = request.form["item"].strip().lower()

        matched_row = data[data["item"].str.lower() == item]

        if not matched_row.empty:
            result = {
                "item": item,
                "category": matched_row.iloc[0]["category"],
                "disposal": matched_row.iloc[0]["disposal"]
            }
        else:
            result = {
                "item": item,
                "category": "Unknown",
                "disposal": "Consult local waste management guidelines"
            }

    return render_template_string(HTML_PAGE, result=result)

@app.route("/predict", methods=["POST"])
def predict():
    user_input = request.json.get("item", "").strip().lower()

    matched_row = data[data["item"].str.lower() == user_input]

    if not matched_row.empty:
        return jsonify({
            "item": user_input,
            "category": matched_row.iloc[0]["category"],
            "disposal": matched_row.iloc[0]["disposal"]
        })

    return jsonify({
        "item": user_input,
        "category": "Unknown",
        "disposal": "Consult local waste management guidelines"
    })

if __name__ == "__main__":
    app.run(debug=True)
