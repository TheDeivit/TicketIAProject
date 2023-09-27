import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt  # Importa Matplotlib
import pickle

# Carga el conjunto de datos desde el archivo CSV
data = pd.read_csv('ticket/dataset.csv')

# Realiza la codificación one-hot de las columnas categóricas
data_encoded = pd.get_dummies(data, columns=['urgency_id', 'location_id', 'category_id'])

# Divide el conjunto de datos en características (X) y la variable objetivo (y)
X = data_encoded.drop('technician_id', axis=1)  # Características
y = data_encoded['technician_id']  # Variable objetivo

# Divide los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Crea un modelo de árbol de decisión con hiperparámetros ajustados y criterio "entropy"
clf = DecisionTreeClassifier(max_depth=24, min_samples_split=2, min_samples_leaf=1, criterion='entropy')

# Entrena el modelo utilizando el conjunto de entrenamiento
clf.fit(X_train, y_train)

# Visualiza el árbol de decisión después de entrenar el modelo
#plt.figure(figsize=(12, 8))
#plot_tree(clf, filled=True, feature_names=X.columns.tolist(), class_names=[str(c) for c in clf.classes_], rounded=True)
#plt.show()  # Muestra el árbol

# Predicción para el nuevo ticket
new_ticket = {
                'urgency_id': '64eea4934fc31abc4d0a68ab',
                'location_id': '64eea4a64fc31abc4d0a68af',
                'category_id': '64fe83cc4eee2435616d6706',
            }

# Crear un DataFrame para el nuevo ticket
new_ticket_df = pd.DataFrame([new_ticket])

# Crear un DataFrame para el nuevo ticket con todas las columnas de características
new_ticket_encoded = pd.get_dummies(new_ticket_df, columns=['urgency_id', 'location_id', 'category_id'])
new_ticket_encoded = new_ticket_encoded.reindex(columns=X.columns, fill_value=0)

# Obtener las probabilidades de pertenencia a cada clase
predicted_probabilities = clf.predict_proba(new_ticket_encoded)

# Obtener las 3 clases con las probabilidades más altas
#top_3_classes = clf.classes_[predicted_probabilities.argsort(axis=1)[:, -4:][:, ::-1]]

#print("Tres técnicos más probables:", top_3_classes)


technician_id = clf.classes_[predicted_probabilities.argmax()]

print("Mejor técnico:", technician_id)

# Guardar el modelo en un archivo (puedes elegir un nombre y ubicación adecuados)
with open('modelo_arbol.pkl', 'wb') as model_file:
    pickle.dump(clf, model_file)