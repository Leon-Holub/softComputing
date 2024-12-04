from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score


def load_and_preprocess_data():
    mnist = fetch_openml('mnist_784', version=1)
    X = mnist.data
    y = mnist.target.astype(int)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


def split_data(X, y, test_size=0.3, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def perform_pca(X, n_components=2):
    pca = PCA(n_components=n_components)
    return pca.fit_transform(X)


def perform_tsne(X, y, n_components=2, random_state=42):
    X_subset = X
    y_subset = y
    tsne = TSNE(n_components=n_components, random_state=random_state)
    return tsne.fit_transform(X_subset), y_subset


def visualize_data(X, y, title, filename):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=y, palette='tab10', legend='full')
    plt.title(title)
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    plt.savefig(filename)
    plt.savefig(filename)
    plt.show()


def evaluate_knn(X_train, X_test, y_train, y_test, k_values=range(1, 21)):
    accuracies = []
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        accuracies.append(accuracy_score(y_test, y_pred))
    return accuracies


def plot_accuracies(k_values, accuracies_original, accuracies_pca, accuracies_tsne, filename):
    plt.figure(figsize=(12, 6))
    plt.plot(k_values, accuracies_original, label='Original Data', marker='o')
    plt.plot(k_values, accuracies_pca, label='PCA Reduced Data', marker='o')
    plt.plot(k_values, accuracies_tsne, label='t-SNE Reduced Data', marker='o')
    plt.xlabel('Number of Neighbors (k)')
    plt.ylabel('Accuracy')
    plt.title('kNN Accuracy for Different Values of k')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()


def main():
    X_scaled, y = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = split_data(X_scaled, y)

    X_pca = perform_pca(X_scaled)
    X_tsne, y_subset = perform_tsne(X_scaled, y)

    visualize_data(X_pca, y, title='PCA of MNIST', filename='pca_mnist.png')
    visualize_data(X_tsne, y_subset, title='t-SNE of MNIST', filename='tsne_mnist.png')

    k_values = range(1, 21)
    accuracies_original = evaluate_knn(X_train, X_test, y_train, y_test, k_values)

    X_train_pca, X_test_pca, y_train_pca, y_test_pca = split_data(X_pca, y)
    accuracies_pca = evaluate_knn(X_train_pca, X_test_pca, y_train_pca, y_test_pca, k_values)

    X_train_tsne, X_test_tsne, y_train_tsne, y_test_tsne = split_data(X_tsne, y_subset)
    accuracies_tsne = evaluate_knn(X_train_tsne, X_test_tsne, y_train_tsne, y_test_tsne, k_values)

    plot_accuracies(k_values, accuracies_original, accuracies_pca, accuracies_tsne, filename='knn_accuracies.png')


if __name__ == "__main__":
    main()
