# mesh_utils: the mesh table and the mesh checks

`test.sh` runs `bin/mesh_utils_test` of the MCell build (source: `mcell/utils/mesh_utils_test`) on the
files here. It checks the code of `mcell/src4/mesh_table.hpp`, which takes a geometry object's
connectivity only from the vertex indices of its walls.

- `connectivity/<name>.walls` and `<name>.expected`: the 131 meshes of the prototype check
  `check_edge_table_proto.py` (bow-ties, pinches, edges of three or more walls, flipped walls,
  Moebius strips, random soups and glued grids), and the walls of the six report meshes where
  non-manifold cases come together (`book_bowtie_pinched`, `bowtie_and_pinched`, `same_vertex_*`).
  The expected results are those of `coboundary.py`
  (`mesh_operators`, `classify`), SciPy and NumPy. They were computed once, outside this
  repository; the test never runs Python.
- `reports/<name>.mesh` and `<name>.report`: small meshes with coordinates, one per error or
  warning, and the block each gets in the geometry report. Six of them combine an edge of three or
  more walls, bow-tie vertices and pinched vertices, at different vertices or at the same vertex;
  the report lists every non-manifold vertex once, without saying which case it is. The blocks were
  written by hand and checked against the same tools.
