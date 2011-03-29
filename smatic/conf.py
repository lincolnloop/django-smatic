from django.conf import settings as django_settings


class Settings(object):
    DEFAULTS = {
        'SASS_BIN': 'sass',
        'SASS_EXTENSIONS': ('.scss', '.sass'),
    }

    def __dir__(self):
        return dir(django_settings)

    def __getattr__(self, attr):
        args = []
        if attr in self.DEFAULTS:
            args.append(self.DEFAULTS[attr]) 
        return getattr(django_settings, attr, *args)


settings = Settings()
