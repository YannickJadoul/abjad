import inspect

import pytest

import abjad

ignored_names = (
    "__dict__",
    "__init__",
    "__new__",
    "__weakref__",
    "lilypond_type",
    "denominator",
    "duration",
    "multiplier",
    "music",
    "numerator",
    "optional_id",
    "optional_context_mod",
    "push_signature",
    "type",
    "value",
)

ignored_classes = (
    abjad.parsers.parser.LilyPondParser,
    abjad.parsers.reduced.ReducedLyParser,
    abjad.parsers.scheme.SchemeParser,
    abjad.rhythmtrees.RhythmTreeParser,
    abjad.FormatSpecification,
)

classes = abjad.list_all_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad___doc___01(class_):
    """
    All classes have a docstring. All class methods have a docstring.
    """
    missing_doc_names = []
    if getattr(class_, "_is_dataclass", False) is True:
        return
    if class_.__doc__ is None:
        missing_doc_names.append(class_.__name__)
    for attribute in inspect.classify_class_attrs(class_):
        if attribute.name in ignored_names:
            continue
        elif attribute.defining_class is not class_:
            continue
        if attribute.name[0].isalpha() or attribute.name.startswith("__"):
            if getattr(class_, attribute.name).__doc__ is None:
                missing_doc_names.append(attribute.name)
    if missing_doc_names:
        names = [class_.__name__ + "." + _ for _ in missing_doc_names]
        names = ", ".join(names)
        raise Exception(f"Missing docstrings for: {names}")


functions = abjad.list_all_functions()
if functions:

    @pytest.mark.parametrize("function", functions)
    def test_abjad___doc___02(function):
        """
        All functions have a docstring.
        """
        assert function.__doc__ is not None
