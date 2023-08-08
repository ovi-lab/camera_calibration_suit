from pathlib import Path
from typing import Union
from loguru import logger
import cv2


def capture_images(camera_or_file: Union[int, Path, str], dir_name: Union[Path , str], ext_name: str="jpg", wait_time_ms:int=30, display_height:int=720) -> None:
    "From the video stream in camera_index, capture images and store them."
    cap = cv2.VideoCapture(camera_or_file)
    if (cap.isOpened() == False):
        logger.error("Failed cap.isOpened()")
        return

    image_index = 0
    directory = Path(dir_name)
    file_name = "image_{}." + ext_name

    logger.info(f"Capturing video from {camera_or_file}.")
    logger.info(f"Directory to store - {directory}   with extension {ext_name}")

    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=False)
        logger.info(f"Created directory {directory}")
    else:
        logger.warning(f"Directory {directory} already exists.")

    logger.info("Press <RET> to save image, `q` to exit, `b` to rewid 5 frames back, `p` to play/pause.")

    _current_wait_time = wait_time_ms
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed cap.read()")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        h, w = frame.shape[:2]
        if h < display_height:
            factor = 1
        else:
            factor = h/display_height
        cv2.imshow('frame', cv2.resize(frame, (round(w/factor), round(h/factor))))

        key = cv2.waitKey(_current_wait_time)
        if key == ord('q'):
            logger.info("Exiting")
            break
        elif key == ord("p"):
            if _current_wait_time == 0:
                if wait_time_ms == 0:
                    logger.warning("Play/pause won't work as wait-time-ms passed is 0")
                _current_wait_time = wait_time_ms
            else:
                _current_wait_time = 0
        elif key == ord('b'):
            current_frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_number - 10)
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
