from pathlib import Path
from typing import Union
from loguru import logger
import cv2


def capture_images(camera_or_file: Union[int, Path, str], dir_name: Union[Path , str], ext_name: str="jpg", wait_time_ms:int=30) -> None:
    "From the video stream in camera_index, capture images and store them."
    cap = cv2.VideoCapture(camera_or_file)
    image_index = 0
    directory = Path(dir_name)
    file_name = "calibration_chessboard_{}." + ext_name

    logger.info(f"Capturing video from {camera_or_file}.")
    logger.info(f"Directory to store - {directory}   with extension {ext_name}")

    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=False)
        logger.info(f"Created directory {directory}")

    logger.info("Press <RET> to save image, `q` to exit.")

    while True:
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(wait_time_ms)
        if key == ord('q'):
            logger.info("Exiting")
            break
        elif key == 13:  # enter
            out_file_name = directory / file_name.format(image_index)
            if out_file_name.exists():
                logger.error(f"File {out_file_name} already exists")
                break
            cv2.imwrite(str(out_file_name), frame)
            logger.info(f"Writing image {out_file_name}")
            image_index += 1

    cap.release()
    cv2.destroyAllWindows()
