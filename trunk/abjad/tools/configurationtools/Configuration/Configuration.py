import abc
import collections
import configobj
import validate
import os
import time
from abjad.tools import abctools


class Configuration(collections.MutableMapping, abctools.AbjadObject):
    '''Abjad configuration object.
    '''

    ### CLASS ATTRIBUTES ###

    ### INITIALIZER ###

    def __init__(self):

        # verify configuration directory
        if not os.path.exists(self.CONFIG_DIRECTORY_PATH):
            os.makedirs(self.CONFIG_DIRECTORY_PATH)

        # attempt to load config from disk, and validate
        # a config object will be created if none is found on disk
        config = configobj.ConfigObj(
            self.CONFIG_FILE_PATH,
            configspec=self._config_specification
            )

        # validate
        validator = validate.Validator()
        validation = config.validate(validator, copy=True)

        # replace failing key:value pairs with default values
        if validation is not True:
            for key, valid in validation.iteritems():
                if not valid:
                    default = config.default_values[key]
                    print 'Warning: config key {!r} failed validation, '\
                        'setting to default: {!r}.'.format(key, default)
                    config[key] = default

        # setup output formatting
        config.write_empty_values = True
        config.comments.update(self._option_comments)
        config.initial_comment = self._initial_comment

        # write back to disk
        with open(self.CONFIG_FILE_PATH, 'w') as f:
            config.write(f)

        # turn the ConfigObj instance into a standard dict,
        # and replace its empty string values with Nones,
        # caching the result on this AbjadConfiguration instance.
        self._settings = dict(config)
        for key, value in self._settings.iteritems():
            if value == '' or value == 'None':
                self._settings[key] = None

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        del(self._settings[i])

    def __getitem__(self, i):
        return self._settings[i]

    def __iter__(self):
        for key in self._settings:
            yield key

    def __len__(self):
        return len(self._settings)

    def __setitem__(self, i, arg):
        self._settings[i] = arg

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def CONFIG_DIRECTORY_PATH(self):
        raise NotImplemented

    @abc.abstractproperty
    def CONFIG_FILE_NAME(self):
        raise NotImplemented

    @property
    def CONFIG_FILE_PATH(self):
        return os.path.join(self.CONFIG_DIRECTORY_PATH, self.CONFIG_FILE_NAME)

    @property
    def HOME_DIRECTORY_PATH(self):
        return os.environ.get('HOME') or \
            os.environ.get('HOMEPATH') or \
            os.environ.get('APPDATA')

    ### PRIVATE PROPERTIES ###

    @property
    def _config_specification(self):
        specs = self._option_specification
        return ['{} = {}'.format(key, value) for key, value in sorted(specs.items())]

    @property
    def _current_time(self):
        return time.strftime("%d %B %Y %H:%M:%S")

    @abc.abstractproperty
    def _initial_comment(self):
        raise NotImplemented

    @property
    def _option_comments(self):
        options = self._option_definitions
        comments = [(key, options[key]['comment']) for key in options]
        return dict(comments)

    @abc.abstractproperty
    def _option_definitions(self):
        raise NotImplemented

    @property
    def _option_specification(self):
        options = self._option_definitions
        specs = [(key, options[key]['spec']) for key in options]
        return dict(specs)
