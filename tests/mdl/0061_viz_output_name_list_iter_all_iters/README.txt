This is a reference test that dumps viz output every timestep compared to 
0062 that dumps viz data every 10 timesteps
  
  
In MCell 3.4 that simulation result differs when viz_output is set with periodicity 10 vs 1.


VIZ_OUTPUT
{
  MODE = ASCII
  FILENAME = "./viz_data/seed_" & seed & "/Scene"
  MOLECULES
  {
    NAME_LIST {a c}
    //second variant: ITERATION_NUMBERS {ALL_DATA @ [[0 TO 5000 STEP 10]]}
    ITERATION_NUMBERS {ALL_DATA @ ALL_ITERATIONS}
  }
}

Reason is described below, to get identical behavior, debug macro 
MCELL3_NEXT_BARRIER_IS_THE_NEXT_TIMESTEP was introduced.


The reason is that in run_timestep 
https://github.com/mcellteam/mcell/blob/master/src/diffuse.c#L3703​

max_time is computed from release_time:
​

         if ​(max_time > release_time - am->t)



max_time = release_time - am->t;
....





am = (struct abstract_molecule *)diffuse_3D(

state, (struct volume_molecule *)am, max_time);


for the variant with all iterations, release_time is 1, but for the variant with periodicity 10, release_time is 10.
This then results in the molecule (c, idx 20 from the attached dumps) to be diffused in this example for 7.9 us instead of 0.9 us.

The release_time argument is computed in mcell_run_iteration:
https://github.com/mcellteam/mcell/blob/master/src/mcell_run.c#L516


double next_barrier =



min3d(next_release_time, next_vol_output, next_viz_output);

..  

run_timestep(world, local->store, next_barrier,

(double)world->iterations +
1.0);
...




All molecules in the model with viz periodicity 10 get this long 'max_time'.​
However, only for molecules created in the middle of a timestep, 



if (*steps == 1.0) {

pick_displacement(displacement, m->get_space_step(m), world->rng);

*r_rate_factor = *rate_factor = 1.0;

} else {

*rate_factor = sqrt(*steps);

*r_rate_factor = 1.0 / *rate_factor;

pick_displacement(displacement, *rate_factor * m->get_space_step(m), world->rng);

}​


This viz_output periodicity of 10 is used in the rat NMJ example.

  