# {{cookiecutter.project_name}}
{{cookiecutter.description}}

## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

## Make
Here we will document the different `make` commands defined in the `Makefile`.
All *commands* (excluding the `all` command which is simply executed by
running `make`) are executed by the following format: `make [COMMAND]`. To see
the *contents* of a command that will be executed upon invocation of the
command, simply run `make -n [COMMAND]`.

### Commands
+ `all`: (*aka*: `make`) alias for `jupyter` command
+ `jupyter`: launches the Jupyter notebook development Docker image
+ `pause`: pause PSECS (to pause between commands)
+ `address`: get Docker container address/port
+ `containers`: launch all Docker containers
+ `list-containers`: list all running containers
+ `stop-containers`: simply stops all running Docker containers
+ `restart-containers`: restart all containers
+ `clear-nb`: simply clears Jupyter notebook output
+ `clean`: combines all clearing commands into one

## Docker
This is the same Docker command that is defined in the `Makefile` as the
`jupyter` command. To run it outside of `make`, first `git clone` the repo:
```
git clone {{ cookiecutter.repo_url }}
```
Then `cd {{ cookiecutter.repo_name }}` and run the following:
```
docker run -d \
           --rm \
           --name {{ cookiecutter.container_name }} \
           -e PYTHONPATH=/home/jovyan/src \
           -e JUPYTER_ENABLE_LAB=yes \
           -p 8888 \
           -v $PWD:/home/jovyan \
           {{ cookiecutter.docker_image }} && \
sleep 5 && \
  docker logs {{ cookiecutter.container_name }} 2>&1 | \
    grep "http://127.0.0.1" | tail -n 1 | \
    sed "s/:8888/:$(docker port {{ cookiecutter.container_name }} | \
    grep '0.0.0.0:' | awk '{print $3'} | sed 's/0.0.0.0://g')/g"
```
Click the link (should look similar to:
http://127.0.0.1:RANDOM_PORT/lab?token=LONG_ALPHANUMERIC_STRING) which will
`automatically` log you in and allow you to start running the *notebooks*.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
