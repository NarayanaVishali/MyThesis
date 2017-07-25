#!/usr/bin/env python
import sys
sys.path.append('./')

previous_date = None
previous_potential = 0

for line in sys.stdin:
    (this_date, potential_value) = line.strip().lstrip().split("\t")
    potential_value = float(potential_value)
    if previous_date == this_date:
        previous_potential += potential_value
    else:
        if previous_date:
            print '%s\t%s' % (previous_date, previous_potential)
        previous_date = this_date
        previous_potential = potential_value

if this_date == previous_date:
    print '%s\t%s' % (previous_date, previous_potential)
