import click
from enum import Enum
from camera_calibration_suite._aruco_calibration import gen_aruco_chessboard, process_aruco_chessboard_images
import camera_calibration_suite._generic_capture as generic_capture


class Methods(Enum):
    aruco = 'aruco'
    plain = 'plain'


@click.group()
def cli():
    pass


@cli.command()
@click.option("-m", "--method", type=click.Choice(Methods.__members__), callback=lambda c, p, v: getattr(Methods, v) if v else None, default='aruco')
def generate_chessboard(method):
    if method == Methods.aruco:
        gen_aruco_chessboard()
    else:
        raise NotImplemented


@cli.command()
@click.argument("dir_name", type=click.Path())
@click.argument("image_ext", type=str)
@click.option("-m", "--method", type=click.Choice(Methods.__members__), callback=lambda c, p, v: getattr(Methods, v) if v else None, default='aruco')
@click.option("-d", "--display", is_flag=True)
def process_chessboard_images(dir_name, image_ext, method, display):
    """Processes the chessboard images (with extention `image_ext`) in the directory `dir_name` """
    if method == Methods.aruco:
        process_aruco_chessboard_images(dir_name, image_ext, display=display)
    else:
        raise NotImplemented


@cli.command()
@click.argument("dir_name", type=click.Path())
@click.option("-e", "--image-ext", type=str, help="Image extension to use", default="jpg")
@click.option("-c", "--camera-or-file", type=str, help="camera index or file name to pass to opencv", default="0")
def capture_images(dir_name, image_ext, camera_or_file):
    """Use opencv to capture images for calibration."""
    if camera_or_file.isdigit():
        camera_or_file = int(camera_or_file)
    generic_capture.capture_images(camera_or_file, dir_name, image_ext)

