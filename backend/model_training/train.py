import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn, torch.optim as optim
from preprocess import load_and_preprocess
from model import ExamPredictor
import joblib

# Load data
X, y, enc, scaler = load_and_preprocess("./data/StudentsPerformance.csv")
dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Instantiate model
model = ExamPredictor(input_dim=X.shape[1])
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Training loop
for epoch in range(1, 1000):
    model.train()
    for xb, yb in loader:
        preds = model(xb)
        loss = criterion(preds, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch}/1000 — Loss: {loss.item():.4f}")

# Save weights
torch.save(model.state_dict(), "exam_predictor_weights.pth")
joblib.dump(enc, "encoder.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model training complete and weights saved.")
