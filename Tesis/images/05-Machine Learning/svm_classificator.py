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
    degree_array=(np.arange(3) + 2),
    c_array=np.array([0.01, 0.03, 0.1, 0.3, 1, 3, 10]),
    gamma_array=np.array([0.01, 0.03, 0.1, 0.3, 0.7, 1, 3, 10, 30, 50]),
    coef0_array=np.array([0, 0.01, 0.03, 0.5, 0.1, 0.3, 0.5, 0.7, 1]),
):
    error_min = 1
    for i in range(c_array.size):
        for j in range(degree_array.size):
            for k in range(coef0_array.size):
                for l in range(gamma_array.size):
                    clf = svm.SVC(
                        C=c_array[i],
                        kernel="poly",
                        gamma=gamma_array[l],
                        degree=degree_array[j],
                        coef0=coef0_array[k],
                    ).fit(x_train, y_train)
                    predictions = clf.predict(x_val)
                    error = np.mean((predictions != y_val).astype(int))
                    print(
                        "degree = %.2lf, C = %.2lf, gamma = %.2lf, r = %.2lf, error = %.6lf"
                        % (
                            degree_array[j],
                            c_array[i],
                            gamma_array[l],
                            coef0_array[k],
                            error,
                        )
                    )
                    if error < error_min:
                        c = c_array[i]
                        degree = degree_array[j]
                        r = coef0_array[k]
                        gamma = gamma_array[l]
                        error_min = error
    print(
        "Final parameters: C = %.2lf, degree = %.2lf, gamma = %.2lf, r = %.2lf"
        % (c, degree, gamma, r)
    )
    clf = svm.SVC(C=c, kernel="poly", gamma=gamma, degree=degree, coef0=r).fit(
        x_train, y_train
    )
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


def sigmoid_parameters(
    x_train,
    y_train,
    x_val,
    y_val,
    c_array=np.array([0.01, 0.03, 0.1, 0.3, 0.7, 1, 3, 10, 30, 50]),
    gamma_array=np.array([0.01, 0.03, 0.1, 0.3, 0.7, 1, 3, 10, 30, 50]),
    coef0_array=np.array([0, 0.01, 0.03, 0.1, 0.3, 0.7, 1, 3, 10, 30]),
):
    error_min = 1
    for i in range(c_array.size):
        for j in range(gamma_array.size):
            for k in range(coef0_array.size):
                clf = svm.SVC(
                    C=c_array[i],
                    kernel="sigmoid",
                    gamma=gamma_array[j],
                    coef0=coef0_array[k],
                ).fit(x_train, y_train)
                predictions = clf.predict(x_val)
                error = np.mean((predictions != y_val).astype(int))
                print(
                    "C = %.2lf, gamma = %.2lf, r = %.2lf, error = %.6lf"
                    % (c_array[i], gamma_array[j], coef0_array[k], error)
                )
                if error < error_min:
                    c = c_array[i]
                    gamma = gamma_array[j]
                    r = coef0_array[k]
                    error_min = error
    print("Final parameters: C = %.2lf, gamma = %.2lf, r = %.2lf" % (c, gamma, r))
    clf = svm.SVC(C=c, kernel="sigmoid", gamma=gamma, coef0=r).fit(x_train, y_train)
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


def plot_decision_boundary(x, y, clf, h=0.2, filename="plot.png"):
    # create a mesh to plot in
    x_min, x_max = x[:, 0].min() - 0.1, x[:, 0].max() + 0.1
    y_min, y_max = x[:, 1].min() - 0.1, x[:, 1].max() + 0.1
    # x_min, x_max = -1, 1
    # y_min, y_max = -1, 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    # Plot also the training points
    fig = plt.figure(figsize=(10, 5), dpi=100)
    ax = plt.subplot()
    ax.contourf(xx, yy, z, cmap=plt.cm.coolwarm, alpha=0.8)
    ax.scatter(
        x[y == 1, 0],
        x[y == 1, 1],
        s=2,
        c="r",
        cmap=plt.cm.coolwarm,
        label=r"$\lambda_S$",
    )
    ax.scatter(
        x[y == 0, 0],
        x[y == 0, 1],
        s=2,
        c="b",
        cmap=plt.cm.coolwarm,
        label=r"$\lambda_W$",
    )

    ax.set_xlabel(r"$\lambda$")
    ax.set_ylabel(r"$\hat{\mathrm{SNR}}$")
    ax.legend()
    ax.set_xticks([])
    ax.set_yticks([])
    #    plt.xlim(x[:,0].min(), x[:,0].max())
    #    plt.ylim(x[:,1].min(), x[:,1].max())
    plt.savefig(filename, dpi=300, bbox_inches="tight")
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
data_full = loadtxt("eigenvalues_4signals.csv", delimiter=",")
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

