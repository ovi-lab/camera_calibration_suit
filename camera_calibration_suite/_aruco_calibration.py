# based on https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html

from typing import Union
import numpy as np
import cv2
from cv2 import aruco
from pathlib import Path
from loguru import logger


def gen_aruco_chessboard():
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard_create(7, 5, 1, .8, aruco_dict)
    imboard = board.draw((2000, 2000))
    logger.info("Generating file chessboard.png")
    cv2.imwrite("chessboard.png", imboard)


def process_aruco_chessboard_images(dir_name: Union[Path, str], image_ext:str) -> None:
    logger.info(f"Getting images (with extension {image_ext}) from {dir_name}")
    images = Path(dir_name).glob(f"*.{image_ext}")
    logger.info(list(images))
