import numpy as np


def to_array(dataframe):

    # peak 1: 0.6 < q < 1.3
    peak1_data_index = dataframe.index[(dataframe["scattering_vector"] > 0.6) & (dataframe["scattering_vector"] < 1.5)].tolist()
    peak1_data = dataframe.loc[peak1_data_index]
    q1 = np.array(peak1_data["scattering_vector"].tolist())
    i1 = np.array(peak1_data["counts_per_area"].tolist())

    # peak 2: 1.5 < q < 3
    peak2_data_index = dataframe.index[(dataframe["scattering_vector"] > 1.5) & (dataframe["scattering_vector"] < 3)].tolist()
    peak2_data = dataframe.loc[peak2_data_index]
    q2 = np.array(peak2_data["scattering_vector"].tolist())
    i2 = np.array(peak2_data["counts_per_area"].tolist())

    # peak 3: 3 < q < 4
    peak3_data_index = dataframe.index[(dataframe["scattering_vector"] > 3) & (dataframe["scattering_vector"] < 4)].tolist()
    peak3_data = dataframe.loc[peak3_data_index]
    q3 = np.array(peak3_data["scattering_vector"].tolist())
    i3 = np.array(peak3_data["counts_per_area"].tolist())

    return q1, i1, q2, i2, q3, i3