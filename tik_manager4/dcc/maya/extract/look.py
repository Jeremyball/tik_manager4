"""Extract Look from Maya scene"""

from maya import cmds
from maya import OpenMaya as om

import json

from tik_manager4.dcc.extract_core import ExtractCore
from tik_manager4.dcc.maya import utils


class Look(ExtractCore):
    """Extract Look from Maya scene."""

    nice_name = "Look"
    color = (244, 132, 132)

    def __init__(self):
        super().__init__()

        self.shading_groups = []
        self.mtls = []
        self.transforms = []
        self.asset = []
        self.thing = "asset"
        self._extension = ".mb"

        # Category names must match to the ones in category_definitions.json (case sensitive)
        self.category_functions = {
            "Model": self._extract_model,
            "Animation": self._extract_animation,
            "Fx": self._extract_fx,
            "Layout": self._extract_layout,
            "Lighting": self._extract_lighting,
        }

    def _extract_model(self):
        look_file = self.resolve_output().rpartition(".")[0] + ".look"

        ################
        # COLLECT mtls #
        ################

        for shape in cmds.listRelatives(self.thing, allDescendents=True, typ="shape"):
            sg = cmds.listConnections(shape, t="shadingEngine")
            if sg:
                self.transforms.append(cmds.listRelatives(shape, p=True)[0])
                self.shading_groups.append(sg[0])

                for mtl in cmds.listConnections(sg[0] + ".surfaceShader"):
                    self.mtls.append(mtl)

        ##############
        # WRITE mtls #
        ##############

        # select sg's for export
        cmds.select(self.shading_groups, ne=True)

        # export the shaders
        cmds.file(self.resolve_output(), type="mayaBinary", es=True, f=True)

        ##########################
        # COLLECT look file data #
        ##########################

        data = []

        for i in range(len(self.transforms)):

            entry = {
                "transform": self.transforms[i],
                "mtl": self.mtls[i],
                "sg": self.shading_groups[i],
            }

            data.append(entry)

        ########################
        # WRITE look file data #
        ########################

        with open(look_file, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def _extract_animation(self):
        pass

    def _extract_fx(self):
        pass

    def _extract_layout(self):
        pass

    def _extract_lighting(self):
        pass

    def _extract_default(self):
        pass
