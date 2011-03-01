from setuptools import setup, find_packages
from static_installer import get_version

setup(
    name='django-smatic',
    version=get_version(),
    description="Smart tools to handle static files in Django",
    #long_description=open('README.rst').read(),
    author='Marco Louro',
    author_email='marco@lincolnloop.com',
    license='BSD',
    url='http://github.com/lincolnloop/django-smatic/',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
