Kinome-wide structural pocket similarity
========================================

[![GitHub Actions Build Status](https://github.com/volkamerlab/kissim_app/workflows/CI/badge.svg)](https://github.com/volkamerlab/kissim_app/actions?query=workflow%3ACI)

All-against all comparison of structurally covered kinases using the [`kissim`](https://github.com/volkamerlab/kissim) fingerprint. 

![Kinome-wide all-against-all comparison](docs/_static/kissim_app_toc.png)

## Project Organization

    ├── LICENSE
    ├── README.md          <- The top-level README for this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── devtools           <- Test and user environment; script to generate notebook folder READMEs.
    │   ├── test_env.yaml
    │   ├── user_env.yaml
    │   └── regenerate_readmes.py
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details.
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting.
    │
    ├── results            <- Encodings (fingerprints) and comparisons.
    │
    ├── setup.py           <- Makes project pip installable (pip install -e .) so src can be imported.
    │
    ├── scripts            <- KiSSim scripts.
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module.
    │   ├── data           <- Download or generate data.
    │   ├── evaluation     <- Evaluate data and results.
    │   ├── definitions.py <- Module definitions.
    │   ├── paths.py       <- Module paths to data and results folders.
    │   └── utils.py       <- Module utility functions.
    │
    ├── test               <- Test data, results, and scripts for CI notebook checks.
    |
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


## Contact

If you have questions or suggestions regarding the notebooks in this repository, 
please [open an issue here](https://github.com/volkamerlab/kissim_app/issues).

If you have questions or suggestions regarding the `kissim` package, 
please [open an issue here](https://github.com/volkamerlab/kissim/issues).


We are looking forward to hearing from you!

## License

This work is published under the [MIT license](https://github.com/volkamerlab/kissim/blob/master/LICENSE).

Copyright (c) 2020, Volkamer Lab


## Acknowledgements

### Funding

Volkamer Lab's projects are supported by several public funding sources
(for more info see our [webpage](https://volkamerlab.org/)).

### Collaborators

The `kissim` project is a collaboration between the Volkamer Lab 
(Dominique Sydow, Eva Aßmann and Andrea Volkamer), Albert Kooistra (University of Copenhagen), 
and Friedrich Rippmann (Merck).

### External resources

#### Databases/websites

- [KLIFS](https://klifs.net/)
- [KinMap](http://www.kinhub.org/kinmap/)

#### Python packages

See Python packages listed in the [`kissim` repository README](https://github.com/volkamerlab/kissim#python-packages).

#### Repository

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
