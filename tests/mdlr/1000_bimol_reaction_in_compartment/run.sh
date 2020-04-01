python /nadata/cnl/home/ahusar/src4/mcell/src/rules_py/mdlr2mdl.py -ni Scene.mdlr -o Scene

/nadata/cnl/home/ahusar/src4/mcell_tools/work/build_mcell/mcell Scene.main.mdl -rules Scene.mdlr_rules.xml


#python /nadata/cnl/home/ahusar/src4/mcell_tools/work/build_mcell/mcell3r.py -s 1 -r Scene.mdlr_rules.xml -m Scene.main.mdl
#python /nadata/cnl/home/ahusar/src4/mcell_tools/work/build_mcell/postprocess_mcell3r.py 1 Scene.mdlr_rules.xml