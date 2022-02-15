import os
import csv

import matplotlib.pyplot as plt

from modules.legacyfunctions import *
from modules.newfunctions import to_array
from modules.saxslicer import SAXSlicer


class DataExtracion:

    def __init__(self, path, calibration_file):
        self.path = path
        self.file = calibration_file
        self.calibration_file = self.path + self.file
        self.slic = SAXSlicer()
        self.data = self.slic.extract_data()
        self.metadata = self.slic.extract_metadata()

    def process_calibration(self, input: str):
        q = self.data["scattering_vector"]
        i = self.data["counts_per_area"]
        peaks = to_array(self.data)
        if input == "q":
            output = q
        elif input == "i":
            output = i
        elif input == "peaks":
            output = peaks
        else:
            output = q, i, peaks
        return output
    
    def process_samples(self, input: str):
        files = os.listdir(self.path)
        list_of_files = [i for i in files if i.endswith("_lorentz.txt")]
        data_for_plot = [i for i in files if i.endswith("[7].pdh")]
        q_sample = []
        for current_file in list_of_files:
            print(f"Extracting data from {current_file}.")
            current_peak = self.slic.extract_lorentz(self.path, current_file)
            q_sample.append(current_peak)
        if input == "q":
            output = q_sample
        elif input == "plot":
            output = data_for_plot
        else:
            output = q_sample, data_for_plot
        return output


class Visualisation:

    def __init__(self, calibration_q, calibration_i, calibration_peaks):
        self.calibration_q = calibration_q
        self.calibration_i = calibration_i
        self.calibration_peaks = calibration_peaks
        self.fig = plt.figure()
        self.add = self.fig.add_subplot(1,1,1)

    def create_plot(self, colour: str = "orange"):
        self.add.plot(self.calibration_q, 
                 self.calibration_i, 
                 marker = ",", 
                 color = colour, 
                 label = "diffractogram"
                 )
        plt.xlabel("$q$ / $\mathrm{nm}^{-1}$")
        plt.ylabel("$I$ / a.u.")
        plt.xlim(0,5)
        plt.ylim(0, (max(self.calibration_i)+(0.1*max(self.calibration_i))))
    
    def do_lorentz(self):
        q_cholpal = []
        LorentzFit(self.calibration_peaks[0], self.calibration_peaks[1], self.fig, self.add, q_cholpal)
        plt.legend(frameon=False)
        LorentzFit(self.calibration_peaks[2], self.calibration_peaks[3], self.fig, self.add, q_cholpal)
        LorentzFit(self.calibration_peaks[4], self.calibration_peaks[5], self.fig, self.add, q_cholpal)
        return q_cholpal


class Analysis:
    
    def __init__(self, samples_q, samples_for_plot, q_cholpal):
        self.samples_q = samples_q
        self.samples_for_plot = samples_for_plot
        self.q_cholpal = q_cholpal
    
    def do_analysis(self):
        calc = []
        for peak in self.samples_q:
            calc.append(SAXScalc(self.q_cholpal, peak))
        dataEvaluation=[]
        for i, dataPlotItem in enumerate(self.samples_for_plot):
            name = [os.path.splitext(dataPlotItem)[0]]
            calcItem = calc[i]
            for i, calcItemItem in enumerate(calcItem):  
                for i, calcItemItemItem in enumerate(calcItemItem):
                    name.append(calcItemItem[i])
            dataEvaluation.append(name)
        return dataEvaluation

class Results:
    
    def __init__(self, path_to_read, samples_for_plot, data_evaluation, path_to_write):
        self.path_to_read = path_to_read
        self.samples_for_plot = samples_for_plot
        self.data_evaluation = data_evaluation
        self.path_to_write = path_to_write

    def write_to_tsv(self):
        header = ["sample", "$d_1$", "$d_2$", "$d_3$", "$d_2/d_1$", "$d_3/d_1$","LLC phase", "a"]
        path = self.path_to_write + "SAXS_results.tsv"
        with open(path, "w") as f:
            wr = csv.writer(f, delimiter="\t")
            wr.writerow(header)
            wr.writerows(self.data_evaluation)

    def plot_and_save_data(self, colour: str = "blue"):
        for dataPlotItem in self.samples_for_plot:
            name2 = self.path_to_read + dataPlotItem
            SAXSplt(name2, os.path.splitext(dataPlotItem)[0], colour)
