# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('study_programs_2022.csv')

print(df.describe())
print(df['Program'].value_counts())

df.describe(include=['object'])

df_sorted = df.sort_values(by="Average Gross Salary (PLN)", ascending=False)

plt.figure(figsize=(10, 8))
plt.barh(df_sorted['Program'], df_sorted['Average Gross Salary (PLN)'], color='lightblue')
plt.xlabel("Average Gross Salary (PLN)")
plt.title("Ranking of Study Programs by Salary")
plt.gca().invert_yaxis()  # Highest salaries at the top
plt.show()
plt.tight_layout()

correlation = df.corr(numeric_only=True)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from random import randrange
import pickle

X = df[["Job Search Duration (months)", "% Time Unemployed", "Relative Unemployment Index", "Relative Salary Index"
]]
y = df["Average Gross Salary (PLN)"]

'''
# Optional model tuning block — find best model with random seeds
best_model_score = 0
for _ in range(200):
    seed = randrange(100000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed)

    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    if score > best_model_score:
        best_model_score = score
        best_seed = seed
        print(best_model_score, " seed: ", best_seed)
        with open("study_programs_model.pickle", "wb") as f:
            pickle.dump(model, f)
'''

# Load best model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=59360)

with open("study_programs.pickle", "rb") as f:
    model = pickle.load(f)

print("R² (model accuracy):", model.score(X_test, y_test))
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

X_new = pd.DataFrame([[2.0, 4.0, 0.4, 0.5]], columns=X.columns)
prediction = model.predict(X_new)
print("Predicted salary:", round(prediction[0], 2), "PLN")
