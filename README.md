# pyclicktrack

Utility to generate 16/24 bit WAV file click tracks with an unipolar/bipolar square wave.
Useful to generate a master clock to sync MIDI instruments using devices like the [E-RM multiclock](https://www.e-rm.de/multiclock/).
The output file can be reporduced in a DAW or - for DAWless recording - setup in a separate track when using digital multitrack recorder like [Zoom R24](https://zoomcorp.com/es/us/mezcladores-digitales--grabadoras-multipistas/multi-track-recorders/r24/).

# Installation

```bash
python3 setup.py install
```

# Execution

The utility is self-explanatory:

```bash
python3 -m clicktrack --help
```

It is faster when using `--beats` or `--bars` duration option.
Default values:
* `--ppq`: 24 PPQ
* `--bpm`: 120 bpm
* `--frequency`: 44.1 KHz
* `--amplitude`: 100%
* `--depth`: 16 bits
* `--width`: 50% pulse width
* `--bipolar`: False