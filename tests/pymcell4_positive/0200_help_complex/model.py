import sys
import os
import pydoc


MCELL_PATH = os.environ.get('MCELL_PATH', '')
if MCELL_PATH:
    sys.path.append(os.path.join(MCELL_PATH, 'lib'))
else:
    print("Error: variable MCELL_PATH that is used to find the mcell library was not set.")
    sys.exit(1)
    
import mcell as m

# __doc__ must be set
assert "This class represents" in m.Complex.__doc__

# and a small check that attributes have documentation as well
help_result_string = pydoc.render_doc(m.Complex)
assert "Specifies compartment" in help_result_string
