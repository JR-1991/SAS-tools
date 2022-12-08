import seaborn as sns
import pandas as pd


class Plotter:

    def __init__(self, df_exp_data: pd.DataFrame, **kwargs):
        
        self.df_exp_data = df_exp_data
        if kwargs.get('df_lit_data') != None:
            self.df_lit_data = kwargs['df_lit_data']
            self.lit_data_exists = True
        else:
            self.lit_data_exists = False
        

    def plotting(self):
        
        bias = min(self.df_exp_data.iloc[:, 1])
        #ns.set_theme(rc={'axes.facecolor':'darkslategray', 'figure.facecolor':'goldenrod', 'grid.color':'black', 'axes.edgecolor':'black'})
        #ns.set_context("notebook", font_scale=1.5)
        if self.lit_data_exists == True:
            self.df_lit_data.iloc[:, 1] = self.df_lit_data.iloc[:,1] + bias
            df_data = pd.concat([self.df_exp_data, self.df_lit_data], axis=1)
        #df_data.rename(columns = {'Angle': 'Angle1', 'Intensity': 'Intensity1','Angle': 'Angle2', 'Intensity': 'Intensity2'}, inplace=True)
        #print(df_data)
        
        if self.lit_data_exists == True:
            exp_data_plot = sns.lineplot(x = "Angle_exp", y = "Intensity_exp", data=df_data)
            sns.lineplot(x = "Angle_lit", y = "Intensity_lit", data=df_data)
        else:
            exp_data_plot = sns.lineplot(x = 'scattering_vector', y = 'counts_per_area', data=self.df_exp_data)
        exp_data_fig = exp_data_plot.get_figure()
        exp_data_fig.savefig('exp_data_plot.png', facecolor='white', transparent=False, dpi=600)
