# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


long_description = ('\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read()
]))


setup(
    name='collective.utils',
    version='0.1',
    description="Generic utils for everyday Plone development",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Plone',
    author='Johannes Raggam',
    author_email='dev@programmatic.pro',
    url='http://pypi.python.org/pypi/collective.utils',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'z3c.jbot',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
