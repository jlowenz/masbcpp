#!/usr/bin/env python3

import pathlib as pl
import os, signal, sys
import subprocess as sp
import joblib as jl
import itertools as it
import datetime as dt
from argparse import ArgumentParser

scene_script="/code/pkgs/masbcpp/docker/masbcpp.sh"

def kill_child_processes(signum, frame):
    parent_id = os.getpid()
    ps_command = sp.Popen("ps -o pid --ppid %d --noheaders" % parent_id, shell=True, stdout=subprocess.PIPE)
    ps_output = ps_command.stdout.read()
    retcode = ps_command.wait()
    for pid_str in ps_output.strip().split("\n")[:-1]:
        os.kill(int(pid_str), signal.SIGKILL)
    sys.exit()

def process(in_file, radius):
    print("Processing PCD: {}".format(str(in_file)))
    par_dir = in_file.parent
    ret = sp.call("{0} -d 5 -p 5 -r {1} {2} {3}".format(scene_script,
                                                        radius,
                                                        str(in_file),
                                                        str(par_dir)), shell=True)
    if ret != 0:
        return (False,in_file,radius)
    return (True,in_file,radius)

def run(r, files):
    output = jl.Parallel(n_jobs=8)(jl.delayed(process)(f,r) for f in files)
    redo = list(filter(lambda x: not x[0], output))
    return redo

def main():
    signal.signal(signal.SIGTERM, kill_child_processes)
    signal.signal(signal.SIGINT, kill_child_processes)
    usage = "{} <args> : Process PCD files for medial axis".format(scene_script)
    parser = ArgumentParser(usage=usage)
    parser.add_argument("dirs", nargs="+")
    parser.add_argument("-r", "--radius", type=float, default=2.0,
                        help="Initial ball radius")
    args = parser.parse_args()

    all_pcds = []
    for d in args.dirs:
        dd = pl.Path(d)
        for pcd in dd.glob("**/*.pcd"):
            all_pcds.append(pcd)
            
    redo = run(args.radius, all_pcds)
    max_retries = 3
    retries = 0
    while len(redo) > 0 and retries < max_retries:
        print("Redoing {} files".format(len(redo)))
        files = [ret[1] for ret in redo]
        redo = run(args.radius, files)
        retries += 1

if __name__=="__main__":
    main()
    
