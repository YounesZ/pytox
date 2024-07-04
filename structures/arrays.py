import numpy as np
from ...pytox.utils.decorators import validate_arguments


@validate_arguments
def shape_as_column_vector(vec: np.ndarray) -> np.ndarray:

    shp = vec.shape
    assert len(shp)>0 and len(shp)<3
    if len(shp)==1:
        # Reshape
        vec = np.expand_dims(vec, 1)

    return vec

