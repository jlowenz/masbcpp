#!/usr/bin/env python3

import string
import pathlib as pl
import sys
from optparse import OptionParser
import joblib as jl
import shutil
import subprocess as sp
from model import Model

def process(model):
    path_to_mesh2pcd = "/NAS/home/dev/ws/mesh/src/mesh2pcd/docker/mesh2pcd.sh"
    # run the mesh2pcd on this model
    print("Processing: {0}".format(model.path))
    if model.done:
        print("  skipping...")
        return (True,model)
    print("  working...")
    # parse the path to generate the pcd name
    pcd_fname = model.path.stem + ".pcd"
    pcd_path = model.path.parent / pcd_fname
    scene_pcd = model.scene / pcd_fname
    if scene_pcd.exists():
        # avoid the processing if the model exists
        return True
    proc = sp.Popen([path_to_mesh2pcd,
                     str(model.path),
                     str(pcd_path),
                     "-scale", str(model.scale)])
    ret = proc.wait()
    shutil.copy(str(pcd_path), str(model.scene))
    return ret == 0
        
def run(models, nprocs):
    print("models",models[0].scale," ",nprocs)
    output = jl.Parallel(n_jobs=nprocs)([jl.delayed(process)(m)
                                         for m in models])
    redo = [m for (s,m) in zip(output,models) if s]
    return redo

def do_parse(scene,cat,opts):
    return scene.is_dir() and \
      (cat == opts.category or \
           (opts.category == "" and \
                cat not in opts.filter))

def main():
    usage = "run_mesh2pcd.py [options] /path/to/shapenet /path/to/scenes"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--category", type=str, default="",
                      help="Specify the object category to use.")
    parser.add_option("-f", "--filter", type=str, action="append",
                      help="Ignore the given object category")
    parser.add_option("-j", "--nprocs", type=int, default=8,
                      help="Number of parallel processes to launch")

    opts,args = parser.parse_args()
    if len(args) != 2:
        parser.print_usage()
        exit(1)

    shapenet_dir = pl.Path(args[0])
    # get all the models to process
    base_dir = pl.Path(args[1])
    models = []
    if base_dir.exists():
        for scene in base_dir.iterdir():
            cat = scene.name.split("_")[0]
            if do_parse(scene, cat, opts):
                # get the scene_description
                with open(str(scene / "scene_description.txt"),"r") as sd:
                    sd.readline() # layout
                    # single shapenet path
                    apath = pl.Path(sd.readline().strip())
                    path = shapenet_dir / "/".join(apath.parts[-4:])
                    wnid = sd.readline().strip()
                    tags = sd.readline().strip()
                    scale = float(sd.readline())
                    models.append(Model(path,scale,scene))

        # launch the parallel processes to generate the pcds
        count = 0
        redo = run(models,opts.nprocs)
        while count < 5 and len(redo) > 0:
            count += 1
            redo = run(redo,opts.nprocs)

    else:
        raise RuntimeError("Base path to scenes not found")

if __name__ == "__main__":
    main()
    print("DONE!")
