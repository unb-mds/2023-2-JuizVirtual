"""
MIT License

Copyright (c) 2023 MDS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from dataclasses import asdict
from typing import List

from sphinxawesome_theme import ThemeOptions
from sphinxawesome_theme.postprocess import Icons

#########################
#  Project information  #
#########################

project = "MDS Squad 06"
author = "Squad 06"
copyright = f"2023-present, {author}."

###########################
#  General configuration  #
###########################

extensions: List[str] = []

templates_path = ["_templates"]
exclude_patterns: List[str] = []

language = "pt"

##################
#  HTML Options  #
##################

html_title = author
html_theme = "sphinxawesome_theme"
html_copy_source = False
html_permalinks_icon = Icons.permalinks_icon

html_static_path = ["_static"]

theme_options = ThemeOptions(
    show_prev_next=True,
    extra_header_link_icons={
        "Repository on GitHub": {
            "link": "https://github.com/unb-mds/2023-2-Squad06",
            "icon": (
                '<svg height="22px" style="margin-top:-1px;display:inline" '
                'viewBox="0 0 45 44" '
                'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
                '<path fill-rule="evenodd" clip-rule="evenodd" '
                'd="M22.477.927C10.485.927.76 10.65.76 22.647c0 9.596 6.223 '
                "17.736 14.853 20.608 1.087.2 1.483-.47 1.483-1.047 "
                "0-.516-.019-1.881-.03-3.693-6.04 1.312-7.315-2.912-7.315-"
                "2.912-.988-2.51-2.412-3.178-2.412-3.178-1.972-1.346.149-1.32."
                "149-1.32 2.18.154 3.327 2.24 3.327 2.24 1.937 3.318 5.084 "
                "2.36 6.321 1.803.197-1.403.759-2.36 1.379-2.903-4.823-.548-9."
                "894-2.412-9.894-10.734 0-2.37.847-4.31 2.236-5.828-.224-.55-."
                "969-2.759.214-5.748 0 0 1.822-.584 5.972 2.226 1.732-.482 "
                "3.59-.722 5.437-.732 1.845.01 3.703.25 5.437.732 4.147-2.81 "
                "5.967-2.226 5.967-2.226 1.185 2.99.44 5.198.217 5.748 1.392 "
                "1.517 2.232 3.457 2.232 5.828 0 8.344-5.078 10.18-9.916 "
                "10.717.779.67 1.474 1.996 1.474 4.021 0 2.904-.027 5.247-."
                "027 5.96 0 .58.392 1.256 1.493 1.044C37.981 40.375 44.2 "
                '32.24 44.2 22.647c0-11.996-9.726-21.72-21.722-21.72" '
                'fill="currentColor"/></svg>'
            ),
        },
    },
)

html_theme_options = asdict(theme_options)
