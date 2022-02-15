import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lmfit.models import LorentzianModel


class EvaluationToolkit:
    """Various tools for the data evaluation of SAXS experiments."""

    def lorentzian_on_calibration(self, dataframe: pd.DataFrame):
        
        q = dataframe["scattering_vector"]
        # peak 1: 0.6 < q < 1.5
        peak1_dataframe = dataframe.loc[(q > 0.6) & (q < 1.5)]
        # peak 2: 1.5 < q < 3.0
        peak2_dataframe = dataframe.loc[(q > 1.5) & (q < 3.0)]
        # peak 3: 3.0 < q < 4.0
        peak3_dataframe = dataframe.loc[(q > 3.0) & (q < 4.0)]

        model = LorentzianModel()
        parameters = model.guess(
            data=np.array(peak1_dataframe["scattering_vector"].tolist()),
            x=np.array(peak1_dataframe["counts_per_area"].tolist())
        )
        result = model.fit(
            data=np.array(peak1_dataframe["scattering_vector"].tolist()),
            x=np.array(peak1_dataframe["counts_per_area"].tolist()),
            params=parameters
        )
        res_fit = []
        for item in (result.fit_report()).split():
            try:
                res_fit.append(float(item))
            except ValueError:
                pass
        cal_q.append(res_fit[9])

        fig = plt.figure()
        fig.add_subplot(1,1,1).plot(
            dataframe["scattering_vector"], 
            dataframe["counts_per_area"], 
            marker = ",", 
            color = "orange", 
            label = "diffractogram"
        )
        plt.xlabel("$q$ / $\mathrm{nm}^{-1}$")
        plt.ylabel("$I$ / a.u.")
        plt.xlim(0,5)
        plt.ylim(0, (max(dataframe["counts_per_area"])+(0.1*max(dataframe["counts_per_area"]))))

        fig.add_subplot(1,1,1).plot(np.array(peak1_dataframe["counts_per_area"].tolist()), result.best_fit, linestyle = ':', color = 'blue', label = 'best fit')
        plt.legend(frameon=False)
        plt.show()

        # calibration_peaks[0], calibration_peaks[1], fig, fig.add_subplot(1,1,1), cal_q       
        # LorentzFit(calibration_peaks[2], calibration_peaks[3], fig, fig.add_subplot(1,1,1), cal_q)
        # LorentzFit(calibration_peaks[4], calibration_peaks[5], fig, fig.add_subplot(1,1,1), cal_q)


if __name__ == "__main__":
    toolkit = EvaluationToolkit()

    cal_i = [0.0, 1.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0]
    cal_q = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2]
    dataframe = pd.DataFrame(list(zip(cal_q, cal_i)), 
        columns = ["scattering_vector", "counts_per_area"])
    toolkit.lorentzian_on_calibration(dataframe)
