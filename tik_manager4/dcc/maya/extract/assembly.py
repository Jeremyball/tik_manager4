"""Extract Assembly from Maya scene"""

from maya import cmds
from maya import OpenMaya as om

import json
import os

from tik_manager4.dcc.extract_core import ExtractCore
from tik_manager4.dcc.maya import utils


class Assembly(ExtractCore):
    """Extract Assembly from Maya scene."""

    nice_name = "Assembly"
    color = (255, 255, 255)

    def __init__(self):
        super().__init__()

        # Category names must match to the ones in category_definitions.json (case sensitive)
        self.category_functions = {
            "Model": self._extract_model,
            "Animation": self._extract_animation,
            "Fx": self._extract_fx,
            "Layout": self._extract_layout,
            "Lighting": self._extract_lighting,
        }

    def _extract_model(self):
        publishes = os.listdir(self.extract_folder)
        looks = []
        alembics = []

        # get look and alembic publishes
        for i in publishes:
            if "LOOK_" in i:
                looks.append(i)
            if "ALEMBIC_" in i:
                alembics.append(i)

        # get latest alembics, mtls and link
        abc_file = self.extract_folder + "/" + alembics[-1]
        mtls_file = self.extract_folder + "/" + looks[-1]
        link_file = self.extract_folder + "/" + looks[-2]

        # save scene
        curr_file = cmds.file(save=True, force=True)

        # open new scene
        cmds.file(new=True, ignoreVersion=True, f=True)

        # import alembic
        cmds.AbcImport(
            abc_file, mode="import", fitTimeRange=False, setToStartFrame=False
        )

        # import shaders
        cmds.file(mtls_file, i=True)

        ################
        # link shaders #
        ################

        # open linker file
        with open(link_file) as data_file:
            link_data = json.load(data_file)

        for i in link_data:
            cmds.select(i["transform"])
            cmds.hyperShade(assign=i["mtl"])

        # save as assembly
        cmds.file(rename=self.resolve_output())
        cmds.file(save=True, type="mayaBinary")

        # open original file
        cmds.file(curr_file, open=True, force=True)

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
