# -*- encoding: utf -*-
import os
import re
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Controller(ScoreManagerObject):
    r'''Controller.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INTIIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        superclass = super(Controller, self)
        superclass.__init__(session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _abjad_import_statement(self):
        return 'from abjad import *'

    @property
    def _unicode_directive(self):
        return '# -*- encoding: utf-8 -*-'

    @property
    def _user_input_to_action(self):
        result = {
            }
        return result

    ### PRIVATE METHODS ###

    def _filter_asset_menu_entries_by_view(self, entries, view):
        entries = entries[:]
        filtered_entries = []
        for item in view:
            try:
                pattern = re.compile(item)
            except:
                pattern = None
                message = 'invalid regular expression: {!r}.'
                message  = message.format(item)
                self._io_manager.proceed(message)
            for entry in entries:
                display_string, _, _, path = entry
                file_name = display_string.split()[0]
                if item == file_name:
                    filtered_entries.append(entry)
                elif pattern and pattern.match(file_name):
                    filtered_entries.append(entry)
        return filtered_entries

    @staticmethod
    def _is_directory_with_metadata_module(path):
        if os.path.isdir(path):
            for directory_entry in os.listdir(path):
                if directory_entry == '__metadata__.py':
                    return True
        return False

    @staticmethod
    def _is_package_path(path):
        if os.path.isdir(path):
            for directory_entry in os.listdir(path):
                if directory_entry == '__init__.py':
                    return True
        return False

    def _list_directories_with_metadata_modules(self, path=None):
        path = path or self._path
        paths = []
        for directory_path, subdirectory_names, file_names in os.walk(path):
            if self._is_directory_with_metadata_module(directory_path):
                if directory_path not in paths:
                    paths.append(directory_path)
            for subdirectory_name in subdirectory_names:
                path = os.path.join(directory_path, subdirectory_name)
                if self._is_directory_with_metadata_module(path):
                    if path not in paths:
                        paths.append(path)
        return paths

    def _make_asset_menu_entries(
        self,
        apply_view=True,
        include_annotation=True,
        include_extensions=False,
        include_asset_name=True,
        include_year=False,
        human_readable=True,
        packages_instead_of_paths=False,
        sort_by_annotation=False,
        ):
        paths = self._list_visible_asset_paths()
        strings = []
        for path in paths:
            if human_readable:
                string = self._path_to_human_readable_name(
                    path,
                    include_extension=include_extensions,
                    )
            else:
                string = os.path.basename(path)
            if include_annotation:
                annotation = self._path_to_annotation(path, year=include_year)
                if include_asset_name:
                    string = '{} ({})'.format(string, annotation)
                else:
                    string = str(annotation)
            strings.append(string)
        pairs = zip(strings, paths)
        if sort_by_annotation:
            tmp = stringtools.strip_diacritics
            pairs.sort(key=lambda x: tmp(x[0]))
        entries = []
        for string, path in pairs:
            if packages_instead_of_paths:
                path = self._configuration.path_to_package_path(path)
            entry = (string, None, None, path)
            entries.append(entry)
        if self._session.is_test:
            return entries
        if not apply_view:
            return entries
        view = self._read_view()
        if view is not None:
            entries = self._filter_asset_menu_entries_by_view(entries, view)
        return entries

    def _make_directory_menu_section(self, menu, is_permanent=False):
        commands = []
        commands.append(('directory - list', 'ls'))
        commands.append(('directory - list long', 'll'))
        if not is_permanent:
            commands.append(('directory - remove', 'rm'))
            commands.append(('directory - rename', 'ren'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='directory',
            )

    def _make_done_menu_section(self, menu):
        commands = []
        commands.append(('done', 'done'))
        menu.make_navigation_section(
            commands=commands,
            name='zzz - done',
            )

    def _make_initializer_menu_section(self, menu):
        commands = []
        if (self._initializer_file_path and
            os.path.isfile(self._initializer_file_path)):
            commands.append(('initializer - remove', 'inrm'))
            commands.append(('initializer - read only', 'inro'))
        else:
            commands.append(('initializer - stub', 'ins'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='initializer',
            )

    def _make_metadata_menu_section(self, menu):
        commands = []
        commands.append(('metadatum - add', 'mda'))
        commands.append(('metadatum - get', 'mdg'))
        commands.append(('metadatum - remove', 'mdrm'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='metadatum',
            )

    def _make_metadata_module_menu_section(self, menu):
        commands = []
        commands.append(('metadata module - remove', 'mdmrm'))
        commands.append(('metadata module - rewrite', 'mdmrw'))
        commands.append(('metadata module - read only', 'mdmro'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='metadata module',
            )

    def _make_sibling_asset_tour_menu_section(self, menu):
        section = menu['go - scores']
        menu.menu_sections.remove(section)
        commands = []
        commands.append(('go - next score', '>>'))
        commands.append(('go - previous score', '<<'))
        commands.append(('go - next score', '>>'))
        commands.append(('go - next asset', '>'))
        commands.append(('go - previous score', '<<'))
        commands.append(('go - previous asset', '<'))
        menu.make_command_section(
            is_alphabetized=False,
            is_hidden=True,
            commands=commands,
            name='go - scores',
            )

    def _make_views_menu_section(self, menu):
        commands = []
        commands.append(('views - apply', 'va'))
        commands.append(('views - list', 'vls'))
        commands.append(('views - new', 'vnew'))
        commands.append(('views - remove', 'vrm'))
        commands.append(('views - rename', 'vren'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views',
            )

    def _make_views_module_menu_section(self, menu):
        commands = []
        commands.append(('views module - remove', 'vmrm'))
        commands.append(('views module - read only', 'vmro'))
        menu.make_command_section(
            is_hidden=True,
            commands=commands,
            name='views module',
            )

    def _path_to_annotation(self, path, year=False):
        from scoremanager import managers
        score_storehouses = (
            self._configuration.example_score_packages_directory_path,
            self._configuration.user_score_packages_directory_path,
            )
        if path.startswith(score_storehouses):
            score_path = self._configuration._path_to_score_path(path)
            manager = managers.ScorePackageManager(
                path=score_path,
                session=self._session,
                )
            metadata = manager._get_metadata()
            if metadata:
                year_of_completion = metadata.get('year_of_completion')
                title = metadata.get('title')
                if year and year_of_completion:
                    annotation = '{} ({})'.format(title, year_of_completion)
                else:
                    annotation = str(title)
            else:
                package_name = os.path.basename(path)
                annotation = 'Untitled ({})'
                annotation = annotation.format(package_name)
        elif path.startswith(self._abjad_storehouse_path):
            annotation = 'Abjad'
        elif path.startswith(self._user_storehouse_path):
            annotation = self._configuration.composer_last_name
        else:
            annotation = None
        return annotation

    @staticmethod
    def _path_to_human_readable_name(path, include_extension=False):
        path = os.path.normpath(path)
        name = os.path.basename(path)
        if not include_extension:
            name, extension = os.path.splitext(name)
        return stringtools.to_space_delimited_lowercase(name)

    @staticmethod
    def _sort_ordered_dictionary(dictionary):
        new_dictionary = type(dictionary)()
        for key in sorted(dictionary):
            new_dictionary[key] = dictionary[key]
        return new_dictionary