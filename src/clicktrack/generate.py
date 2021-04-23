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

import logging
import math
import wave
import struct

from fractions import Fraction

# ----------------
# Module constants
# ----------------

SAMPLING = { '44.1': 44100, '48': 48000, '96': 96000}

MAX_24_BITS_SIGNED = 8388607
MAX_16_BITS_SIGNED = 32767

AMPLITUDE = { 16: 32767, 24: 8388607 }

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("click")

# ----------------------
# Internal functions
# ----------------------


def make_square_wave(N, amplitude, duty_cycle, bipolar):
	split_point = N * duty_cycle
	f1 = lambda n: amplitude if ( (n % N) < split_point) else 0
	f2 = lambda n: amplitude if ( (n % N) < split_point) else -amplitude
	return f2 if bipolar else f1

def make_packer(depth):
	'''Wav files encode little endian bytes'''
	if depth == 24:
		f = lambda n: struct.pack('<i', n)[:-1]
	elif depth == 16:
		f = lambda n: struct.pack('<h', n)
	else:
		f = None
	return f

# ----------------------
# COMMAND IMPLEMENTATION
# ----------------------


def wav(options):
	log.info(f"Generating WAV file {options.file}")
	sampling_freq = int(SAMPLING[options.frequency])
	bpm     = options.bpm
	ppq     = options.ppq
	beats   = options.beats
	minutes = options.minutes
	bars    = options.bars
	bipolar = options.bipolar
	
	duty_cycle = options.width / 100
	bytes_per_sample = options.depth // 8

	amplitude = int(AMPLITUDE[options.depth] * (options.amplitude / 100))
	if minutes:
		duration = minutes.tm_min*60 + minutes.tm_sec
		log.info(f"{minutes.tm_min}:{minutes.tm_sec} minutes @ {bpm} bpm = {duration} seconds(s)")
	elif beats:
		duration = 60*options.beats/bpm
		log.info(f"{beats} beats @ {bpm} bpm = {duration} seconds(s)")
	elif bars:
		duration = 4*60*options.bars/bpm
		log.info(f"{bars} bars @ {bpm} bpm = {duration} seconds(s)")
	else:
		raise ValueError("Missing duration")

	# The E-RM multiclock device needs a unipolar square wave at 24 ppq resolution

	# Aquí estaria bien corregir los defciamles
	nsamples_per_tick = (60 * sampling_freq) / (ppq * bpm)
	nsamples_per_beat = int(round((60 * sampling_freq) / (bpm),0))
	nsamples_per_bar  = int(round((60 * 4 * sampling_freq) / (bpm),0))

	reminder = Fraction(nsamples_per_tick % 1)
	frequency = (2*bpm) / 5	# Square wave frequency to generate
	total_samples = int(round(sampling_freq * duration,0))
	log.info(f"Each tick has {int(nsamples_per_tick)} whole samples and a reminder of {reminder} samples")
	log.info(f"Needs {total_samples} samples for {duration} seconds(s)")
	square_wave = make_square_wave(nsamples_per_tick, amplitude, duty_cycle)
	packer = make_packer(options.depth)
	log.info(f"Bit depth = {options.depth}, {bytes_per_sample} bytes/sample")
	log.info(f"The resulting output waveform has a frequency of {frequency} Hz.")

	with wave.open(options.file,"wb") as wo:
		wo.setnchannels(1) # mono
		wo.setsampwidth(bytes_per_sample)
		wo.setframerate(sampling_freq)
		wo.setcomptype("NONE","not compressed")
		wo.setnframes(total_samples)
		if minutes:
			for t in range(0,total_samples):
				wo.writeframes(packer(square_wave(t)))
		elif beats:
			for beat in range(0,beats):
				samples = (packer(square_wave(t)) for t in range(0, nsamples_per_beat))
				wo.writeframes(b''.join(samples))
		else:
			for bar in range(0,bars):
				samples = (packer(square_wave(t)) for t in range(0, nsamples_per_bar))
				wo.writeframes(b''.join(samples))

