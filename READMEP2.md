# Project 2: Data Classification Using AI
**DecodeLabs Industrial Training Kit — AI Track | Batch 2026**

## 📌 Overview
This project implements a supervised learning pipeline that classifies iris flowers into one of three species — **Setosa**, **Versicolor**, or **Virginica** — using the **K-Nearest Neighbors (KNN)** algorithm.

It follows the **Input → Process → Output (IPO)** framework taught in the training kit.

## 🎯 Objective
- Load and understand a real-world dataset
- Split data into training and testing sets
- Apply a simple classification algorithm (KNN)
- Evaluate the model using standard metrics
- Test the model on new, unseen data

## 📂 Files in this Project

| File | Description |
|------|--------------|
| `project2_classification.py` | Main Python script — full ML pipeline |
| `elbow_plot.png` | Error rate vs. K value chart (generated on run) |
| `confusion_matrix.png` | Confusion matrix heatmap (generated on run) |
| `DecodeLabs_Project2_Report.docx` | Final submission-ready report |
| `README.md` | This file |

## 🧠 Dataset
**Iris Dataset** (built into scikit-learn)
- 150 samples
- 4 features: sepal length, sepal width, petal length, petal width
- 3 balanced classes: Setosa, Versicolor, Virginica

## ⚙️ How It Works
1. **Load Data** — Iris dataset loaded via `sklearn.datasets.load_iris()`
2. **Scale Features** — `StandardScaler` normalizes all features (mean=0, variance=1)
3. **Split Data** — 80% training / 20% testing, stratified and shuffled
4. **Tune K** — Elbow method tests K=1 to 20 to find the lowest error rate
5. **Train Model** — `KNeighborsClassifier` fit on training data
6. **Evaluate** — Confusion matrix, accuracy, precision, recall, F1 score
7. **Predict New Sample** — Tests the model on one unseen flower measurement

## 🛠️ Requirements
```bash
pip install pandas scikit-learn matplotlib seaborn
```

## ▶️ How to Run
```bash
python project2_classification.py
```

Running the script will:
- Print the full pipeline output to the console
- Save `elbow_plot.png` and `confusion_matrix.png` in the same folder

## 📊 Results

| Metric | Score |
|--------|-------|
| Accuracy | 96.67% |
| Precision (macro avg) | 96.97% |
| Recall (macro avg) | 96.67% |
| F1 Score (macro avg) | 96.66% |
| Optimal K | 1 |

## 📝 Key Learnings
- Feature scaling is essential for distance-based algorithms like KNN
- The elbow method helps pick the best K value objectively, instead of guessing
- Even simple algorithms like KNN can achieve excellent results on clean, well-separated data
- Most misclassifications occurred between Versicolor and Virginica, the two species with overlapping petal measurements

## 👩‍💻 Author
Priya — DecodeLabs Artificial Intelligence Track, Batch 2026

## 📞 Program Contact
- 🌐 www.decodelabs.tech
- ✉ decodelabs.tech@gmail.com
- 📍 Greater Lucknow, India
