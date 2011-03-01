import os
from commands import getstatusoutput
from django import template
from django.conf import settings
from django.utils._os import safe_join

register = template.Library()

def scss(file_path):
    """
        Converts an scss file into css and returns the output
    """
    input_path = safe_join(settings.SMATIC_SCSS_ROOT, file_path)
    if not os.path.exists(input_path):
        raise Exception('File does not exist: %s\n' % input_path)

    sass_dict = { 'bin' : settings.SASS_BIN, 'sass_style' : 'compact', 'input' : input_path }
    cmd = "%(bin)s --scss -t %(sass_style)s -C %(input)s" % sass_dict
    (status, output) = getstatusoutput(cmd)
    if not status == 0:
        raise Exception(output)

    return output

register.simple_tag(scss)


def js(file_path):

    input_path = safe_join(settings.SMATIC_JS_ROOT, file_path)
    if not os.path.exists(input_path):
        # TODO: check if enabled on
        raise Exception('File does not exist: %s\n' % input_path)

    return '<script type="text/javascript" src="%sjs/%s"></script>' % (settings.STATIC_URL, file_path)

register.simple_tag(js)