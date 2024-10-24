import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load the Wine Quality dataset
df = pd.read_csv('winequality-red.csv', sep=';')

# Display the first few rows of the dataset
print("Data Preview:\n", df.head())

# Define features and labels
X = df.drop('quality', axis=1)  # Features
y = df['quality']  # Labels

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)
print("Predictions:", predictions)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# Confusion matrix
conf_matrix = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:\n", conf_matrix)

# Classification report
class_report = classification_report(y_test, predictions)
print("\nClassification Report:\n", class_report)
