#!/usr/bin/env python

# Author: Anders Dalskov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os
import sys

RATES = ''
EXCH_FILE = 'rates.json'
FIXER_IO = 'https://api.fixer.io/latest'

# Run update.
if len(sys.argv) > 1 and (sys.argv[1] in ('u', 'update')):
    import urllib.request
    new_rates = json.loads(urllib.request.urlopen(FIXER_IO).read())
    RATES = new_rates
    with open(EXCH_FILE, 'w') as f:
        f.write(json.dumps(new_rates))
    exit(0)

# Load exchange rate file
if os.path.exists(EXCH_FILE):
    with open(EXCH_FILE, 'r') as f:
        RATES = json.loads(f.read())
else:
    print(f'file "rates.json" could not be found')
    print("Try re-running the program with the `u' or `update' option")
    exit(1)


# Pretty print the currencies that are recongnized.
def pprint_avail_rates(rates, line_len=10):
    if rates != '':
        print('Available rates:')
        r = list(rates['rates'].keys())
        r.append(rates['base'])
        rp = ''
        for i in range(len(r)):
            rp += r[i]
            if (i+1) % line_len == 0:
                rp += '\n'
            else:
                rp += ' '
        print(rp)


if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} base target')
    pprint_avail_rates(RATES)
    exit(1)

sys.stderr.write(f'Using rates from {RATES["date"]}\n')

base = sys.argv[1].upper()
targ = sys.argv[2].upper()
_base = RATES['base']  # the `standard' base used by fixer.io
_rates = RATES['rates']
_rates[_base] = 1.0  # add base to list of rates
mult = 1.0 if len(sys.argv) == 3 else float(sys.argv[3])

if (base not in _rates and base != _base):
    print(f'unknown symbol: "{base}"')
    pprint_avail_rates(RATES)
    exit(1)

if targ not in _rates:
    print(f'unknown symbol: "{targ}"')
    pprint_avail_rates(RATES)
    exit(1)

# Switch the base, in case our input base doesn't match the one
# fixer.io uses by default (which is EUR AFAIK)
if base != _base:
    base_v = _rates[base]
    for r in _rates:
        _rates[r] /= base_v
    _rates[_base] = 1 / base_v
else:
    _rates[_base] = 1.0

print(f'{_rates[base]*mult:.4f} {base} is {_rates[targ]*mult:.4f} {targ}')
