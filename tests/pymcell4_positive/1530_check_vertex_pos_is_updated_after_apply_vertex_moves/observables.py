import mcell as m

# ---- observables ----
SEED = 1
viz_output = m.VizOutput(
    mode = m.VizMode.ASCII,
    output_files_prefix = './viz_data/seed_' + str(SEED).zfill(5) + '/Scene',
    every_n_timesteps = 1
)

observables = m.Observables()
observables.add_viz_output(viz_output)
