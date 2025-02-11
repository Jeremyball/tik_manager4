"""Extract Maya scene."""

from maya import cmds
from maya import OpenMaya as om
import maya.mel as mel

from tik_manager4.dcc.extract_core import ExtractCore
from tik_manager4.dcc.maya import flux_utility

# The Collector will only collect classes inherit ExtractCore
class MayaBinary(ExtractCore):
    """Extract Source Maya scene."""

    nice_name = "Maya Binary"
    color = (255, 255, 255)

    def __init__(self):
        self.extension = ".mb"
        self.category_functions = {"Rig": self._extract_rig,"Model": self._extract_model}
        
        exposed_settings = {
            "Model": {
                "anim_publish": {
                    "display_name": "Anim Publish",
                    "type": "boolean",
                    "value": True,
                },
                "abc_publish": {
                    "display_name": "Abc Publish",
                    "type": "boolean",
                    "value": True,
                },
            },
        }        
        
        super().__init__(exposed_settings=exposed_settings)

    def _extract_model(self):
        """Extract method for model category"""

        settings = self.settings.get("Model")
        version_number = int(self.extract_name.split("_v")[1])
        _file_path = self.resolve_output()

        ##################
        # add flux attrs #
        ##################

        flux_utility.add_bool_attr("extract_abc", "asset", settings.get("abc_publish"))

        cmds.select("fege")
        
        if not cmds.attributeQuery("test", node="asset", exists=True):
            cmds.addAttr("asset", ln="test", at="bool")


        #############
        # export mb #
        #############

        cmds.file(_file_path, options="v=1;", typ="mayaBinary", es=True, constructionHistory=True, f=1, shader=0)

    def _extract_rig(self):
        """Extract method for any non-specified category"""

        # remove all materials
        try:
            # non destructive shader remove
            mel.eval("deleteShadingGroupsAndMaterials")
            mel.eval(
                'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");'
            )

        except:
            pass

        # select asset
        cmds.select("asset")

        # export asset
        cmds.file(
            self.resolve_output(),
            force=True,
            typ="mayaBinary",
            exportSelected=True,
            preserveReferences=False,
            constructionHistory=True,
            constraints=True,
            expressions=True,
            shader=False,
        )

    def _extract_default(self):
        # select asset
        cmds.select("asset")

        # export asset
        cmds.file(
            self.resolve_output(),
            force=True,
            typ="mayaBinary",
            exportSelected=True,
            preserveReferences=True,
            constructionHistory=True,
            constraints=True,
            expressions=True,
            shader=True,
        )
