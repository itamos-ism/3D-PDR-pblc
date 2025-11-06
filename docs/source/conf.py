# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '3D-PDR'
copyright = '2025, Thomas G. Bisbas'
author = 'Thomas G. Bisbas'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
            'sphinx.ext.autodoc',  # Automatically generate docs from docstrings
    'sphinx.ext.viewcode', # Add links to highlighted source code
    'sphinx.ext.napoleon', # Support for Google-style docstrings
    # 'myst_parser',       # Uncomment if you're using MyST for Markdown files
        ]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
