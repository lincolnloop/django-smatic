import os
import shlex
import pipes
from subprocess import PIPE, Popen

from django.contrib.staticfiles.finders import get_finders, BaseFinder
from django.core.files.storage import default_storage, FileSystemStorage

from smatic.conf import settings


class SassFinder(BaseFinder):

    def __init__(self, *args, **kwargs):
        super(SassFinder, self).__init__(*args, **kwargs)
        self.storage = FileSystemStorage(location=settings.SASS_ROOT,
                                         base_url=settings.STATIC_URL)

    @staticmethod
    def convert(absolute_file_path, output_filename):
        """
        Does the actual conversion. Takes one argument, the absolute path to
        the SCSS/SASS files.
        """
        absolute_output_filename = os.path.join(settings.SASS_ROOT,
                                                output_filename)

        # Check for the mtime to avoid constantly writing the file.
        if os.path.isfile(absolute_output_filename):
            if (os.path.getmtime(absolute_output_filename) >
                    os.path.getmtime(absolute_file_path)):
                return absolute_output_filename

        output_dir = os.path.dirname(absolute_output_filename)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        cmd = '%(bin)s -t %(sass_style)s -C %(input)s %(output)s' % {
            'bin': settings.SASS_BIN,
            'sass_style': 'compact',
            'input': pipes.quote(absolute_file_path),
            'output': pipes.quote(absolute_output_filename),
        }

        process = Popen(shlex.split(str(cmd)), stderr=PIPE)
        stderr = process.communicate()

        if not process.returncode == 0:
            # TODO: put the error into the css file when DEBUG is True perhaps?
#            if settings.DEBUG:
#                raise TemplateSyntaxError('Scss file conversion failed. '
#                                          'Reason: %s' % stderr.read())
            return False

        return absolute_output_filename
    
    def get_finders(self):
        finder_class = type(self)
        for finder in get_finders():
            if not isinstance(finder, finder_class):
                yield finder

    def list(self, ignore_patterns):
        """
        Iterate the list methods of all other finders, generating (and
        returning) CSS files when an SCSS file is found.
        """
        for finder in self.get_finders():
            for path, storage in finder.list([]):
                name, ext = os.path.splitext(path)
                if ext not in settings.SASS_EXTENSIONS:
                    continue
                output_name = '%s.css' % name
                if getattr(storage, 'prefix', None):
                    output_name = os.path.join(storage.prefix, output_name)
                if self.convert(storage.path(path), output_name):
                    yield output_name, self.storage

    def find(self, path, all=False):
        """
        Finds SCSS files for paths ending in '.css', generating the CSS file
        on the fly.
        """
        name, ext = os.path.splitext(path)
        if ext != '.css':
            return []
        for finder in self.get_finders():
            for ext in settings.SASS_EXTENSIONS:
                match = finder.find('%s%s' % (name, ext))
                if match:
                    break
            if not match:
                continue
            converted = self.convert(match, path)
            if converted:
                if all:
                    return [converted]
                return converted
            # Found a match, exit the loop.
            break
        return []
