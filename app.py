from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import numpy as np
import json
from generate_plotting_data import generate_plotting_data, cancer_name_map, highest_degrees, race_mapping, region_map, gender_map, reverse_map
import pickle

app = Flask(__name__)

# Dummy data
features = {
    "cancer_types": list(cancer_name_map.keys()),
    "insurance_types": ['uninsured', 'private', 'medicaid', 'medicare', 'other_public', 'tricare', 'hmo_public', 'other_paid'],
    "regions": list(region_map.values()),
    "employment_statuses": ["employed", "unemployed", "other"],
    "highest_degrees": highest_degrees, # index + 1 is the code
    "family_sizes": list(range(1, 8)),
    "genders": list(gender_map.values()),
    "income_levels": ["<30k", "30k-60k", "60k-100k", "100k+"],
    "races": race_mapping.values(),
}

model = None
scaler_model = None
cancer_label_encoder = insurance_label_encoder = None

def load_model(path_root='saved_model/'):
  global model, scaler_model

  with open(path_root + "best_model.pkl", "rb") as f:
    model = pickle.load(f)
    print("loaded trained model")
  with open(path_root + 'scaler_model.pickle', "rb") as f:
    scaler_model = pickle.load(f)

  with open(path_root + "cancer_label_encoder.pkl", "wb") as f:
    cancer_label_encoder = pickle.load(f)

  with open(path_root + "insurance_label_encoder.pkl", "wb") as f:
    insurance_label_encoder = pickle.load(f)

  

reverse_gender_map = reverse_race_map = reverse_highest_degree_map = reverse_region_map = reverse_cancer_map = reverse_employment_status = None

def build_reverse_maps():
  global reverse_gender_map, reverse_race_map, reverse_highest_degree_map, reverse_region_map, reverse_cancer_map, reverse_employment_status
  reverse_gender_map, reverse_map(gender_map)
  reverse_race_map = reverse_map(race_mapping)
  reverse_highest_degree_map = {deg: i for i, deg in enumerate(highest_degrees, 1)}
  reverse_region_map = reverse_map(region_map)
  reverse_cancer_map = reverse_map(cancer_name_map)
  reverse_employment_status = {"employed": 3, "unemployed": 0, "other": -1}


@app.route("/")
def index():
    return render_template(
        "index.html",
        cancer_types=features["cancer_types"],
        employment_statuses=features["employment_statuses"],
        highest_degrees=features["highest_degrees"],
        insurance_types=features["insurance_types"],
        regions=features["regions"],
        genders=features["genders"],
        races=features["races"],
    )


@app.route("/get_eda_plots", methods=["POST"])
def get_eda_plots():
    cancer_type = request.json["cancer_type"]


    generated_data = generate_plotting_data("data/processed/results.csv", cancer_type)


    # Generate dummy plots for all EDA types
    figures = {}

    # Coverage vs Race
    figures["race"] = go.Figure(
        data=[
            go.Bar(name=race_name, x=list(data.keys()), y=list(data.values()))
            for race_name, data in generated_data["race"].items()
        ]
    )
    figures["race"].update_layout(title="Coverage vs Race", barmode="group")

    # Coverage vs Region
    figures["region"] = go.Figure(
        data=[
            go.Bar(name=region_name, x=list(data.keys()), y=list(data.values()))
            for region_name, data in generated_data["region"].items()
        ]
    )
    figures["region"].update_layout(title="Coverage vs Region", barmode="group")

    # Coverage vs Employment Status
    figures["employment_status"] = go.Figure(
        data=[
            go.Bar(name=status_name, x=list(data.keys()), y=list(data.values()))
            for status_name, data in generated_data["employment_statuses"].items()
        ]
    )
    figures["employment_status"].update_layout(
        title="Coverage vs Employment Status", barmode="group"
    )

    # Amount vs Highest Degree Obtained
    figures["degree"] = go.Figure(
        data=[go.Bar(x=generated_data["highest_degree"]["highest_degree"], y=generated_data["highest_degree"]['insurance_cover'])]
    )
    figures["degree"].update_layout(title="Amount vs Highest Degree Obtained")

    # Amount vs Family Size
    figures["family_size"] = go.Figure(
        data=[go.Bar(x=generated_data["family_size"]['family_size'], y=generated_data["family_size"]['amount'])]
    )
    figures["family_size"].update_layout(title="Amount vs Family Size")

    # Amount vs Age
    figures["age"] = go.Figure(
        data=[go.Bar(x=generated_data['age']['age'], y=generated_data['age']['insurance_cover'])]
    )
    figures["age"].update_layout(title="Amount vs Age")

    # Total Out-of-Pocket vs Income
    figures["income"] = go.Figure(
        data=[
            go.Scatter(
                x=list(generated_data["family_income"].keys()), y=list(generated_data['family_income'].values()), mode="lines+markers"
            )
        ]
    )
    figures["income"].update_layout(title="Total Out-of-Pocket vs Income")

    # Convert all figures to JSON
    response = {
        key: json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
        for key, fig in figures.items()
    }
    return jsonify(response)


@app.route("/predict_toxicity", methods=["POST"])
def predict_toxicity():
    user_input = request.json
    df = pd.DataFrame(columns=['insurance_type', 'race', 'cancer_dx', 'hours_worked', 'employment_status', 'family_size', 'highest_degree', 'sex', 'age', 'cancer_type', 'region', 'family_income'])
    new_row = {
        'insurance_type': insurance_label_encoder.transform(user_input['inp_insurance_type']),
        'race': reverse_race_map[user_input['inp_race']],
        'cancer_dx': 1.0,
        'employment_status': reverse_employment_status[user_input['inp_employment_status']],
        'highest_degree': reverse_highest_degree_map[user_input['inp_highest_degree']],
        'sex': reverse_gender_map[user_input['inp_gender']],
        'age': scaler_model.transform(user_input['inp_age']),
        'cancer_type': cancer_label_encoder.transform(reverse_cancer_map[user_input['inp_cancer_type']]]),
        'region': reverse_region_map[user_input['inp_region']],
    }

    df = df.append(new_row, ignore_index=True)

    out_of_pocket = model.predict(df)
    toxicity_fraction = out_of_pocket / int(user_input['family_income'])  # Replace with actual prediction logic
    return jsonify({"toxicity": toxicity_fraction})


with app.app_context():
  build_reverse_maps()
  load_model()

if __name__ == "__main__":
    app.run(debug=True)
