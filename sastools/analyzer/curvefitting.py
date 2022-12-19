import json
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lmfit import models
from lmfit.model import save_modelresult, load_modelresult
from scipy import signal

class Analyzer():

    def __init__(self, experimental_data : pd.DataFrame):
        """ Initializing the x and y  values  for the fit"""

        self.exp_data = experimental_data
        self.x = self.exp_data.iloc[:,0].values.tolist()
        self.y = self.exp_data.iloc[:,1].values.tolist()

    def pack_data_into_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        spec_dict = {
            'data': {
                'x': self.x,
                'y': self.y
            }
        }
        return spec_dict

    def plot_data(self):
        exp_data_plot = sns.lineplot(x = 'scattering_vector', y = 'counts_per_area', data=self.exp_data)
        exp_data_fig = exp_data_plot.get_figure()
        exp_data_fig.savefig('exp_data_plot.png', facecolor='white', transparent=False, dpi=600)

    def find_peaks_cwt(self, peak_widths=(20,), cutoff_amplitude=None):
        self.c = cutoff_amplitude
        self.w = peak_widths
        peak_indices = signal.find_peaks_cwt(self.y, self.w)
        x_val_peak = [self.x[peak_index] for peak_index in peak_indices]
        y_val_peak = [self.y[peak_index] for peak_index in peak_indices]
        self.peak_dict = {}
        for i in range(len(x_val_peak)):
            self.peak_dict[x_val_peak[i]] = y_val_peak[i]
        if self.c != None:
            self.peak_dict = {key:val for key, val in self.peak_dict.items() if val >= self.c}
        self.n_peaks = len(self.peak_dict)
        print('number of found peaks:', self.n_peaks)
        j=1
        for key, value in self.peak_dict.items():
            print('peak number:', j, 'x:', key, 'y:', value)
            j=j+1
        peak_fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        for i in self.peak_dict:
            ax.axvline(i, c='black', linestyle='dotted')
        peak_fig.savefig('found_peaks.png', facecolor='white', transparent=False, dpi = 600)

    def set_specifications_manually(self, number_of_models, model_specifications):
        self.n_models= number_of_models
        self.models = model_specifications
        spec_dict = self.pack_data_into_dict()
        models_list = []
        for model in self.models:
            model_dict = {
                'type': model[0],
                'params': {
                    'center': model[1][0],
                    'height': model[1][1],
                    'sigma': model[1][2]
                },
                'help': {
                    'center': {
                        'min':model[2][0],
                        'max':model[2][1]
                    }
                }
            }
            models_list.append(model_dict)
        spec_dict.update({'models': models_list})
        json_models_dict = json.dumps(spec_dict, indent=4)
        with open("models_dict.json", "w") as outfile:
            outfile.write(json_models_dict)

    def set_specifications_automatically(self, tolerance, model_type):
        self.model_type = model_type
        t = tolerance
        x_range = np.max(self.x) - np.min(self.x)
        spec_dict =self.pack_data_into_dict()
        models_list = []
        for x, y in self.peak_dict.items():
            model_dict = {
                'type': self.model_type,
                'params': {
                    'center': x,
                    'height': y,
                    'sigma': x_range / len(self.peak_dict) * np.min(self.w)
                },
                'help': {
                    'center': {
                        'min': (x-t),
                        'max': (x+t)
                    }
                }
            }
            models_list.append(model_dict)
        spec_dict.update({'models':models_list})
        json_models_dict = json.dumps(spec_dict, indent=4)
        with open("models_dict.json", "w") as outfile:
            outfile.write(json_models_dict)

    def generate_model(self, speci):
        composite_model = None
        params = None
        x_min = np.min(speci['data']['x'])
        x_max = np.max(speci['data']['x'])
        x_range = x_max - x_min
        y_max = np.max(speci['data']['y'])
        for i, basis_func in enumerate(speci['models']):
            prefix = f'model{i}_'
            model = getattr(models, basis_func['type'])(prefix=prefix)
            if basis_func['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']: # for VoigtModel gamma is constrained to sigma
                model.set_param_hint('sigma', min=1e-6, max=x_range)
                model.set_param_hint('center', min=x_min, max=x_max)
                model.set_param_hint('height', min=1e-6, max=1.1*y_max)
                model.set_param_hint('amplitude', min=1e-6)
                default_params = {
                    prefix+'center': x_min + x_range * random.random(),
                    prefix+'height': y_max * random.random(),
                    prefix+'sigma': x_range * random.random()
                }
            else:
                raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
            if 'help' in basis_func:  # allow override of settings in parameter
                for param, options in basis_func['help'].items():
                    model.set_param_hint(param, **options)
            model_params = model.make_params(**default_params, **basis_func.get('params', {}))
            if params is None:
                params = model_params
            else:
                params.update(model_params)
            if composite_model is None:
                composite_model = model
            else:
                composite_model = composite_model + model
        return composite_model, params

    def fit(self):
        with open('models_dict.json', 'r') as outfile:
            speci = json.load(outfile)
        model, params = self.generate_model(speci)
        model_result = model.fit(speci['data']['y'], params, x = speci['data']['x'])
        save_modelresult(model_result, 'model_result.sav')

    def list_of_model_centers(self):
        model_result = load_modelresult('model_result.sav')
        list_xc= []
        for i in range(self.n_peaks):
            list_xc.append(model_result.best_values[f'model{i}_center'])
        with open('list_xc.txt', 'w') as f:
            for line in list_xc:
                f.write(f"{line}\n")

    def plot_fit(self):
        model_result = load_modelresult('model_result.sav')
        # print(model_result.fit_report())
        fig = model_result.plot(data_kws={'markersize': 0.5})
        fig.axes[0].set_title('')
        fig.savefig('model_result.png', facecolor = 'white', dpi=600)
        print(model_result.best_values)
