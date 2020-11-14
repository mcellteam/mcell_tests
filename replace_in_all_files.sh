#!/bin/bash
# this is an auxiliary script used e.g. when API changes
find ./ -type f -exec sed -i "s/MCELL_NO_COMPARTMENT_SIZE/MCELL_DEFAULT_COMPARTMENT_VOLUME/g" {} \;