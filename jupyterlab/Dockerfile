# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook

# JupyterLab 3.0.16
# Python 3.7.10
FROM jupyter/scipy-notebook:f9c990eb6295

USER root

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    fonts-dejavu \
    gcc \
    gfortran \
    libgmp-dev \
    libpari-dev \
    pari-gp \
    scilab \
    tzdata \
    wget \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Science Platform Conda packages

RUN conda config --add channels conda-forge \
  && conda config --set channel_priority strict

RUN conda update -n base conda
RUN conda update --all
RUN conda install --quiet --yes \
    'astropy' \
    'astroquery' \
    'awscli' \
    'boto3' \
    'gammapy' \
    'gatspy' \
    'gwcs' \
    'jupyterhub==1.4.2' \
    'nodejs' \
    'photutils' \
    'psycopg2' \
    'pyspark' \
    'pyvo' \
    'reproject' \
    'specutils' \
    'vaex'
RUN conda clean --all --yes \
    && fix-permissions $CONDA_DIR

ENV CPATH=$CONDA_DIR/include \
    JAVA_HOME=/usr/bin/java

RUN pip install \
    pari_jupyter \
    jupyterlab-sql \
    scilab-kernel \
    && fix-permissions $CONDA_DIR

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/
