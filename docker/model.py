import pathlib as pl

class Model(object):
    def __init__(self, path, scale, scene):
        self.path_ = pl.Path(path)
        self.scale_ = float(scale)
        self.scene_ = pl.Path(scene)
        self.done_ = False
        # check to see if the cloud already exists
        print("Checking path: ", self.path_)
        if self.path_.exists():
            pcd_fname = self.pcd_name
            target = self.scene_ / pcd_fname
            print(" Checking target: ", target)
            if target.exists() and target.stat().st_size > 0:
                self.done_ = True
            elif target.exists():
                target.unlink()
        else:
            print(" Path doesn't exist")

    @property
    def done(self):
        return self.done_
                
    @property
    def pcd_name(self):
        pcd_fname = self.path_.stem + ".pcd"
        return pcd_fname
            
    @property
    def path(self):
        return pl.Path(self.path_)

    @property
    def scale(self):
        return self.scale_

    @property
    def scene(self):
        return pl.Path(self.scene_)
