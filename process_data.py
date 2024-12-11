import numpy as np
import pandas as pd

#
#     'REGION22': 'Region', ['-1 INAPPLICABLE', '1 NORTHEAST', '2 MIDWEST', '3 SOUTH', '4 WEST']
#     'FAMS1231': 'Family Size', ['-1 INAPPLICABLE',        '1 PERSON',       '2 PERSONS', '3 PERSONS',4,5,6,7,8, 9,10, 11, 14]
#     'RXEXP22': 'Prescription Cost Spent', (int32)
#     'CANCERDX': 'Cancer Diagnosis',
#     'UNINS22': 'Uninsured',
#     'PRVEV22': 'Private Insurance', (categorical)['0 NO', '1 YES']
#     'MCDEV22': 'Medicaid Status',(categorical)
#     'MCREV22': 'Medicare Status',(categorical)
#     'PRVEV22': 'Private Health Care status',(categorical)
#     'VAEV22': 'Veteran's Administration Status',(categorical)
#     'TRIEV22': 'Tricare status',(categorical)
#     'WCPEV22': Worker's Comp status,(categorical)
#     'OSREV22': Other Sources Comp status,(categorical)
#     'HOUR53': 'Hours Worked', (categorical, -ve numbers are not recorded, higher numbers max number of hours)
#     'EMPST53': 'Employment Status',
#     'FAMINC22': 'Family Income', (int32)
#     'HIDEG': 'Highest Degree', ['-8 DON'T KNOW', '-7 REFUSED', '1 NO DEGREE', '2 GED', '3 HIGH SCHOOL DIPLOMA', '4 BACHELOR'S DEGREE', '5 MASTER'S DEGREE', '6 DOCTORATE DEGREE', '7 OTHER DEGREE', '8 UNDER AGE 16 - INAPPLICABLE']
#     'MARRY22X': 'Marital Status', ['-8 DON'T KNOW' < '-7 REFUSED' < '1 MARRIED' < '2 WIDOWED' < '3 DIVORCED' < '4 SEPARATED' < '5 NEVER MARRIED' < '6 UNDER AGE 16 - INAPPLICABLE']
#     'RACEV1X': 'Race', ['1 WHITE - NO OTHER RACE REPORTED', '2 BLACK - NO OTHER RACE REPORTED','3 AMER INDIAN/ALASKA NATIVE - NO OTHER RACE','4 ASIAN/NATV HAWAIIAN/PACFC ISL-NO OTH', '6 MULTIPLE RACES REPORTED']
#     'SEX': 'Sex', ['1 MALE', '2 FEMALE']
#     'AGELAST': 'Age',
#     'TOTSLF22': 'Out of Pocket Cost',
#     'CABLADDR': 'Bladder Cancer',
#     'CABREAST': 'Breast Cancer',
#     'CACERVIX': 'Cervix Cancer',
#     'CACOLON': 'Colon Cancer',
#     'CALUNG': 'Lung Cancer',
#     'CALYMPH': 'Lymphoma Cancer',
#     'CAMELANO': 'Melanoma Cancer',
#     'CAOTHER': 'Other Cancer',
#     'CAPROSTA': 'Prostate Cancer',
#     'CASKINNM': 'Skin Nonmelanoma Cancer',
#     'CASKINDK': 'Skin Unknown Cancer',
#     'CAUTERUS': 'Uterus Cancer',
#     'TOTMCD22': 'Total paid by Medicaid', (int)
#     'TOTMCR22': 'Total paid by Medicare', (int)
#     'TOTPRV22': 'Total paid by private insurance', (int)
#     'TOTVA22' : 'Total paid by Veteran's Administration', (int)
#     'TOTTRI22' : 'Total paid by Tricare', (int)
#     'TOTOFD22': 'Total paid by other federal sources', (int)
#     'TOTSTL22' : 'Total paid by State and Local', (int)
#     'TOTTRI22' : 'Total paid by Tricare', (int)
#     'TOTWCP22': 'Total paid by worker's comp' (int)
#     'TOTOSR22': 'Total paid by other sources' (int)
#     'DUPERSID': Patient ID

