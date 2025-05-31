from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

surveys = []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    # Validate required fields
    required_fields = ['fullname', 'email', 'contact', 'date', 'age', 'food', 'eatout', 'movies', 'tv', 'radio']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    # Validate age range
    age = data['age']
    if age < 5 or age > 120:
        return jsonify({'message': 'Age must be between 5 and 120.'}), 400

    # Validate food list not empty
    if not data['food']:
        return jsonify({'message': 'At least one favorite food must be selected.'}), 400

    # Append survey
    surveys.append(data)
    return jsonify({'message': 'Survey submitted successfully!'})

@app.route('/results', methods=['GET'])
def results():
    if not surveys:
        return jsonify({'message': 'No Surveys Available', 'total': 0})

    total = len(surveys)
    ages = [s['age'] for s in surveys]
    avg_age = round(sum(ages) / total, 1)
    oldest = max(ages)
    youngest = min(ages)

    # Percentage who like pizza
    pizza_count = sum('Pizza' in s['food'] for s in surveys)
    pizza_percent = round((pizza_count / total) * 100, 1)

    # Average 'eatout' rating
    eatout_avg = round(sum(int(s['eatout']) for s in surveys) / total, 2)

    return jsonify({
        'total': total,
        'avg_age': avg_age,
        'oldest': oldest,
        'youngest': youngest,
        'pizza_percent': pizza_percent,
        'eatout_avg': eatout_avg
    })

if __name__ == '__main__':
    app.run(debug=True)