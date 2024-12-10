from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import numpy as np
import json

app = Flask(__name__)

# Dummy data
data = {
    "cancer_types": ["Lung", "Breast", "Colon"],
    "insurance_types": ["Medicare", "Medicaid", "Private"],
    "regions": ["Northeast", "South", "Midwest", "West"],
    "employment_statuses": ["Employed", "Unemployed"],
    "highest_degrees": ["High School", "Bachelor's", "Master's", "Doctorate"],
    "family_sizes": list(range(1, 8)),
    "ages": list(range(20, 81)),
    "genders": ['male', 'female'],
    "income_levels": ["<30k", "30k-60k", "60k-100k", "100k+"],
    "dummy_amounts": [1000, 2000, 3000, 4000, 5000],
    'races': ['white', 'black', 'asian', 'other']
}

@app.route('/')
def index():
    return render_template('index.html', cancer_types=data['cancer_types'], employment_statuses=data['employment_statuses'], highest_degrees=data['highest_degrees'], insurance_types=data['insurance_types'], regions=data['regions'], genders=data['genders'], races=data['races'])

@app.route('/get_eda_plots', methods=['POST'])
def get_eda_plots():
    cancer_type = request.json['cancer_type']

    # Generate dummy plots for all EDA types
    figures = {}

    # Coverage vs Race
    figures['race'] = go.Figure(data=[
        go.Bar(name=race, x=data['insurance_types'], y=data['dummy_amounts'])
        for race in data['races']
    ])
    figures['race'].update_layout(title='Coverage vs Race', barmode='group')

    # Coverage vs Region
    figures['region'] = go.Figure(data=[
        go.Bar(name=region, x=data['insurance_types'], y=data['dummy_amounts'])
        for region in data['regions']
    ])
    figures['region'].update_layout(title='Coverage vs Region', barmode='group')

    # Coverage vs Employment Status
    figures['employment_status'] = go.Figure(data=[
        go.Bar(name=status, x=data['insurance_types'], y=data['dummy_amounts'])
        for status in data['employment_statuses']
    ])
    figures['employment_status'].update_layout(title='Coverage vs Employment Status', barmode='group')

    # Amount vs Highest Degree Obtained
    figures['degree'] = go.Figure(data=[
        go.Bar(x=data['highest_degrees'], y=data['dummy_amounts'])
    ])
    figures['degree'].update_layout(title='Amount vs Highest Degree Obtained')

    # Amount vs Family Size
    figures['family_size'] = go.Figure(data=[
        go.Histogram(x=data['family_sizes'], y=data['dummy_amounts'])
    ])
    figures['family_size'].update_layout(title='Amount vs Family Size')

    # Amount vs Age
    figures['age'] = go.Figure(data=[
        go.Histogram(x=data['ages'], y=data['dummy_amounts'])
    ])
    figures['age'].update_layout(title='Amount vs Age')

    # Total Out-of-Pocket vs Income
    figures['income'] = go.Figure(data=[
        go.Scatter(x=data['income_levels'], y=data['dummy_amounts'], mode='lines+markers')
    ])
    figures['income'].update_layout(title='Total Out-of-Pocket vs Income')

    # Convert all figures to JSON
    response = {key: json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)) for key, fig in figures.items()}
    return jsonify(response)

@app.route('/predict_toxicity', methods=['POST'])
def predict_toxicity():
    user_input = request.json
    print(user_input)
    toxicity_fraction = np.random.uniform(0, 1) # Replace with actual prediction logic
    return jsonify({"toxicity": toxicity_fraction})

if __name__ == '__main__':
    app.run(debug=True)
