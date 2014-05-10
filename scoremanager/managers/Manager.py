# -*- encoding: utf-8 -*-
import copy
import filecmp
import os
import shutil
import subprocess
from abjad.tools import stringtools
from abjad.tools import systemtools
from scoremanager.core.Controller import Controller


class Manager(Controller):
    r'''Manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_identifier',
        '_main_menu',
        '_path',
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert session is not None
        assert path is not None and os.path.sep in path
        Controller.__init__(self, session=session)
        self._asset_identifier = None
        self._path = path

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of manager.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._path)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._path:
            return os.path.basename(self._path)
        return self._space_delimited_lowercase_class_name

    @property
    def _input_to_action(self):
        superclass = super(Manager, self)
        result = superclass._input_to_action
        result = copy.deepcopy(result)
        result.update({
            'pyd': self.doctest,
            'pyt': self.pytest,
            'rad': self.add_to_repository,
            'rci': self.commit_to_repository,
            'rst': self.repository_status,
            'rrv': self.revert_to_repository,
            'rup': self.update_from_repository,
            'uar': self.remove_unadded_assets,
            })
        return result

    @property
    def _repository_add_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            command = 'git add -A {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            paths = self._get_unadded_asset_paths()
            commands = []
            for path in paths:
                command = 'svn add {}'.format(path)
                commands.append(command)
            command = ' && '.join(commands)
        else:
            raise ValueError(self)
        return command

    @property
    def _repository_status_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            return 'git status {}'.format(self._path)
        elif self._is_svn_versioned(path=self._path):
            return 'svn st {}'.format(self._path)
        else:
            raise ValueError(self)

    @property
    def _repository_update_command(self):
        if not self._path:
            return
        if self._is_in_git_repository(path=self._path):
            root_directory = self._get_repository_root_directory()
            return 'git pull {}'.format(root_directory)
        elif self._is_svn_versioned(path=self._path):
            return 'svn update {}'.format(self._path)
        else:
            raise ValueError(self)

    @property
    def _shell_remove_command(self):
        paths = self._io_manager.find_executable('trash')
        if paths:
            return 'trash'
        return 'rm'

    @property
    def _space_delimited_lowercase_name(self):
        if self._path:
            return os.path.basename(self._path)

    ### PRIVATE METHODS ###

    def _enter_run(self):
        pass

    def _exit_run(self):
        return self._should_backtrack()

    def _find_first_file_name(self):
        for directory_entry in os.listdir(self._path):
            if not directory_entry.startswith('.'):
                path = os.path.join(self._path, directory_entry)
                if os.path.isfile(path):
                    return directory_entry

    def _get_added_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
                if line.startswith('A'):
                    path = line.strip('A')
                    path = path.strip()
                    root_directory = self._get_repository_root_directory()
                    path = os.path.join(root_directory, path)
                    paths.append(path)
        elif self._is_svn_versioned():
            command = 'svn st {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
                if line.startswith('A'):
                    path = line.strip('A')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_current_directory_path(self):
        return self._path

    def _get_modified_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
                if line.startswith(('M', ' M')):
                    path = line.strip('M ')
                    path = path.strip()
                    root_directory = self._get_repository_root_directory()
                    path = os.path.join(root_directory, path)
                    paths.append(path)
        elif self._is_svn_versioned():
            command = 'svn st {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
                if line.startswith('M'):
                    path = line.strip('M')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _get_repository_root_directory(self):
        if self._is_git_versioned():
            command = 'git rev-parse --show-toplevel'
            process = self._io_manager.make_subprocess(command)
            line = process.stdout.readline()
            line = line.strip()
            return line
        elif self._is_svn_versioned():
            pass
        else:
            raise ValueError(self)

    def _get_score_package_directory_name(self):
        line = self._path
        path = self._configuration.example_score_packages_directory_path
        line = line.replace(path, '')
        path = self._configuration.user_score_packages_directory_path
        line = line.replace(path, '')
        line = line.lstrip(os.path.sep)
        return line

    def _get_unadded_asset_paths(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
                if line.startswith('?'):
                    path = line.strip('?')
                    path = path.strip()
                    root_directory = self._get_repository_root_directory()
                    path = os.path.join(root_directory, path)
                    paths.append(path)
        elif self._is_svn_versioned():
            command = 'svn st {}'
            command = command.format(self._path)
            process = self._io_manager.make_subprocess(command)
            paths = []
            for line in process.stdout.readlines():
                if line.startswith('?'):
                    path = line.strip('?')
                    path = path.strip()
                    paths.append(path)
        else:
            raise ValueError(self)
        return paths

    def _initialize_file_name_getter(self):
        getter = self._io_manager.make_getter()
        asset_identifier = getattr(self, '_asset_identifier', None)
        if asset_identifier:
            prompt = 'new {} name'.format(asset_identifier)
        else:
            prompt = 'new name'
        getter.append_dash_case_file_name(prompt)
        return getter

    def _is_git_added(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        first_line = first_line.strip()
        if first_line.startswith('A'):
            return True
        return False

    def _is_git_unknown(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        first_line = first_line.strip()
        if first_line.startswith('??'):
            return True
        return False

    def _is_git_versioned(self, path=None):
        if not self._is_in_git_repository(path=path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        first_line = first_line.strip()
        if first_line == '':
            return True
        elif first_line.startswith('M'):
            return True
        else:
            return False

    def _is_in_git_repository(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        command = 'git status --porcelain {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        if first_line.startswith('fatal:'):
            return False
        else:
            return True

    def _is_populated_directory(self, directory_path):
        if os.path.exists(directory_path):
            if os.listdir(directory_path):
                return True
        return False

    def _is_svn_versioned(self, path=None):
        path = path or self._path
        if path is None:
            return False
        if not os.path.exists(path):
            return False
        is_in_svn_versioned_tree = False
        path_to_check = path
        root_directory = os.path.sep
        while path_to_check:
            if os.path.isdir(path_to_check):
                if '.svn' in os.listdir(path_to_check):
                    is_in_svn_versioned_tree = True
            path_to_check = os.path.dirname(path_to_check)
            if path_to_check == root_directory:
                break
        if not is_in_svn_versioned_tree:
            return False
        command = 'svn st {}'
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        if first_line.startswith('svn: warning:'):
            return False
        else:
            return True

    def _is_up_to_date(self):
        if self._is_git_versioned():
            command = 'git status --porcelain {}'
        elif self._is_svn_versioned():
            command = 'svn st {}'
        else:
            raise ValueError(self)
        command = command.format(self._path)
        process = self._io_manager.make_subprocess(command)
        first_line = process.stdout.readline()
        return first_line == ''

    def _list(self, public_entries_only=False):
        result = []
        if not os.path.exists(self._path):
            return result
        if public_entries_only:
            for directory_entry in sorted(os.listdir(self._path)):
                if directory_entry[0].isalpha():
                    if not directory_entry.endswith('.pyc'):
                        if not directory_entry in ('test',):
                            result.append(directory_entry)
        else:
            for directory_entry in sorted(os.listdir(self._path)):
                if not directory_entry.startswith('.'):
                    if not directory_entry.endswith('.pyc'):
                        result.append(directory_entry)
        return result

    def _list_pretty(self):
        lines = []
        for directory_entry in self._list():
            path = os.path.join(self._path, directory_entry)
            if os.path.isdir(path):
                line = directory_entry + '/'
            elif os.path.isfile(path):
                line = directory_entry
            else:
                raise TypeError(directory_entry)
            lines.append(line)
        lines.append('')
        self._io_manager.display(
            lines,
            capitalize=False,
            )
        self._session._hide_next_redraw = True

    def _list_visible_asset_paths(self):
        return [self._path]

    # TODO: eventually change prompt=False to prompt=True
    def _remove(self, prompt=False):
        if prompt:
            message = '{} will be removed.'
            message = message.format(self._path)
            self._io_manager.display([message, ''])
            getter = self._io_manager.make_getter()
            getter.append_string("type 'remove' to proceed")
            result = getter._run()
            if self._should_backtrack():
                return
            if not result == 'remove':
                return
        cleanup_command = None
        if self._is_in_git_repository():
            if self._is_git_unknown():
                command = 'rm -rf {}'
            else:
                command = 'git rm --force -r {}'
                cleanup_command = 'rm -rf {}'
        elif self._is_svn_versioned():
            command = 'svn --force rm {}'
        else:
            command = 'rm -rf {}'
        path = self._path
        command = command.format(path)
        process = self._io_manager.make_subprocess(command)
        line = process.stdout.readline()
        if cleanup_command:
            cleanup_command = cleanup_command.format(path)
            process = self._io_manager.make_subprocess(cleanup_command)
            line = process.stdout.readline()
        return True

    def _rename(self, new_path):
        if self._is_in_git_repository():
            if self._is_git_unknown():
                command = 'mv {} {}'
            else:
                command = 'git mv --force {} {}'
        elif self._is_svn_versioned():
            command = 'svn --force mv {} {}'
        else:
            command = 'mv {} {}'
        command = command.format(self._path, new_path)
        process = self._io_manager.make_subprocess(command)
        process.stdout.readline()
        self._path = new_path

    def _rename_interactively(
        self, 
        extension=None,
        file_name_callback=None,
        force_lowercase=True,
        ):
        getter = self._io_manager.make_getter()
        string = 'existing asset name'
        getter.append_string(string)
        name = getter._run()
        if self._should_backtrack():
            return
        name = stringtools.strip_diacritics(name)
        if file_name_callback:
            name = file_name_callback(name)
        name = name.replace(' ', '_')
        if force_lowercase:
            name = name.lower()
        if extension and not name.endswith(extension):
            name = name + extension
        parent_directory_path = os.path.dirname(self._path)
        new_path = os.path.join(parent_directory_path, name)
        messages = []
        messages.append('')
        messages.append('Will rename ...')
        messages.append('')
        message = '  FROM: {}'.format(self._path)
        messages.append(message)
        message = '    TO: {}'.format(new_path)
        messages.append(message)
        messages.append('')
        self._io_manager.display(messages)
        result = self._io_manager.confirm()
        if self._should_backtrack():
            return
        if not result:
            return
        if self._rename(new_path):
            message = '{} renamed.'.format(self._asset_identifier)
            self._io_manager.proceed(message)

    def _revert_from_repository(self):
        paths = []
        paths.extend(self._get_added_asset_paths())
        paths.extend(self._get_modified_asset_paths())
        commands = []
        if self._is_git_versioned():
            for path in paths:
                command = 'git reset -- {}'.format(path)
                commands.append(command)
        elif self._is_svn_versioned():
            for path in paths:
                command = 'svn revert {}'.format(path)
                commands.append(command)
        else:
            raise ValueError(self)
        command = ' && '.join(commands)
        self._io_manager.spawn_subprocess(command)
        self._io_manager.display('')

    def _run(self, pending_input=None):
        from scoremanager import iotools
        if pending_input:
            self._session._pending_input = pending_input
        context = iotools.ControllerContext(self)
        directory_change = systemtools.TemporaryDirectoryChange(self._path)
        io_manager = self._io_manager
        with context, directory_change:
                self._enter_run()
                while True:
                    result = io_manager._get_wrangler_navigation_directive()
                    if not result:
                        menu = self._make_main_menu()
                        result = menu._run()
                    if self._exit_run():
                        break
                    elif not result:
                        continue
                    self._handle_main_menu_result(result)
                    if self._exit_run():
                        break

    def _space_delimited_lowercase_name_to_asset_name(
        self, space_delimited_lowercase_name):
        space_delimited_lowercase_name = space_delimited_lowercase_name.lower()
        asset_name = space_delimited_lowercase_name.replace(' ', '_')
        return asset_name

    def _test_add_to_repository(self):
        assert self._is_up_to_date()
        path_1 = os.path.join(self._path, 'tmp_1.py')
        path_2 = os.path.join(self._path, 'tmp_2.py')
        with systemtools.FilesystemState(remove=[path_1, path_2]):
            with file(path_1, 'w') as file_pointer:
                file_pointer.write('')
            with file(path_2, 'w') as file_pointer:
                file_pointer.write('')
            assert os.path.exists(path_1)
            assert os.path.exists(path_2)
            assert not self._is_up_to_date()
            assert self._get_unadded_asset_paths() == [path_1, path_2]
            assert self._get_added_asset_paths() == []
            self.add_to_repository(prompt=False)
            assert self._get_unadded_asset_paths() == []
            assert self._get_added_asset_paths() == [path_1, path_2]
            self.revert_to_repository(prompt=False)
            assert self._get_unadded_asset_paths() == [path_1, path_2]
            assert self._get_added_asset_paths() == []
        assert self._is_up_to_date()
        return True

    def _test_remove_unadded_assets(self):
        assert self._is_up_to_date()
        path_3 = os.path.join(self._path, 'tmp_3.py')
        path_4 = os.path.join(self._path, 'tmp_4.py')
        with systemtools.FilesystemState(remove=[path_3, path_4]):
            with file(path_3, 'w') as file_pointer:
                file_pointer.write('')
            with file(path_4, 'w') as file_pointer:
                file_pointer.write('')
            assert os.path.exists(path_3)
            assert os.path.exists(path_4)
            assert not self._is_up_to_date()
            assert self._get_unadded_asset_paths() == [path_3, path_4]
            self.remove_unadded_assets(prompt=False)
        assert self._is_up_to_date()
        return True

    def _test_revert_to_repository(self):
        assert self._is_up_to_date()
        assert self._get_modified_asset_paths() == []
        file_name = self._find_first_file_name()
        if not file_name:
            return
        file_path = os.path.join(self._path, file_name)
        with systemtools.FilesystemState(keep=[file_path]):
            with file(file_path, 'a') as file_pointer:
                string = '# extra text appended during testing'
                file_pointer.write(string)
            assert not self._is_up_to_date()
            assert self._get_modified_asset_paths() == [file_path]
            self.revert_to_repository(prompt=False)
        assert self._get_modified_asset_paths() == []
        assert self._is_up_to_date()
        return True

    ### PUBLIC METHODS ###

    def add_to_repository(self, prompt=True):
        r'''Adds unversioned assets to repository.

        Returns none.
        '''
        self._session._attempted_to_add_to_repository = True
        if self._session.is_repository_test:
            return
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize=False)
        command = self._repository_add_command
        assert isinstance(command, str)
        self._io_manager.run_command(command)
        self._io_manager.proceed(prompt=prompt)

    def commit_to_repository(self, commit_message=None, prompt=True):
        r'''Commits unversioned assets to repository.

        Returns none.
        '''
        self._session._attempted_to_commit_to_repository = True
        if self._session.is_repository_test:
            return
        if commit_message is None:
            getter = self._io_manager.make_getter()
            getter.append_string('commit message')
            commit_message = getter._run()
            if self._should_backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self._io_manager.display(line)
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
        lines = []
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        lines.append(line)
        command = 'svn commit -m "{}" {}'
        command = command.format(commit_message, self._path)
        self._io_manager.run_command(command, capitalize=False)
        self._io_manager.proceed(prompt=prompt)

    def doctest(self):
        r'''Runs doctest on Python files contained in visible assets.

        Returns none.
        '''
        self._doctest()

    def pytest(self):
        r'''Runs py.test on Python files contained in visible assets.

        Returns none.
        '''
        self._pytest()

    def remove_unadded_assets(self, prompt=True):
        r'''Removes assets not yet added to repository.

        Returns none.
        '''
        self._remove_unadded_assets(prompt=prompt)

    def repository_status(self, prompt=True):
        r'''Displays repository status of assets.

        Returns none.
        '''
        self._session._attempted_repository_status = True
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize=False)
        command = self._repository_status_command
        process = self._io_manager.make_subprocess(command)
        path = self._path
        path = path + os.path.sep
        clean_lines = []
        for line in process.stdout.readlines():
            clean_line = line.strip()
            clean_line = clean_line.replace(path, '')
            clean_lines.append(clean_line)
        clean_lines.append('')
        self._io_manager.display(
            clean_lines,
            capitalize=False,
            )
        self._session._hide_next_redraw = True

    def revert_to_repository(self, prompt=True):
        r'''Reverts assets from repository.

        Returns none.
        '''
        self._session._attempted_to_revert_to_repository = True
        if self._session.is_repository_test:
            return
        message = 'reverting {} ...'
        message = message.format(self._path)
        self._io_manager.display(message)
        self._revert_from_repository()
        self._io_manager.proceed(prompt=prompt)

    def update_from_repository(self, prompt=True):
        r'''Updates versioned assets.

        Returns none.
        '''
        self._session._attempted_to_update_from_repository = True
        if self._session.is_repository_test:
            return
        line = self._get_score_package_directory_name()
        line = line + ' ...'
        self._io_manager.display(line, capitalize=False)
        command = self._repository_update_command
        self._io_manager.run_command(command)
        self._io_manager.proceed(prompt=prompt)