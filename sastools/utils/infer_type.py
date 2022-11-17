import numpy


def infer_type(var_to_infer) -> str:
    if isinstance(var_to_infer, str):
        return "String"
    elif isinstance(var_to_infer, numpy.int32):
        return "Int32"
    elif isinstance(var_to_infer, (int or numpy.int64)):
        return "Int64"
    elif isinstance(var_to_infer, numpy.float32):
        return "Float32"
    elif isinstance(var_to_infer, (float or numpy.float64)):
        return "Float64"
    elif isinstance(var_to_infer, bool):
        return "Boolean"
    else:
        raise ValueError(f"{type(var_to_infer)} not a valid type.")
