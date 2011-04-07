from smatic.conf import settings


def extra_ignores(command_class):
    for option in command_class.option_list:
        if getattr(option, 'dest', None) != 'ignore_patterns':
            continue
        # Add scss to the default files to exclude.
        option.default = list(settings.SASS_EXTENSIONS)
