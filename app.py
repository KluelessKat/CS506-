from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import numpy as np
import json
from generate_plotting_data import generate_plotting_data, cancer_name_map, highest_degrees


app = Flask(__name__)

# Dummy data
features = {
    "cancer_types": list(cancer_name_map.keys()),
    "insurance_types": ["Medicare", "Medicaid", "Private"],
    "regions": ["Northeast", "South", "Midwest", "West"],
    "employment_statuses": ["Employed", "Unemployed"],
    "highest_degrees": highest_degrees, # index + 1 is the code
    "family_sizes": list(range(1, 8)),
    "genders": ["male", "female"],
    "income_levels": ["<30k", "30k-60k", "60k-100k", "100k+"],
    "races": ["white", "black", "asian", "other"],
}


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
    print(user_input)
    toxicity_fraction = np.random.uniform(0, 1)  # Replace with actual prediction logic
    return jsonify({"toxicity": toxicity_fraction})


if __name__ == "__main__":
    app.run(debug=True)
