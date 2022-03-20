"""
This module contains a function that reads a `loggin.config` JSON file 
and returns the corresponding `Logger` instance.
"""


import json
import logging
import logging.config
import os
from pathlib import Path
from typing import Union


def logger_from_json(
    logs_directory: Union[str, bytes, os.PathLike], custom_filename: str = None
) -> logging.Logger:
    """
    Create a logging.Logger object from JSON configuration file.

    Args:
        json_cfg_file (str): Path to  logging.config-conform JSON file
        custom_filename (str, optional): Provide optional custom name
        for the logfile (default: notebook.log). Defaults to None.

    Returns:
        logging.Logger: Logger instance according to config file.
        Don't forget to change Logger.name to __name__!
    """

    # Load json_cfg_file for logger and get the filename from it
    json_cfg_file = list(Path(logs_directory).glob("**/*.json"))[0]
    print(f"Loading logger configuration from '{json_cfg_file.name}'.")
    with json_cfg_file.open("r") as f:
        logcfg = json.load(f)

    # Replace filename in logcfg string with full Path
    path_to_log = Path(
        logs_directory / logcfg["handlers"]["file_handler"]["filename"]
    )
    logcfg["handlers"]["file_handler"]["filename"] = path_to_log

    # Replace logfile stem if custom_filename was given
    if custom_filename:
        filename = Path(custom_filename).stem
        path_to_log = path_to_log.with_stem(filename)
        logcfg["handlers"]["file_handler"]["filename"] = path_to_log

    # Create logfile and required directories along the resolved path
    path_to_log.resolve()
    path_to_log.parent.mkdir(parents=True, exist_ok=True)
    path_to_log.touch(exist_ok=True)

    # Load configuration as dict into logging.config
    logging.config.dictConfig(logcfg)

    # Create and return Logger instance from logging.config
    logger = logging.getLogger("standard")
    print("Done.")

    return logger
