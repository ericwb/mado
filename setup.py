# Copyright © 2020 Eric Brown
#
# SPDX-License-Identifier: GPL-3.0-or-later
import os
import setuptools


APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': os.path.join('icons', 'mado.icns'),
}

setuptools.setup(
    name='Mado',
    version='1.0.0',
    app=APP,
    author='Eric Brown',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
    setup_requires=[
        'py2app',
        'Pillow'
    ],
)
