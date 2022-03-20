from datetime import date
import os
from pathlib import Path
from typing import List, Union

import pandas as pd
from pyaniml import AnIMLDocument

from modules.loggerfromjson import logger_from_json

print(f"Initializing logger for '{__name__}'.")
logger = logger_from_json(Path(__file__).parents[2] / "logs/")
logger.name = __name__

cwd = Path.cwd()
path_to_datasets = cwd / "./notebooks/datasets/"


class TSVWriter:
    """Create a TSV file from a SeriesSet within an AnIML document."""

    def __init__(self, animl_doc: AnIMLDocument):
        logger.debug(
            f"Constructor called, '{self.__repr__()}'@{hex(id(self))} initialised."
        )
        self.animl_doc = animl_doc
        self.seriesID = []

    def __del__(self):
        logger.debug(
            f"Destructor called, '{self.__repr__()}'@{hex(id(self))} deleted."
        )

    def __repr__(self):
        return "TSVWriter"

    def available_seriesIDs(self) -> List[str]:
        available_seriesIDs = []
        experiment_steps = self.animl_doc.experiment_step_set.experiment_steps
        for experiment_step in experiment_steps:
            results = experiment_step.result.results
            for result in results:
                # Check Series in Result
                try:
                    available_seriesIDs.append(result.id[:-2])
                except:
                    pass
                # Check Series in Result.SeriesSet
                try:
                    for series in result.series:
                        available_seriesIDs.append(series.id[:-2])
                except:
                    pass
                # Check Categories
                try:
                    for category in result.categories:
                        # Check for Series in Result.Category
                        try:
                            available_seriesIDs.append(category.id[:-2])
                        except:
                            pass
                        # Check for Series in Result.Category.SeriesSet
                        try:
                            for series in category.series:
                                available_seriesIDs.append(series.id[:-2])
                        except:
                            pass
                except:
                    pass
        return list(dict.fromkeys(available_seriesIDs))

    def add_seriesID(self, list_of_ids: List[str]) -> None:
        for _ in list_of_ids:
            self.seriesID.append(_)

    def create_dataframe(self) -> pd.DataFrame:
        dict_of_data = {}
        for sample_id in self.seriesID:
            experiment_steps = (
                self.animl_doc.experiment_step_set.experiment_steps
            )
            for experiment_step in experiment_steps:
                results = experiment_step.result.results
                for result in results:
                    # Check Series in Result
                    try:
                        if sample_id in result.id:
                            dict_of_data[
                                result.id
                            ] = result.individual_value_set.data
                    except:
                        pass
                    # Check Series in Result.SeriesSet
                    try:
                        for series in result.series:
                            if sample_id in series.id:
                                dict_of_data[
                                    series.id
                                ] = series.individual_value_set.data
                    except:
                        pass
                    # Check Categories
                    try:
                        for category in result.categories:
                            # Check for Series in Result.Category
                            try:
                                if sample_id in category.id:
                                    dict_of_data[
                                        category.id
                                    ] = category.individual_value_set.data
                            except:
                                pass
                            # Check for Series in Result.Category.SeriesSet
                            try:
                                for series in category.series:
                                    if sample_id in series.id:
                                        dict_of_data[
                                            series.id
                                        ] = series.individual_value_set.data
                            except:
                                pass

                    except:
                        pass
        return pd.DataFrame(
            {key: pd.Series(value) for key, value in dict_of_data.items()}
        )

    def create_tsv(
        self, df: pd.DataFrame, path: Union[str, bytes, os.PathLike]
    ) -> None:
        file = Path(path)
        df.to_csv(path_or_buf=file, sep="\t", index=False)


def main():
    path = path_to_datasets / "download/fairsaxs_220316.animl"
    with path.open("r") as f:
        xml_string = f.read()
        doc = AnIMLDocument.fromXMLString(xml_string)

    test = TSVWriter(doc)
    test.add_seriesID(
        ["OTAB_095wtp_T030", "OTAB_100wtp_T090", "CholPal_20220214"]
    )
    df = test.create_dataframe()
    test.create_tsv(df, (path_to_datasets / "processed/fairsaxs_220316.tsv"))


if __name__ == "__main__":
    main()
