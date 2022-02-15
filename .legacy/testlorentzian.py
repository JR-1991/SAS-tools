from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from pyaniml import AnIMLDocument, Sample, Device, ExperimentStep, Category, Parameter, SeriesSet, Series, IndividualValueSet


CWD = Path.cwd()
PATH_TO_INPUT = Path(CWD / "./notebooks/testing/lorentz.txt")
PATH_TO_OUTPUT = Path(CWD / "./notebooks/testing/test.animl")


@dataclass
class ReadOriginLorentz:
    """ Dataclass for handling Lorentzian data from Origin TXT file. """

    file: str

    def __post_init__(self):
        file = Path(self.file)
        with file.open("r") as txt:
            self.dataframe = pd.read_table(
                filepath_or_buffer=txt,
                header=0,
                names=[
                    "quantity",
                    "symbol",
                    "value",
                    "stddev",
                    "t-value",
                    "probabililty",
                    "dependency"
                ],
                engine="python"
            )
        self.xc_values = self.dataframe.loc[self.dataframe["symbol"] == "xc"]

    def get_full_dataframe(self):
        return self.dataframe

    def get_xc_dataframe(self):
        return self.xc_values


if __name__ == "__main__":
# Prepare the external Origin Lorentz data as a pandas DataFrame
    lorentz = ReadOriginLorentz(PATH_TO_INPUT)  


# Set up a mockup AnIMLDocument
    animl = AnIMLDocument()

    sample = Sample(
        name="SI06",
        id="si06",
    )
    animl.add_sample(sample)

    data_evaluation = ExperimentStep(
        name="Data evaluation",
        experiment_step_id="es01"
    )

    device = Device(
        name="Microsoft Windows 10 Pro Personal Computer",
        firmware_version="10.0.19044",
        serial_number=""
    )
    data_evaluation.add_method(device)

    method = Category(
        name="Spectral analysis",
        parameters=[
            Parameter(
                name="Software",
                parameter_type="String",
                value="Origin Lab Origin"
            )
        ]
    )
    data_evaluation.add_method(method)

    lorentz_results = SeriesSet(
        name="Lorentz fit and standard deviation",
        series=[
            Series(
                name="xc values",
                id="xc",
                data_type="Float32",
                dependency="independent",
                plot_scale="None",
                data=IndividualValueSet(
                    lorentz.get_xc_dataframe()["value"].tolist()
                )
            ),
            Series(
                name="Standard deviation",
                id="stddev",
                data_type="Float32",
                dependency="independent",
                plot_scale="None",
                data=IndividualValueSet(
                    lorentz.get_xc_dataframe()["stddev"].tolist()
                )
            )
        ]
    )
    data_evaluation.add_result(lorentz_results)

    animl.add_experiment_step(data_evaluation)

    with PATH_TO_OUTPUT.open("w") as f:
        f.write(animl.toXML())

    print(lorentz.get_xc_dataframe()["value"])