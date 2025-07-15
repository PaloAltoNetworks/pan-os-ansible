project = "Palo Alto Networks Ansible Collection"
copyright = "2020, Palo Alto Networks"
author = "Palo Alto Networks"

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_antsibull_ext",
]
exclude_patterns = []

intersphinx_mapping = {
    "ansible": ("https://docs.ansible.com/ansible/latest/", None),
}

html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
    "github_user": "PaloAltoNetworks",
    "github_repo": "pan-os-ansible",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}
