# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) 2021
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

# ---------------
# Airflow imports
# ---------------

#--------------
# local imports
# -------------

from ._version import get_versions


# -----------------------
# Module global variables
# -----------------------

# ----------------
# Module constants
# ----------------


__version__ = get_versions()['version']

del get_versions
