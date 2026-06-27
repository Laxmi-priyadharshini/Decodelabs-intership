"""
DecodeLabs - Project 2: Data Classification Using AI
Goal: Build a basic classification model using a small dataset (Iris).
Pipeline: Input -> Process -> Output (IPO Framework)
Algorithm: K-Nearest Neighbors (KNN)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    precision_score, recall_score, f1_score
)

# -------------------------------------------------------------------
# STEP 1: INPUT -> Load and understand the dataset
# -------------------------------------------------------------------
iris = load_iris()
X = iris.data                      # Features: sepal length/width, petal length/width
y = iris.target                    # Labels: 0=Setosa, 1=Versicolor, 2=Virginica
feature_names = iris.feature_names
target_names = iris.target_names

df = pd.DataFrame(X, columns=feature_names)
df['species'] = pd.Categorical.from_codes(y, target_names)

print("=" * 60)
print("STEP 1: DATASET OVERVIEW")
print("=" * 60)
print(f"Samples: {df.shape[0]}, Features: {X.shape[1]}, Classes: {len(target_names)}")
print(f"Classes: {list(target_names)}")
print("\nFirst 5 rows:\n", df.head())
print("\nClass distribution:\n", df['species'].value_counts())
print("\nStatistical summary:\n", df.describe())

# -------------------------------------------------------------------
# STEP 2: PROCESS -> Feature Scaling (The Gatekeeper Rule)
# -------------------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("\n" + "=" * 60)
print("STEP 2: FEATURE SCALING APPLIED (mean=0, variance=1)")
print("=" * 60)

# -------------------------------------------------------------------
# STEP 3: PROCESS -> Train-Test Split (Structural Integrity)
# -------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,        # 80% train / 20% test
    random_state=42,      # reproducibility
    shuffle=True,
    stratify=y             # keeps class balance equal in both sets
)
print("\n" + "=" * 60)
print("STEP 3: TRAIN-TEST SPLIT")
print("=" * 60)
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples : {X_test.shape[0]}")

# -------------------------------------------------------------------
# STEP 4: TUNING -> Find the optimal K (Elbow Method)
# -------------------------------------------------------------------
error_rates = []
k_range = range(1, 21)
for k in k_range:
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    knn_temp.fit(X_train, y_train)
    pred_temp = knn_temp.predict(X_test)
    error_rates.append(np.mean(pred_temp != y_test))

best_k = k_range[np.argmin(error_rates)]
print("\n" + "=" * 60)
print("STEP 4: OPTIMAL K SELECTION")
print("=" * 60)
print(f"Best K found: {best_k} (lowest error rate: {min(error_rates):.4f})")

plt.figure(figsize=(8, 5))
plt.plot(k_range, error_rates, marker='o', linestyle='--', color='steelblue')
plt.axvline(best_k, color='orange', linestyle=':', label=f'Optimal K = {best_k}')
plt.title("Tuning the Engine: Error Rate vs K Value")
plt.xlabel("K Value")
plt.ylabel("Error Rate")
plt.legend()
plt.tight_layout()
plt.savefig("elbow_plot.png", dpi=150)
plt.close()

# -------------------------------------------------------------------
# STEP 5: PROCESS -> Train the final KNN model (scikit-learn workflow)
# -------------------------------------------------------------------
model = KNeighborsClassifier(n_neighbors=best_k)   # INSTANTIATE
model.fit(X_train, y_train)                        # FIT
predictions = model.predict(X_test)                 # PREDICT

# -------------------------------------------------------------------
# STEP 6: OUTPUT -> Validation (Confusion Matrix, F1, etc.)
# -------------------------------------------------------------------
acc = accuracy_score(y_test, predictions)
prec = precision_score(y_test, predictions, average='macro')
rec = recall_score(y_test, predictions, average='macro')
f1 = f1_score(y_test, predictions, average='macro')
cm = confusion_matrix(y_test, predictions)

print("\n" + "=" * 60)
print("STEP 5 & 6: MODEL TRAINING + OUTPUT VALIDATION")
print("=" * 60)
print(f"Model used      : KNeighborsClassifier(n_neighbors={best_k})")
print(f"Accuracy        : {acc:.4f}")
print(f"Precision (avg) : {prec:.4f}")
print(f"Recall (avg)    : {rec:.4f}")
print(f"F1 Score (avg)  : {f1:.4f}")
print("\nConfusion Matrix:\n", cm)
print("\nFull Classification Report:\n",
      classification_report(y_test, predictions, target_names=target_names))

# Confusion matrix heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=target_names, yticklabels=target_names)
plt.title("Confusion Matrix - KNN Iris Classifier")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
plt.close()

# -------------------------------------------------------------------
# STEP 7: Test the model on a brand-new, unseen sample
# -------------------------------------------------------------------
sample = np.array([[5.1, 3.5, 1.4, 0.2]])   # typical Setosa measurements
sample_scaled = scaler.transform(sample)
sample_pred = model.predict(sample_scaled)
print("\n" + "=" * 60)
print("STEP 7: PREDICTION ON NEW UNSEEN DATA")
print("=" * 60)
print(f"Input features : {sample.tolist()[0]}")
print(f"Predicted class: {target_names[sample_pred[0]]}")

print("\n✅ Project 2 pipeline completed successfully.")
print("Saved: elbow_plot.png, confusion_matrix.png")
