#!/usr/bin/env python3

from datetime import datetime

import guzzle_sphinx_theme

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "guzzle_sphinx_theme",
]

source_suffix = ".rst"
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

project = "Nengo Enhancement Proposals"
copyright = "2017, Applied Brain Research"
author = "Applied Brain Research"
version = release = datetime.now().strftime("%Y-%m-%d")
language = None

todo_include_todos = True

intersphinx_mapping = {}

# HTML theming
pygments_style = "sphinx"
templates_path = ["_templates"]
html_static_path = []
html_use_smartypants = True

html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = "guzzle_sphinx_theme"

html_theme_options = {
    "project_nav_name": "NEPs",
    "base_url": "https://www.nengo.ai/enhancement_proposals",
}

# Other builders
htmlhelp_basename = "NEPs"

latex_elements = {
    # "papersize": "letterpaper",
    # "pointsize": "11pt",
    # "preamble": "",
    # "figure_align": "htbp",
}

latex_documents = [
    (master_doc,  # source start file
     "neps.tex",  # target name
     project,  # title
     "Applied Brain Research",  # author
     "manual"),  # documentclass
]

man_pages = [
    # (source start file, name, description, authors, manual section).
    (master_doc, "neps", project, [author], 1)
]

texinfo_documents = [
    (master_doc,  # source start file
     "NEPs",  # target name
     project,  # title
     author,  # author
     "Nengo",  # dir menu entry
     project,  # description
     "Miscellaneous"),  # category
]
