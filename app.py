import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Placeholder scoring logic using simple NLP heuristics
def score_response(response):
    fluency = round(6.5 + 0.5 * (len(response.split()) > 20), 1)
    lexical = round(6.5 + 0.5 * ("however" in response.lower()), 1)
    grammar = round(6.5 + 0.5 * ("because" in response.lower()), 1)
    pronunciation = 7.0  # Static placeholder
    overall = round((fluency + lexical + grammar + pronunciation) / 4, 1)

    # Placeholder feedback
    errors = "Minor grammatical issues and limited lexical variety."
    corrected = "Use more varied sentence structures and precise vocabulary."
    improvement = "Incorporate complex grammar and idiomatic expressions."
    feedback = "Response is generally clear but could benefit from more advanced vocabulary and grammar."

    return pd.Series([
        fluency, lexical, grammar, pronunciation, overall,
        errors, corrected, improvement, feedback
    ])

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_csv(file)

    df[['Fluency & Coherence', 'Lexical Resource', 'Grammatical Range & Accuracy',
        'Pronunciation', 'Overall Band Score Estimate',
        'Errors and Why They Affect the Score',
        'Corrected Answer (Band 7+)',
        'What the Candidate Should Have Done to Achieve 7+',
        'In-Depth Feedback and Areas for Improvement']] = df['Response'].apply(score_response)

    feedback_data = df.to_dict(orient='records')
    return render_template('feedback_table.html', feedback_data=feedback_data)

if __name__ == '__main__':
    app.run(debug=True)
