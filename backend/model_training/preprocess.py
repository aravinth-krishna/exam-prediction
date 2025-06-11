import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_and_preprocess(csv_path: str):
    df = pd.read_csv(csv_path)
    # Numeric features
    X_num = df[['reading score','writing score']].values
    # Categorical features
    X_cat = df[['gender','race/ethnicity','parental level of education',
                'lunch','test preparation course']].values
    # One‑hot encode
    enc = OneHotEncoder(sparse_output=False)
    X_cat_enc = enc.fit_transform(X_cat)
    # Standardize
    scaler = StandardScaler()
    X_num_scl = scaler.fit_transform(X_num)
    # Combine features
    X = torch.tensor(np.hstack([X_num_scl, X_cat_enc]), dtype=torch.float32)
    # Target: math score
    y = torch.tensor(df['math score'].values, dtype=torch.float32).unsqueeze(1)
    return X, y, enc, scaler

if __name__ == "__main__":
    X, y, enc, scaler = load_and_preprocess("../data/StudentsPerformance.csv")
    print(f"Shape X: {X.shape}, y: {y.shape}")
