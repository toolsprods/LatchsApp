# -*- coding: utf-8 -*-

import os
import sys
import pygubu

try:
    DATA_DIR = os.path.abspath(os.path.dirname(__file__))
except NameError:
    DATA_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


class View:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(os.path.join(DATA_DIR, 'main.ui'))
        builder.add_resource_path(os.path.join(DATA_DIR, 'img'))

        self.mainwindow = builder.get_object('mainwindow', master)
