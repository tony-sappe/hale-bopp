# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook
FROM jupyter/scipy-notebook:f9c990eb6295

LABEL maintainer="Tony Sappe"

USER root

# APT packages
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc \
    scilab \
    pari-gp \
    libpari-dev \
    libgmp-dev \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Astrophysics Conda packages

RUN conda config --add channels conda-forge \
  && conda config --set channel_priority flexible

RUN conda update -n base conda
RUN conda update --all
RUN conda install --quiet --yes \
    'astropy' \
    'astroquery' \
    'gammapy' \
    'gwcs' \
    'matplotlib' \
    'photutils' \
    'pyvo' \
    'reproject' \
    'specutils' \
    'vaex'
RUN conda clean --all --yes \
    && fix-permissions $CONDA_DIR

ENV CPATH=$CONDA_DIR/include

RUN pip install \
    pari_jupyter \
    scilab-kernel \
    && fix-permissions $CONDA_DIR

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/


# docker run jupyter-scipy source /opt/conda/bin/activate base && pip freeze