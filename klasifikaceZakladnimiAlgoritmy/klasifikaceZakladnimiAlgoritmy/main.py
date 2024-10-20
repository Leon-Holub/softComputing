# Zjištování zda zítra bude pršet
# zdroj dat weatherAUS.csv


# TOTO JE KNN
# příklad
# Den A má teplotu Ta a Hustotu srážek Ha - teplota [-5; 45], srážky [0; 100]
# Den B má teplotu Tb a Hustotu srážek Hb
# delta AB = Odmocnina((Ta - Tb)^2 + (Ha - Hb)^2) + ...)


# Den A má vítr W - [0-330]
# Den B má vítr WNW
# West je 270 stupňů a WestNorthWest je 300 stupňů
# Směr větru by měl nejvetší váhu, tím že je max 330 stupňů
# Proto si vše převedu na stejnou váhu -> [0;1]

# Udělat aby se filtrovalo podle města
# Data podle měst si rozdělit na 2 datasety - trénovací a testovací
# 3:1 - 75% trénovací, 25% testovací
# CrossValiace - 10x
# Rozdělím na 10 částí, 9 částí budu trénovat a 1 část testovat
# Fold 0 bude mít věe kromě 0. části dat
# Fold 1 bude mít vše kromě 1. části dat
# Po všech foldech spočítám průměr a STD


## Gaussian naive Bayes classifier 
# 2300 nepršelo, 700 pršelo

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler


def classify_weather_for_city(city_name=None, save_graphs=False):
    # Načtení datasetu
    data = pd.read_csv('weatherAUS.csv')

    # Filtrování dat pouze pro konkrétní město
    if city_name:
        data = data[data['Location'] == city_name]

    # Příprava datasetu
    # Výběr sloupců, které použijeme pro klasifikaci (např. 'MinTemp', 'MaxTemp', 'Rainfall', ...)
    columns_to_use = ['MinTemp', 'MaxTemp', 'Rainfall', 'Humidity3pm', 'Humidity9am', 'Pressure9am', 'Pressure3pm',
                      'RainToday']
    data = data[columns_to_use + ['RainTomorrow']]

    # Převod hodnot 'RainToday' na binární ('Yes' -> 1, 'No' -> 0)
    data['RainToday'] = data['RainToday'].map({'Yes': 1, 'No': 0})

    # Nahrazení chybějících hodnot ve sloupcích 'MinTemp' a 'MaxTemp' mediánem
    data['MinTemp'] = data['MinTemp'].fillna(data['MinTemp'].median())
    data['MaxTemp'] = data['MaxTemp'].fillna(data['MaxTemp'].median())
    data = data.dropna()

    # Převod klasifikované třídy na binární hodnoty ('Yes' -> 1, 'No' -> 0)
    data['RainTomorrow'] = data['RainTomorrow'].map({'Yes': 1, 'No': 0})

    # Rozdělení na vstupy a výstupy
    X = data[columns_to_use]
    y = data['RainTomorrow']

    # Normalizace vstupních dat na rozsah 0 - 1
    scaler = MinMaxScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=columns_to_use)

    # Vytvoření 10-fold cross-validation
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    # Gaussian Naive Bayes Classifier
    gnb = GaussianNB()
    gnb_accuracies = cross_val_score(gnb, X, y, cv=skf, scoring='accuracy')
    print(
        f'Gaussian Naive Bayes Classifier - průměrná přesnost pro {city_name if city_name else "všechna města"}: {gnb_accuracies.mean():.2f}')

    # k-Nearest Neighbours Classifier
    knn = KNeighborsClassifier(n_neighbors=5)
    knn_accuracies = cross_val_score(knn, X, y, cv=skf, scoring='accuracy')
    print(
        f'k-Nearest Neighbours Classifier - průměrná přesnost pro {city_name if city_name else "všechna města"}: {knn_accuracies.mean():.2f}')

    # Confusion Matrix pro každý klasifikátor
    iteration = 0
    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Gaussian Naive Bayes
        gnb.fit(X_train, y_train)
        y_pred_gnb = gnb.predict(X_test)
        cm_gnb = confusion_matrix(y_test, y_pred_gnb)
        print(f'Confusion Matrix - Gaussian Naive Bayes pro {city_name if city_name else "všechna města"}:{cm_gnb}\n')

        # k-Nearest Neighbours
        knn.fit(X_train, y_train)
        y_pred_knn = knn.predict(X_test)
        cm_knn = confusion_matrix(y_test, y_pred_knn)
        print(f'Confusion Matrix - k-Nearest Neighbours pro {city_name if city_name else "všechna města"}:{cm_knn}\n')

        # Vykreslení confusion matrix pro lepší přehled
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        sns.heatmap(cm_gnb, annot=True, fmt='d', cmap='Blues', xticklabels=['No (Predicted)', 'Yes (Predicted)'], yticklabels=['No (True)', 'Yes (True)'])
        plt.title(f'Confusion Matrix - Gaussian Naive Bayes - {city_name if city_name else "všechna města"}')
        plt.subplot(1, 2, 2)
        sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Greens', xticklabels=['No (Predicted)', 'Yes (Predicted)'], yticklabels=['No (True)', 'Yes (True)'])
        plt.title(f'Confusion Matrix - k-Nearest Neighbours - {city_name if city_name else "všechna města"}')
        if save_graphs:
            directory = f'graphs/{city_name if city_name else "all_cities"}'
            if not os.path.exists(directory):
                os.makedirs(directory)
            plt.savefig(
                f'{directory}/confusion_matrix_{city_name if city_name else "all_cities"}_iteration_{iteration}.png')
        else:
            plt.show()
        iteration += 1

classify_weather_for_city('Albury', save_graphs=True)
classify_weather_for_city(save_graphs=True)
