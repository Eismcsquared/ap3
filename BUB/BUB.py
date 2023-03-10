import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def readExcel(path):
    return pd.read_excel(f"file://localhost/{path}")


def calculateAlpha(data):
    alpha = [data["d"][i] / (2 * data["l"][i]) for i in range(len(data["d"]))]
    # err_alpha = [alpha[i] * np.sqrt((data["err_d"][i] / data["d"][i]) ** 2 + (data["err_l"][i] / data["l"][i]) ** 2) for i in range(len(data["d"]))]

    return pd.DataFrame({"alpha": alpha})


def calculateSinusAlpha(data):
    sin_alpha = [data["d"][i] / np.sqrt(data["d"][i] ** 2 + 4 * data["l"][i] ** 2) for i in range(len(data))]
#   err_sin_alpha = [4 * np.sqrt(data["l"][i] ** 4 * data["err_d"][i] ** 2 + data["l"][i] ** 2 * data["d"][i] ** 2 * data["err_l"][i] ** 2) / (np.sqrt(data["d"][i] ** 2 + 4 * data["l"][i] ** 2) ** 3) for i in range(len(data))]
    return pd.DataFrame({"alpha": sin_alpha})

def weightedLinearRegression(data):
    length = len(data)
    alpha = np.empty(length)
    err_alpha = np.empty(length)
    n = np.empty(length)
    for i in range(length):
        alpha[i] = data["alpha"][i]
        err_alpha[i] = data["err_alpha"][i]
        n[i] = data["n"][i]
    weight = 1 / err_alpha ** 2
    D = np.sum(weight) * np.dot(weight, n ** 2) - np.dot(weight, n) ** 2
    a0 = (np.dot(weight, n ** 2) * np.dot(weight, alpha) - np.dot(weight, n) * np.dot(weight, alpha * n)) / D
    a1 = (np.sum(weight) * np.dot(weight, alpha * n) - np.dot(weight, n) * np.dot(weight, alpha)) / D
    result = lambda x: a0 + a1 * x
    stdDev = np.sqrt(np.dot(weight, (alpha - result(n)) ** 2) / (length - 2))
    err_a1 = stdDev * np.sqrt(np.sum(weight) / D)
    print(f"lineare Regression: y = {a1}x + {a0}")
    print(f"Unsicherheit des Anstiegs: {err_a1}")
    return result


def linearRegression(data):
    length = len(data)
    alpha = np.empty(length)
    n = np.empty(length)
    for i in range(length):
        alpha[i] = data["alpha"][i]
        n[i] = data["n"][i]
    D = length * np.dot(n, n) - np.sum(n) ** 2
    a0 = (np.dot(n, n) * np.sum(alpha) - np.sum(n) * np.dot(n, alpha)) / D
    a1 = (length * np.dot(n, alpha) - np.sum(n) * np.sum(alpha)) / D
    result = lambda x: a0 + a1 * x
    stdDev = np.sqrt(np.sum((alpha - result(n)) ** 2) / (length - 2))
    err_a1 = stdDev * np.sqrt(length / D)
    print(f"lineare Regression: y = {a1}x + {a0}")
    print(f"Unsicherheit des Anstiegs: {err_a1}")
    return result

def plotWithoutErrorBar(data, funcY):
    ln = data["l"].unique()
    l1 = ln[0]
    l2 = ln[1]
    l3 = ln[2]
    a = funcY(data)
    data["alpha"] = a["alpha"]
    data_l1 = data[data["l"] == l1]
    data_l2 = data[data["l"] == l2]
    data_l3 = data[data["l"] == l3]
    plt.plot(data_l1["n"], data_l1["alpha"], "o", mfc="none", mec="r")
    plt.plot(data_l2["n"], data_l2["alpha"], "o", mfc="none", mec="b")
    plt.plot(data_l3["n"], data_l3["alpha"], "o", mfc="none", mec="g")
    plt.xlabel("Ordnung n")
    plt.ylabel(f"sin{chr(945)}")
    x = np.linspace(0, 7.5, 100)
    plt.plot(x, linearRegression(data)(x), color="black")
    plt.show()

#   plt.errorbar(data_l1["n"], data_l1["alpha"], data_l1["err_alpha"], fmt="ro", capsize=3)
#   plt.errorbar(data_l2["n"], data_l2["alpha"], data_l2["err_alpha"], fmt="bo", capsize=3)
#   plt.errorbar(data_l3["n"], data_l3["alpha"], data_l3["err_alpha"], fmt="go", capsize=3)


""" 
Für den ersten Versuchsteil einkommentieren. Ersetze "path/to/repository" durch den absoluten Pfad des aktuellen Verzeichnisses.
Füge in data.xlsx die Messdaten ein, l steht für den Gitter-Schirm-Abstand, d für den Abstand der beiden Minima, n für die Ordnung
"""
# df = readExcel("path/to/repository/ap3/BUB/data.xlsx")
# plotWithoutErrorBar(df, calculateAlpha)

"""
Für den zweiten Versuchsteil einkommentieren. Analog wie oben. Nutze <color>.xlsx für die Messdaten der entsprechenden Spektrallinie
"""
# df = readExcel("path/to/repository/ap3/BUB/orange.xlsx")
# plotWithoutErrorBar(df, calculateSinusAlpha)
