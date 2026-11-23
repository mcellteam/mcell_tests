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
- `reports/<name>.mesh`, `<name>.report` and `<name>.lines`: small meshes with coordinates, one per
  error or warning, the block each gets in the geometry report, and the terminal lines MCell prints
  for it (none for a mesh without problems). Six of them combine an edge of three or more walls,
  bow-tie vertices and pinched vertices, at different vertices or at the same vertex; the report
  lists every non-manifold vertex once, without saying which case it is. The blocks and lines were
  written by hand and checked against the same tools.
  - A `.mesh` file gives an object as the model gives it. Its vertex and wall lines may hold any
    number of values, as the Python API's lists may (`malformed_lists`). Optional lines after the
    walls: `region <name> <wall indices>` for a surface region (`region_indices`), and
    `removed <wall ids>`, which makes it an MDL object as MCell3 parsed it, with the walls MCell3
    removed (`removed_walls`: one by `REMOVE_ELEMENTS`, left out, and one for its zero area,
    reported; `removed_wall_out_of_range`: one by `REMOVE_ELEMENTS`, left out, and one with vertex
    index -1, which is checked like any wall and reported out of range).
  - Orphaned vertices, which no wall uses, are an error: `orphaned_vertices` (a cube with two
    more vertices) and `removed_walls_orphan` (an octahedron whose `REMOVE_ELEMENTS` removes the
    four walls around a vertex, which is then orphaned). The connectivity meshes' orphaned vertices
    (the glued grids have some) are checked against the vertices that no wall of the file uses.
- The singular and plural form of every terminal line, and the message of the one stop, are
  written in the test program itself.
