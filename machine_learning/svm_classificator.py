#%%
from matplotlib import markers
import numpy as np
from numpy import loadtxt
import random
import matplotlib.pyplot as plt
import matplotlib
from sklearn.svm import SVC
from sklearn import svm, datasets

matplotlib.use("Agg")
get_ipython().run_line_magic("matplotlib", "qt")
#%%
def polynomial_parameters(
    x_train,
    y_train,
    x_val,
    y_val,
    degree_array=(np.arange(6) + 2),
    c_array=np.array([0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 50]),
):
    error_min = 1
    for i in range(c_array.size):
        for j in range(degree_array.size):
            clf = svm.SVC(kernel="poly", degree=degree_array[j], C=c_array[i]).fit(
                x_train, y_train
            )
            predictions = clf.predict(x_val)
            error = np.mean((predictions != y_val).astype(int))
            print(
                "C = %.2lf, degree = %.2lf, error = %.6lf"
                % (c_array[i], degree_array[j], error)
            )
            if error < error_min:
                c = c_array[i]
                degree = degree_array[j]
                error_min = error
    print("Final parameters: C = %.2lf, degree = %.2lf" % (c, degree))
    clf = svm.SVC(kernel="poly", degree=degree, C=c).fit(x_train, y_train)
    return clf


def sigmoid_parameters(
    x_train,
    y_train,
    x_val,
    y_val,
    degree_array=(np.arange(6) + 2),
    c_array=np.array([0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 50]),
):
    error_min = 1
    for i in range(c_array.size):
        for j in range(degree_array.size):
            clf = svm.SVC(kernel="sigmoid", degree=degree_array[j], C=c_array[i]).fit(
                x_train, y_train
            )
            predictions = clf.predict(x_val)
            error = np.mean((predictions != y_val).astype(int))
            print(
                "C = %.2lf, degree = %.2lf, error = %.6lf"
                % (c_array[i], degree_array[j], error)
            )
            if error < error_min:
                c = c_array[i]
                degree = degree_array[j]
                error_min = error
    print("Final parameters: C = %.2lf, degree = %.2lf" % (c, degree))
    clf = svm.SVC(kernel="sigmoid", degree=degree, C=c).fit(x_train, y_train)
    return clf


def rbf_parameters(
    x_train,
    y_train,
    x_val,
    y_val,
    c_array=np.array([0.01, 0.03, 0.1, 0.3, 0.7, 1, 3, 10, 30, 50]),
    gamma_array=np.array([0.01, 0.03, 0.1, 0.3, 0.7, 1, 3, 10, 30, 50]),
):
    error_min = 1
    for i in range(c_array.size):
        for j in range(gamma_array.size):
            clf = svm.SVC(kernel="rbf", gamma=gamma_array[j], C=c_array[i]).fit(
                x_train, y_train
            )
            predictions = clf.predict(x_val)
            error = np.mean((predictions != y_val).astype(int))
            print(
                "C = %.2lf, gamma = %.2lf, error = %.6lf"
                % (c_array[i], gamma_array[j], error)
            )
            if error < error_min:
                c = c_array[i]
                gamma = gamma_array[j]
                error_min = error
    print("Final parameters: C = %.2lf, gamma = %.2lf" % (c, gamma))
    clf = svm.SVC(kernel="rbf", gamma=gamma, C=c).fit(x_train, y_train)
    return clf


def model_accuracy(clf, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full):
    prediction_train = clf.predict(x_train)
    error_train = np.mean((prediction_train != y_train).astype(int))
    print("Accuracy on training set =  %.2lf" % ((1 - error_train) * 100))
    prediction_val = clf.predict(x_val)
    error_val = np.mean((prediction_val != y_val).astype(int))
    print("Accuracy on cross-validation set =  %.2lf" % ((1 - error_val) * 100))
    prediction_test = clf.predict(x_test)
    error_test = np.mean((prediction_test != y_test).astype(int))
    print("Accuracy on test set =  %.2lf" % ((1 - error_test) * 100))
    prediction_all = clf.predict(x_all)
    error_all = np.mean((prediction_all != y_all).astype(int))
    print("Accuracy on all set =  %.2lf" % ((1 - error_all) * 100))
    prediction_full = clf.predict(x_full)
    error_full = np.mean((prediction_full != y_full).astype(int))
    print("Accuracy on full set =  %.2lf" % ((1 - error_full) * 100))


def plot_decision_boundary(x, y, clf, h=0.2):
    # create a mesh to plot in
    # x_min, x_max = x[:, 0].min() - 0.1, x[:, 0].max() + 0.1
    # y_min, y_max = x[:, 1].min() - 0.1, x[:, 1].max() + 0.1
    x_min, x_max = -1, 1
    y_min, y_max = -1, 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    # Plot also the training points
    plt.figure(figsize=(16, 9), dpi=200)
    plt.contourf(xx, yy, z, cmap=plt.cm.coolwarm, alpha=0.8)
    plt.scatter(x[:, 0], x[:, 1], c=y, cmap=plt.cm.coolwarm)
    plt.xlabel(r"$\lambda$")
    plt.ylabel(r"$\frac{\lambda_{max}}{\lambda_{min}}$")
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.show()


def feature_scaling(x, mu=[], sigma=[]):
    if mu == []:
        mu_1 = np.mean(x[:, 0])
        mu_2 = np.mean(x[:, 1])
    else:
        mu_1 = mu[0]
        mu_2 = mu[1]
    if sigma == []:
        sigma_1 = max(x[:, 0]) - min(x[:, 0])
        sigma_2 = max(x[:, 1]) - min(x[:, 1])
    else:
        sigma_1 = sigma[0]
        sigma_2 = sigma[1]
    x[:, 0] = (x[:, 0] - mu_1) / sigma_1
    x[:, 1] = (x[:, 1] - mu_2) / sigma_2
    return x, [mu_1, mu_2], [sigma_1, sigma_2]


#%% Data preparation
data_full = loadtxt("eigenvalues6.csv", delimiter=",")
np.random.shuffle(data_full)
data_1 = data_full[data_full[:, 2] == 1]
data_0 = data_full[data_full[:, 2] == 0]
data = np.append(data_0[0:2000], data_1[0:2000], axis=0)
np.random.shuffle(data)
x_all, mu, sigma = feature_scaling(data[:, 0:2])
y_all = data[:, 2]
n_train = int(data.shape[0] * 0.6)
n_val = int(data.shape[0] * 0.2)
n_test = data.shape[0] - n_train - n_val
x_train = x_all[0:n_train, :]
y_train = y_all[0:n_train]
x_val = x_all[n_train : n_train + n_val, :]
y_val = y_all[n_train : n_train + n_val]
x_test = x_all[n_train + n_val :, :]
y_test = y_all[n_train + n_val :]
x_full, _, _ = feature_scaling(data_full[:, 0:2], mu, sigma)
y_full = data_full[:, 2]

#%% Polynomial
clf = polynomial_parameters(x_train, y_train, x_val, y_val)
#%%
model_accuracy(clf, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full)
plot_decision_boundary(x_full, y_full, clf, h=0.01)

# %% RBF
clf = rbf_parameters(x_train, y_train, x_val, y_val)
#%%
model_accuracy(clf, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full)
plot_decision_boundary(x_full, y_full, clf, h=0.01)


# %%
clf = sigmoid_parameters(x_train, y_train, x_val, y_val)
#%%
model_accuracy(clf, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full)
plot_decision_boundary(x_full, y_full, clf, h=0.01)
# %%
