import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.inspection import permutation_importance

import matplotlib.pyplot as plt

# **Carga de dataset titanic**


# Cargar el dataset Titanic
train_df = pd.read_csv('/content/train.csv')

#10 variables
#25 columnas

# **Normalizacion de datos**

# Preprocesamiento de datos
#Elimina las columnas 'PassengerId', 'Name', 'Ticket', del conjunto de datos, ya que son irrelevantes para la predicción de la supervivencia.

titanic_data = train_df.drop(['PassengerId', 'Name', 'Ticket'], axis=1)


#Rellena los valores faltantes en la columna 'Age' con la media de las edades.

titanic_data['Age'].fillna(titanic_data['Age'].mean(), inplace=True)

#Rellena los valores faltantes en la columna 'Embarked' con el valor más común (moda) de los puertos de embarque.
titanic_data['Embarked'].fillna(titanic_data['Embarked'].mode()[0], inplace=True)

#rellena los valores faltante de la columna cabin con la letra 'U' de unknown
titanic_data['Cabin'].fillna('U', inplace=True)


#Codifica las variables categóricas 'Sex' y 'Embarked' en variables numéricas utilizando el método de variables dummy
titanic_data = pd.get_dummies(titanic_data, columns=['Sex', 'Embarked'], drop_first=True)

# Convertir la columna 'Cabin' en una variable numérica
titanic_data['Cabin'] = titanic_data['Cabin'].astype('category').cat.codes

# **Division de data para entrenamiento**

# Dividir datos en conjunto de entrenamiento y prueba
X = titanic_data.drop('Survived', axis=1)
y = titanic_data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verificar si hay valores NaN
if X_train.isnull().values.any() or y_train.isnull().values.any():
    print("X_train o y_train contienen valores NaN. Debes manejarlos antes de continuar.")

# Verificar si X_train y y_train tienen la misma longitud
if len(X_train) != len(y_train):
    print("X_train y y_train tienen longitudes diferentes. Asegúrate de que sean iguales.")

# Verificar si X_train es 2D y y_train es 1D
if len(X_train.shape) != 2 or len(y_train.shape) != 1:
    print("Las dimensiones de X_train o y_train no son correctas. X_train debe ser 2D y y_train debe ser 1D.")

# **Entrenamiento para ramdomforest y calcula importancia de las caracteristicas**

#Entrena un modelo RandomForestClassifier y un modelo GradientBoostingClassifier
# Entrenar un modelo de Random Forest para clasificación y obtener la importancia de características
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)
feature_importances_rf = rf_clf.feature_importances_
#print("Feature Importances (Random Forest):", feature_importances_rf)

feature_scores = np.mean([tree.feature_importances_ for tree in rf_clf.estimators_], axis=0)
feature_scores_df = pd.DataFrame({'Feature': X_train.columns, 'Score (Random Forest)': feature_scores})
print("\nFeature Scores (Random Forest):")
print(feature_scores_df)

feature_scores_df.plot(x='Feature', y='Score (Random Forest)', kind='bar', title='Feature Scores (Random Forest)')
plt.show()


# **Entrenamiento para Gradient Boosting  y calcula importancia de caracteristicas**

# Entrenar un modelo de Gradient Boosting para clasificación y obtener la importancia de características
gb_clf = GradientBoostingClassifier(random_state=42)
gb_clf.fit(X_train, y_train)
feature_importances_gb = gb_clf.feature_importances_

feature_scores_gb = gb_clf.feature_importances_
feature_scores_df_gb = pd.DataFrame({'Feature': X_train.columns, 'Score (Gradient Boosting)': feature_scores_gb})
print("\nFeature Scores (Gradient Boosting):")
print(feature_scores_df_gb)

feature_scores_df_gb.plot(x='Feature', y='Score (Gradient Boosting)', kind='bar', title='Feature Scores (Gradient Boosting)')
plt.show()


# **Calcula permutacion para gradienboosting**

#calcula permutation score para grandient boosting y random forest y los muestra en un dataframe
result_gb = permutation_importance(gb_clf, X_test, y_test, n_repeats=10, random_state=42)
perm_importance_gb = result_gb.importances_mean
#print("\nPermutation Feature Importance (Gradient Boosting):", perm_importance_gb)
feature_scores_gb = gb_clf.feature_importances_
feature_scores_df_gb = pd.DataFrame({'Feature': X_train.columns, 'Permutation Importance (Gradient Boosting)': perm_importance_gb})
print("\nFeature Scores (Gradient Boosting):")
print(feature_scores_df_gb)


# **Calcula permutacion para ramdom forest**

# Calcular Permutation Feature Importance Score para el modelo de Random Forest
result = permutation_importance(rf_clf, X_test, y_test, n_repeats=10, random_state=42)
perm_importance = result.importances_mean
#print("Permutation Feature Importance (Random Forest):", perm_importance)
feature_scores = np.mean([tree.feature_importances_ for tree in rf_clf.estimators_], axis=0)
feature_scores_df = pd.DataFrame({'Feature': X_train.columns,'Permutation Importance (Random Forest)': perm_importance})
print("\nFeature Scores (Random Forest):")
print(feature_scores_df)

# **Calcula score para cada caracteristica**

#cacular score para cada feature
# Calcular el score de cada característica y mostrarlo nombre de cada caracteriatica
feature_scores = np.mean([tree.feature_importances_ for tree in rf_clf.estimators_], axis=0)
feature_scores_gb = gb_clf.feature_importances_
feature_scores_df = pd.DataFrame({'Feature': X_train.columns, 'Score (Random Forest)': feature_scores, 'Score (Gradient Boosting)': feature_scores_gb})
print("\nFeature Scores:")
print(feature_scores_df)



# **Calcula sobreviviente y muertos**

#calcular sobrevivientes y muertos
import matplotlib.pyplot as plt

survived = titanic_data[titanic_data['Survived'] == 1]
dead = titanic_data[titanic_data['Survived'] == 0]
# mostrar graficamente los sobrevivientes y muertos
print("Sobrevivientes: ", len(survived))
print("Muertos: ", len(dead))
total= len(dead) + len(survived)
print("Total de personas:", total)
# grafico de barras para sobrevivientes y muertos
titanic_data['Survived'].value_counts().plot(kind='bar', title='Sobrevivientes vs. Muertos')
plt.xlabel('Survived')
plt.ylabel('Count')
plt.xticks([0, 1], ['Muertos', 'Sobrevivientes'])

plt.show()

most_important_feature = feature_scores_df['Feature'][feature_scores_df['Score (Random Forest)'].idxmax()]
print("\nEl dato más importante es:", most_important_feature)
print("Explicación: El dato más importante es el que tiene el mayor score en el modelo de Random Forest. Esto significa que es la característica que más influye en la predicción de la supervivencia de los pasajeros del Titanic.")

# Calculate the feature importance scores for the given input x
input_data = pd.DataFrame([x], columns=X_train.columns)
feature_importances = gb_clf.feature_importances_
input_feature_scores = pd.DataFrame({'Feature': X_train.columns, 'Importance': feature_importances})
input_feature_scores = input_feature_scores.sort_values(by='Importance', ascending=False)

# Get the top features with the highest importance scores
top_features = input_feature_scores['Feature'].head(3).tolist()  # Change the number 3 to the desired number of top features

# Print the top features and their explanations
print("The output 'y' of the model is most influenced by the following features:")
for feature in top_features:
    print("- " + feature)

print("\nExplanation:")
print("The listed features have the highest importance scores, indicating that they have the greatest influence on predicting the output 'y' for the given input x.")
