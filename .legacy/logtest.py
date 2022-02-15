from loggerfromjson import logger_from_json


logger = logger_from_json(
    json_cfg_file="./notebooks/testing/logcfg.json",
    custom_filename="SAXS-workflow"
)
logger.name = __name__


def main():
    logger.debug("Starting logging.")
    print("Doing some magic!")
    x = 1024
    y = 0
    logger.info(f"Setting x={x} and y={y}.")
    try:
        x / y
    except ZeroDivisionError:
        logger.exception(
            f"The divison by zero is undefined.",
            exc_info=True
        )
    print("Done some magic!")
    logger.debug("Finished logging.")


if __name__ == "__main__":
    main()
