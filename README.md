This project contains a suite of camera calibration proecdures for opencv-python

Current implementation contains:
- Single camera calibration using aruco marker configuration.


## Installation
```sh
pip install git+https://github.com/hcilab-uofm/camera_calibration_suit
```


## Usage

### Single camera calibration
1. Generate the marker configuration image:
   ```sh 
   run-calibration generate-chessboard
   ```

2. Capture a set of images from the camera of the chessboard pattern geneated and place them in a directory. You can use the following for that

    ```sh
    run-calibration capture-images captured_chessboard_images
    ```

    Where `captured_chessboard_images` is a directory.

3. Run the `process-chessboard-images` command:
   ```
   run-calibration process-chessboard-images captured_chessboard_images JPG
   ```

   This saves the parameters in a file named `camera_parameters.npy`
   Assuming the direcotry containing the images is named `captured_chessboard_images`, and the image extension is `JPG`.
   Use `-d` to display the images used to generated the parameters.

4. Use the generated parameters to undistort an image from the camera:

  >>> import cv2
  >>> import numpy as np
  >>> image = cv2.imread("test.jpg")
  >>> camera_matrix, distortion_coefficients = np.load("camera_parameters.npy", allow_pickle=True)
  >>> cv2.undistort(image, camera_matrix, distortion_coefficients, None)


### Capture images

To capture images you can use the following command:

```sh
poetry run run-calibration capture-images image-dir
```

Where images will be stored in `image-dir`. Also has the following options:
- `-e`, (`--image-ext`): Image extension to use (defult `jpg`).
- `-c` (`--camera-or-file`): camera index or file name to pass to opencv. Defaults to `0`, which is the 0 index camera.
- `-t`, (`--wait-time-ms`): Wait time for each frame in milliseconds (default 30).
- `-h`, (`--display-height`): Display height (default 720).
- `--help`

This can be used as a common tool as well.