DATA_FILES = {"22": "h243.dta", "21": "h233.dta", "20": "h224.dta"}


def process_data(data_root="./"):
    data = pd.DataFrame()

    UID = "DUPERSID"
    cancer_type_variables = [
        "CABLADDR",
        "CABREAST",
        "CACERVIX",
        "CACOLON",
        "CALUNG",
        "CALYMPH",
        "CAMELANO",
        "CAOTHER",
        "CAPROSTA",
        "CASKINNM",
        "CASKINDK",
        "CAUTERUS",
    ]
    constant_keys = {
        "RACEV1X": "race",
        "CANCERDX": "cancer_dx",
        "HOUR53": "hours_worked",
        "EMPST53": "employment_status",
        "HIDEG": "highest_degree",
        "SEX": "sex",
        "AGELAST": "age",
    }

    year_dep_ins_type = {
        "UNINS": "uninsured",
        "PRVEV": "private",
        "MCDEV": "medicaid",
        "MCREV": "medicare",
        "GVAEV": "other_public",
        "TRIEV": "tricare",
        "GVBEV": "hmo_public",
        "GVCEV": "other_paid",
    }
    year_dependent_keys = {
        "REGION": "region",
        "RXEXP": "prescription_exp",
        "FAMINC": "family_income",
        "TOTSLF": "out_of_pocket",
        "TOTMCD": "insurance_cover",
        "TOTMCR": "insurance_cover",
        "TOTPRV": "insurance_cover",
        "TOTVA": "insurance_cover",
        "TOTTRI": "insurance_cover",
        "TOTOFD": "insurance_cover",
        "TOTSTL": "insurance_cover",
        "TOTWCP": "insurance_cover",
        "TOTOSR": "insurance_cover",
    }

    for year, file in DATA_FILES.items():
        df = pd.read_stata(data_root + file)

        # Ensure UID is properly added
        if "UID" not in data.columns:
            data["UID"] = df[UID]

        # Add insurance type
        if "insurance_type" not in data.columns:
            data["insurance_type"] = None

        for instype, value in year_dep_ins_type.items():
            column_name = instype + year
            if pd.api.types.is_categorical_dtype(df[column_name]):
                mask = df[column_name].str.split().str[0].astype(float) == 1

            data.loc[mask, "insurance_type"] = value

        # Process constant keys
        for df_key, data_key in constant_keys.items():
            if data_key not in data.columns:
                data[data_key] = None
            if pd.api.types.is_categorical_dtype(df[df_key]):
                data[data_key] = df[df_key].str.split().str[0].astype(float)
            else:
                data[data_key] = df[df_key]
        for df_key in cancer_type_variables:
            if "cancer_type" not in data.columns:
                data["cancer_type"] = None
            mask = df[df_key].str.split().str[0].astype(float) == 1
            data.loc[mask, "cancer_type"] = df_key

        # Process year-dependent keys
        for df_key, data_key in year_dependent_keys.items():
            if data_key not in data.columns:
                data[data_key] = None

            df_key_with_year = df_key + year
            if pd.api.types.is_categorical_dtype(df[df_key_with_year]):
                data[data_key] = df[df_key_with_year].str.split().str[0].astype(int)
            elif data_key == "insurance_cover":
                mask = df[df_key_with_year] > 0
                data.loc[mask, data_key] = df.loc[mask, df_key_with_year]
            else:
                data[data_key] = df[df_key_with_year]

    data = data[data["cancer_dx"] == 1]
    data.drop_duplicates(subset=["UID"], inplace=True)
    data.to_csv("results.csv", index=False)
    return data


if __name__ == "__main__":
    process_data("./data/")
