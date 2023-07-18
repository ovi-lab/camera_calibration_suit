# based on https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html

from typing import Iterator, Tuple, Union
import numpy as np
import cv2
from cv2 import aruco
from pathlib import Path
from loguru import logger
from tqdm import tqdm


def _default_aruco_board():
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard((7, 7), 0.3, 0.18, aruco_dict)
    return aruco_dict, board


def gen_aruco_chessboard():
    _, board = _default_aruco_board()
    imboard = board.generateImage((2000, 2000))
    logger.info("Generating file chessboard.png")
    cv2.imwrite("chessboard.png", imboard)


def process_aruco_chessboard_images(dir_name: Union[Path, str], image_ext:str, display=False) -> Tuple[np.ndarray, np.ndarray]:
    logger.info(f"Getting images (with extension {image_ext}) from {dir_name}")
    images = list(Path(dir_name).glob(f"*.{image_ext}"))
    ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = calibrate_camera(*read_chessboards(images))

    out_file_name = "camera_parameters.npy"
    logger.info(f"Saving parameters to {out_file_name}")
    np.save(out_file_name, np.array((camera_matrix, distortion_coefficients), dtype=object), allow_pickle=True)

    if display:
        logger.info("Displaying test images")
        logger.info(f"Loading paramters from {out_file_name}")
        camera_matrix, distortion_coefficients = np.load(out_file_name, allow_pickle=True)
        display_images = []
        for image_name in tqdm(images):
            image = cv2.imread(str(image_name))
            image_undistorted = cv2.undistort(image, camera_matrix, distortion_coefficients,None)
            images_concatanated = np.concatenate((image, image_undistorted), axis=1)
            display_images.append(images_concatanated)
            cv2.imshow("", images_concatanated)
            cv2.waitKey()

        cv2.imshow("", np.concatenate(display_images[:5], 0))
        cv2.waitKey()

    return camera_matrix, distortion_coefficients
    

def read_chessboards(images: Iterator[Path]):
    """
    Charuco base pose estimation.
    """
    logger.info("Pose Estimation Starts:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
    aruco_dict, board = _default_aruco_board()

    for im in tqdm(images):
        im = str(im)
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = gray.shape
    return allCorners, allIds, imsize


def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    """
    logger.info("Camera Calibration Started")
    _, board = _default_aruco_board()

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    #flags = (cv2.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))
    logger.info("Camera calibration paramters generated")

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors
