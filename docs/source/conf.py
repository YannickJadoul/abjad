import sphinx_rtd_theme

import abjad

### GENERAL SPHINX SETTINGS ###
### https://www.sphinx-doc.org/en/master/usage/configuration.html ###

copyright = "2008-2022, Trevor Bača & Josiah Wolf Oberholtzer."
extensions = [
    "abjad.ext.sphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # temporarily comment out sphinx.ext.viewcode when heavily editing docs;
    # prevents "highlighting module code ..." pass on every doc build;
    # uncomment sphinx.ext.viewcode when building official release:
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]
html_favicon = "_static/favicon.ico"
html_logo = "_static/abjad-logo.png"
html_show_copyright = False
html_show_sourcelink = False
html_show_sphinx = False
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "canonical_url": "https://abjad.github.io",
    "display_version": False,
    # most important setting:
    # navigation_depth=1 makes sidebar completely flat;
    # leave flat navigation in place forever:
    "navigation_depth": 1,
    "style_nav_header_background": "#880088",
}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
project = "Abjad"
release = abjad.__version__
rst_epilog = """
..  _Bača: https://github.com/trevorbaca
..  _Fredrik Wallberg: http://quesebifurcan.github.io/music
..  _Jeffrey Treviño: https://soundcloud.com/jefftrevino
..  _Josiah Wolf Oberholtzer: http://josiahwolfoberholtzer.com
..  _Gregory Rowland Evans: http://www.gregoryrowlandevans.com
..  _Oberholtzer: https://github.com/josiah-wolf-oberholtzer
..  _Trevor Bača: http://www.trevorbaca.com
"""
rst_prolog = """
..  role:: author
"""
smartquotes = True
templates_path = ["_templates"]
version = abjad.__version__

### UQBAR ###

uqbar_api_title = "Abjad API"
uqbar_api_source_paths = ["abjad"]
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]

uqbar_book_console_setup = ["import abjad", "from fractions import Fraction"]
uqbar_book_console_teardown = []
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "abjad.ext.sphinx.LilyPondExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True

try:
    import abjadext  # noqa

    uqbar_api_source_paths.append("abjadext")
    uqbar_book_console_setup.append("import abjadext")
except ImportError:
    pass

try:
    from abjadext import rmakers  # noqa

    uqbar_book_console_setup.append("from abjadext import rmakers")
except ImportError:
    pass

try:
    from abjadext import microtones  # noqa

    uqbar_book_console_setup.append("from abjadext import microtones")
except ImportError:
    pass

try:
    from abjadext import nauert  # noqa

    uqbar_book_console_setup.append("from abjadext import nauert")
except ImportError:
    pass

### OTHER EXTENSIONS ###

autodoc_member_order = "groupwise"
graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"
intersphinx_mapping = {
    "http://josiahwolfoberholtzer.com/uqbar/": None,
    "http://www.sphinx-doc.org/en/master/": None,
    "https://docs.python.org/3.10/": None,
}
todo_include_todos = True
