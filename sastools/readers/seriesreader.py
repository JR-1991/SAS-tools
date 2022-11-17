from typing import List

import pandas as pd
from pyaniml import AnIMLDocument


class SeriesReader:
    """
    Read an AnIML document and create a `pandas.DataFrame` from any 
    SeriesSet within.
    """

    def __init__(self, animl_doc: AnIMLDocument):
        self.animl_doc = animl_doc
        self.seriesID = []

    def __repr__(self):
        return "SeriesReader"

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
                    for category in result.content:
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
                        for category in result.content:
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
