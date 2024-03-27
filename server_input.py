from cv2.typing import MatLike
import numpy as np

Mat = np.typing.NDArray[np.uint8]

def get_points(image: MatLike):
    print('Image received')
    return [(1,1), (2,2), (3,3), (4,4)]