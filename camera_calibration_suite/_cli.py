import click
from enum import Enum
from camera_calibration_suite._aruco_calibration import gen_aruco_chessboard, process_aruco_chessboard_images


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
