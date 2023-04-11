import datetime
import hashlib
import ipynbname
from IPython.display import clear_output
from IPython import get_ipython
import os
import pathlib
from typing import Any, Callable
from nbconvert.exporters import PDFExporter
import traitlets.config


HOME_BASE = '/home/jovyan'
BUFF_SIZE = 65536


def check_ipython(err_msg: str = 'Not running in a Jupyter notebook.') -> None:
    '''Simply test wether code is in an ipython shell.'''
    # if not in ipython shell alert user
    assert get_ipython() is not None, err_msg


def hash_notebook(nb_path: str) -> str:
    '''Get hash of a Jupyter notebook.'''
    # setup md5 hash function
    sha512 = hashlib.sha512()

    # open notebook at path
    with open(nb_path, 'rb') as notebook:
        # now read chunks of notebook ...
        while True:
            # getting another chunk
            chunk = notebook.read(BUFF_SIZE)

            # no more chunks?
            if not chunk:
                break

            # add new chunk and hash
            sha512.update(chunk)

    # hash completed
    return sha512.hexdigest()


def get_pdf(nb_path: str,
            debug: bool = False,
            output_dir: str = os.path.join(HOME_BASE, 'reports'),
            template_dir: str = os.path.join(HOME_BASE, 'reports/templates'),
            template_name: str = 'cited_report') -> None:
    '''Generate a PDF report from Jupyter notebook.'''
    # setup report dir if not exist
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Setup config
    config = traitlets.config.Config()

    # set exporter setting to remove code execution counters
    exporter_settings = {
        'exclude_input_prompt': True,
        'exclude_output_prompt': True,
    }
    config.PDFExporter.update(exporter_settings)

    # Configure tag removal - be sure to tag your cells to remove using the
    # words remove_cell to remove cells. You can also modify the code to use
    # a different tag word
    config.TagRemovePreprocessor.remove_cell_tags = ('remove_cell',)
    config.TagRemovePreprocessor.remove_input_tags = ('remove_input',)
    config.TagRemovePreprocessor.enabled = True
    config.TemplateExporter.template_name = template_name
    config.TemplateExporter.extra_template_basedirs = [template_dir]

    # toggle verbose on debug mode
    if debug:
        config.PDFExporter.verbose = True

    # Configure and run out exporter
    config.PDFExporter.preprocessors = ['nbconvert.preprocessors.TagRemovePreprocessor']

    # get exporter
    exporter = PDFExporter(config=config)

    # Configure and run our exporter - returns a tuple - first element with pdf,
    # second with notebook metadata
    pdf_data, metadata = exporter.from_filename(nb_path)

    # get date time for doc
    dt_stamp = datetime.datetime.now().strftime('%y%m%d%H%M%S')

    # extract file name from file path
    nb_name = os.path.basename(nb_path)

    # create report name for PDF
    pdf_name = f'{nb_name}.{dt_stamp}.pdf'

    # create full path for PDF report
    pdf_full_path = os.path.join(output_dir, pdf_name)

    # Write to output PDF file path
    with open(pdf_full_path,  "wb") as f:
        f.write(pdf_data)


def auto_convert(nb_globals: dict,
                 auto: bool = True,
                 force: bool = False,
                 converter: Callable[..., None] = get_pdf,
                 **kwargs: Any) -> None:
    '''Keep track of notebook updates and convert on change.'''
    # see if in jupyter nb
    check_ipython('Designed to be executed in Jupyter notebook only. Please use manual conversion methods.')

    # set nb_path using ipynbname
    nb_path = ipynbname.path().as_posix()

    # check to see if hash in globals
    if 'NB_HASH' in nb_globals and (auto or force):
        # get current hash
        fresh_nb_hash = hash_notebook(nb_path)

        # compare to old
        if fresh_nb_hash != nb_globals['NB_HASH'] or force:
            # notify user of notebook being converted
            print(f'Notebook path to be converted: {nb_path}')

            # time to convert
            converter(nb_path, **kwargs)

            # then clear
            if not kwargs.get('debug', False):
                clear_output()

    # calculate hash
    nb_hash = hash_notebook(nb_path)

    # update globals
    nb_globals['NB_HASH'] = nb_hash