#%%
#%% Data preparation
data_full = loadtxt("eigenvalues_4signals.csv", delimiter=",")
np.random.shuffle(data_full)
data_1 = data_full[data_full[:, 2] == 1]
data_0 = data_full[data_full[:, 2] == 0]
data = np.append(data_0[0:10000], data_1[0:10000], axis=0)
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
clf_poly = polynomial_parameters(x_train, y_train, x_val, y_val)
#%%
model_accuracy(clf_poly, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full)
plot_decision_boundary(x_test, y_test, clf_poly, h=0.01, filename="ml_svm_poly.png")

# %% RBF
clf_rbf = rbf_parameters(x_train, y_train, x_val, y_val)
#%%
model_accuracy(clf_rbf, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full)
plot_decision_boundary(x_test, y_test, clf_rbf, h=0.01, filename="ml_svm_rbf.png")

#%%
# %% SIGMOID
clf_sigmoid = sigmoid_parameters(x_train, y_train, x_val, y_val)
model_accuracy(
    clf_sigmoid, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full
)
plot_decision_boundary(
    x_test, y_test, clf_sigmoid, h=0.01, filename="ml_svm_sigmoid.png"
)

# %%
# Plot also the training points
plt.figure(figsize=(10, 5), dpi=200)
plt.scatter(data_1[0:2000, 0], 2 * data_1[0:2000, 1], s=2, c="r")
plt.scatter(data_0[0:2000, 0], 2 * data_0[0:2000, 1], s=2, c="b")
plt.legend([r"$\lambda_S$", r"$\lambda_W$"])
plt.xlabel(r"$\lambda$")
plt.ylabel(r"$\hat{\mathrm{SNR}}$")
plt.grid()
plt.savefig("ml_avals_plot.png", dpi=300, bbox_inches="tight")
plt.show()
# %%
data_full[:, 0]
# %% RBF
clf = rbf_parameters(x_train, y_train, x_val, y_val)
#%%
model_accuracy(clf, x_train, y_train, x_val, y_val, x_test, y_test, x_full, y_full)
plot_decision_boundary(x_full, y_full, clf, h=0.01)
#%%
x_test[:, 0].min()
# %%
h = 0.01
x_min, x_max = x_test[:, 0].min() - 0.1, x_test[:, 0].max() + 0.1
y_min, y_max = x_test[:, 1].min() - 0.1, x_test[:, 1].max() + 0.1
# x_min, x_max = -1, 1
# y_min, y_max = -1, 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
z = clf_sigmoid.predict(np.c_[xx.ravel(), yy.ravel()])
z = z.reshape(xx.shape)

# Plot also the training points
fig = plt.figure(figsize=(10, 5), dpi=100)
ax = plt.subplot()
ax.contourf(xx, yy, z, cmap=plt.cm.coolwarm, alpha=0.8)
ax.scatter(
    x_test[y_test == 1, 0], x_test[y_test == 1, 1], s=2, c="r", cmap=plt.cm.coolwarm
)
ax.scatter(
    x_test[y_test == 0, 0],
    x_test[y_test == 0, 1],
    s=2,
    c="b",
    cmap=plt.cm.coolwarm,
    label=r"$\lambda_W$",
)
ax.legend()
ax.set_xlabel(r"$\lambda$")
ax.set_ylabel(r"$\hat{\mathrm{SNR}}$")
# plt.legend([_,r"$\lambda_S$", r"$\lambda_W$"])
ax.set_xticks([])
ax.set_yticks([])
#    plt.xlim(x[:,0].min(), x[:,0].max())
#    plt.ylim(x[:,1].min(), x[:,1].max())
# plt.savefig(filename, dpi=300, bbox_inches="tight")
plt.show()
# %%
