import mcell as m

from geometry import *

# ---- observables ----
viz_output = m.VizOutput()

count_a = m.Count(
    name = 'a',
    expression = m.CountTerm(
        species_pattern = m.Complex('a'),
        region = Sphere1 
    ) 
) 

count_b = m.Count(
    name = 'b',
    expression = m.CountTerm(
        species_pattern = m.Complex('b'),
        region = Sphere2
    ) 
) 

observables = m.Observables()
observables.add_viz_output(viz_output)
observables.add_count(count_a)
observables.add_count(count_b)
