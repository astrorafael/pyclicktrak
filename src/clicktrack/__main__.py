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

import sys
import argparse
import os.path
import logging
#import logging.handlers
import traceback
import importlib
import time

# -------------
# Local imports
# -------------

from . import  __version__


# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("click")

# -----------------------
# Module global functions
# -----------------------

def configureLogging(options):
	if options.verbose:
		level = logging.DEBUG
	elif options.quiet:
		level = logging.WARN
	else:
		level = logging.INFO
	
	log.setLevel(level)
	# Log formatter
	#fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
	fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
	# create console handler and set level to debug
	if not options.no_console:
		ch = logging.StreamHandler()
		ch.setFormatter(fmt)
		ch.setLevel(level)
		log.addHandler(ch)
	# Create a file handler
	if options.log_file:
		#fh = logging.handlers.WatchedFileHandler(options.log_file)
		fh = logging.FileHandler(options.log_file)
		fh.setFormatter(fmt)
		fh.setLevel(level)
		log.addHandler(fh)


def python2_warning():
	if sys.version_info[0] < 3:
		log.warning("This software des not run under Python 2 !")


def setup(options):
	python2_warning()
	

def mktime(string):
    return datetime.time.fromisoformat(string)

def mktime(string):
    try:
        struct_tm = time.strptime(string, '%M')
    except ValueError:
        struct_tm = time.strptime(string, '%M:%S')
    return struct_tm

# =================== #
# THE ARGUMENT PARSER #
# =================== #

def createParser():
	# create the top-level parser
	name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
	parser    = argparse.ArgumentParser(prog=name, description="pyclicktrack")

	# Global options
	parser.add_argument('--version', action='version', version='{0} {1}'.format(name, __version__))
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
	group.add_argument('-q', '--quiet',   action='store_true', help='Quiet output.')
	parser.add_argument('-nk','--no-console', action='store_true', help='Do not log to console.')
	parser.add_argument('--log-file', type=str, default=None, help='Optional log file')

	
	# --------------------------
	# Create first level parsers
	# --------------------------
	subparser = parser.add_subparsers(dest='command')
	parser_generate    = subparser.add_parser('generate', help='Generate commands')
	
	# ----------------
	# Entries Commands
	# ----------------

	subparser = parser_generate.add_subparsers(dest='subcommand')

	parser_wav = subparser.add_parser('wav', help='Generate a WAV file')
	parser_wav.add_argument('file', metavar='<file path>',  type=str, help='Output file path')
	parser_wav.add_argument('-b','--bpm', type=float, default=120, help='Tempo in quarter beats per minute')
	parser_wav.add_argument('-p','--ppq', type=int, choices=[24,48], default=24, help='parts per quarter note (ticks)')
	parser_wav.add_argument('-f','--frequency',  type=str, choices=['44.1','48','96'], default='44.1', help='Sampling frequency')
	parser_wav.add_argument('-a','--amplitude', type=int, choices=[25,50,75,100], default=100, help='amplitude in %%')
	parser_wav.add_argument('-d','--depth',  type=int, choices=[16,24], default=16, help='Sample bit depth')
	parser_wav.add_argument('-w','--width', type=int, choices=[5,10,25,50], default=50, help='pulse width in %%')
	parser_wav.add_argument('--bipolar', action='store_true',  help='generate bipolar wave')
	durex = parser_wav.add_mutually_exclusive_group(required=True)
	durex.add_argument('--minutes', type=mktime, metavar='<MM:SS>', default=None, help='Click track duration in minutes')
	durex.add_argument('--beats',   type=int, default=None, help='Click track duration in beats (quarter notes)')
	durex.add_argument('--bars',    type=int, default=None, help='Click track duration in 4/4 bars')
	return parser

# ================ #
# MAIN ENTRY POINT #
# ================ #

def main():
	'''
	Utility entry point
	'''
	try:
		options = createParser().parse_args(sys.argv[1:])
		configureLogging(options)
		setup(options)
		name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
		command  = f"{options.command}"
		subcommand = options.subcommand
		try:
			command = importlib.import_module(command, package=name)
		except ModuleNotFoundError:	# when debugging module in git source tree ...
			command  = f".{options.command}"
			command = importlib.import_module(command, package=name)
		log.info(f"============== {name} {__version__} ==============")
		getattr(command, subcommand)(options)
	except KeyboardInterrupt as e:
		log.critical("[%s] Interrupted by user ", __name__)
	except Exception as e:
		log.critical("[%s] Fatal error => %s", __name__, str(e) )
		traceback.print_exc()
	finally:
		pass

main()

