import IPython.display
import os
import pathlib
import requests
from tqdm.notebook import tqdm_notebook
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
        response = requests.get(
            url,
            headers={'User-Agent': f'requests/{requests.__version__}'},
            stream=True
        )

        # check status code
        assert response.status_code == 200, f'URL failed to resolve with status code: {response.content}'

        # now write image to file
        with open(full_image_path, 'wb') as imgfile, tqdm_notebook(
            desc=fname,
            total=int(response.headers.get('content-length', 0)),
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                bar.update(imgfile.write(data))

        # clear progress bar output
        IPython.display.clear_output()

    # finally open the image
    return IPython.display.Image(full_image_path, **kwargs)
