import matplotlib.pyplot as plt
import matlab as ml
import numpy as np
import pandas as pd

def readExcel(path):
    return pd.read_excel(f"file://localhost/{path}")

# calculate the average of a list/array of numbers
def average(values):
    avg = 0
    for v in values:
        avg += v
    avg /= len(values)
    return avg

# public static double average(double[] values) {
     # double avg = 0;
     # for (int i = 0; i < values.length; i++) {
         # avg += values[i];
     # }
     # return avg / values.length;
# }

# public static void main(String[] args) {
#     double[] arr = new double[]{1, 2, 3};
#     double a = average(arr);
# }
# calculate the standard deviation of the single values from their average
def standardDeviation(values):
    if len(values) <= 1:
        return -1
    acc = 0
    avg = average(values)
    for v in values:
        acc += (v - avg) ** 2
    return np.sqrt(acc / (len(values) - 1))

# calculate the standard deviation of the average of values
def errorOfAverage(values):
    return standardDeviation(values) / np.sqrt(len(values))

def calculateWaveLength(voltage):
    return 6.626e-34 * 2.9979e8 / (1.602e-19 * voltage)

def errorWaveLength(voltage, errorVoltage):
    waveLength = calculateWaveLength(voltage)
    return waveLength / voltage * errorVoltage

# run to calculate the average of voltage difference and the wave length inclusive error
raw_input = input("Geben Sie die Werte von Spannung in V ein, bei denen die Stromstärke maximal ist, jeweils getrennt durch ein Komma. Verwenden Sie \".\" als Dezimaltrennzeichen\n")
maxima = [float(v) for v in raw_input.split(",")]
maxima.sort()
raw_input = input("Geben Sie die Werte von Spannung in V ein, bei denen die Stromstärke minimal ist, jeweils getrennt durch ein Komma. Verwenden Sie \".\" als Dezimaltrennzeichen\n")
minima = [float(v) for v in raw_input.split(",")]
minima.sort()
voltages = []
for i in range(len(maxima) - 1):
    voltages.append(maxima[i+1] - maxima[i])
for i in range(len(minima) - 1):
    voltages.append(minima[i+1] - minima[i])
U = average(voltages)
delta_U = errorOfAverage(voltages)
lam = calculateWaveLength(U)
delta_lam = errorWaveLength(U, delta_U)
print(f"U = ({U}+-{delta_U})V")
print(f"lambda = ({lam * 1e9}+-{delta_lam * 1e9})nm")

