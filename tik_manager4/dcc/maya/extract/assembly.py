"""Extract Assembly from Maya scene"""

from maya import cmds
from maya import OpenMaya as om

import json
import os

from tik_manager4.dcc.extract_core import ExtractCore
from tik_manager4.dcc.maya import utils
from tik_manager4.dcc.maya import flux_utility

class Assembly(ExtractCore):
    """Extract Assembly from Maya scene."""

    nice_name = "Assembly"
    color = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.extension = ".mb"
        self.category_functions = {
            "Model": self._extract_model,
            "Rig": self._extract_rig,
        }

    def _extract_model(self):

        asset_colour = [.2,.9,.2]

        # get files
        looks = self._get_files("LOOK", self.extract_folder)
        model = self._get_files("MB", self.extract_folder)

        # get latest alembics, mtls and link
        model_file = self.extract_folder + "/" + model[-1]
        mtls_file = self.extract_folder + "/" + looks[-1]
        link_file = self.extract_folder + "/" + looks[-2]

        # save scene
        curr_file = cmds.file(save=True, force=True)

        # open new scene
        cmds.file(new=True, ignoreVersion=True, f=True)

        # import model
        cmds.file(model_file, i=True)

        # import shaders
        cmds.file(mtls_file, i=True)

        # set .extract_script to ASSEMBLY
        cmds.setAttr("asset.extract_script", "ASSEMBLY", type="string")        

        # colour asset group
        flux_utility.colour_load(asset_colour, "asset")

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

    def _extract_rig(self):

        model_publish_folder = self.extract_folder.replace("Rig", "Model")

        # get files
        looks = self._get_files("LOOK", model_publish_folder)
        rig = self._get_files("MB", self.extract_folder)

        # get latest alembics, mtls and link
        rig_file = self.extract_folder + "/" + rig[-1]
        mtls_file = model_publish_folder + "/" + looks[-1]
        link_file = model_publish_folder + "/" + looks[-2]

        # open new scene
        cmds.file(new=True, ignoreVersion=True, f=True)

        # import rig
        cmds.file(rig_file, i=True)

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
        cmds.file(rename="null")


    def _get_files(self, extractor, location):
        publishes = os.listdir(location)
        files = []

        # get look and alembic publishes
        for i in publishes:
            if extractor + "_" in i:
                files.append(i)

        return files
