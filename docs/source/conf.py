project = "Palo Alto Networks Ansible Collection"
copyright = "2020, Palo Alto Networks"
author = "Palo Alto Networks"

extensions = [
    "sphinx_rtd_theme",
]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
    "github_user": "PaloAltoNetworks",
    "github_repo": "pan-os-ansible",
    "github_version": "master",
    "conf_py_path": "/docs/source/",
}
