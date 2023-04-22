import IPython.display
import pathlib
import os
import requests
from typing import Any

IMAGE_DWNLD_BASEDIR = '/home/jovyan/data'


def load(url: str, imgdir: str, fname: str, **kwargs: Any) -> IPython.display.Image:
    '''If fname image not found locally then download from URL give.'''
    # create full path
    full_image_path = os.path.join(IMAGE_DWNLD_BASEDIR, imgdir, fname)

    # check if image doesnt exist
    if not os.path.exists(full_image_path):
        # create data dir if it does not exist
        pathlib.Path(os.path.join(IMAGE_DWNLD_BASEDIR, imgdir)).mkdir(parents=True, exist_ok=True)

        # get image
        response = requests.get(url)

        # check status code
        assert response.status_code == 200, f'URL failed to resolve with status code: {response.status_code}'

        # now write image to file
        with open(full_image_path, 'wb') as imgfile:
            imgfile.write(response.content)

    # finally open the image
    return IPython.display.Image(full_image_path, **kwargs)
