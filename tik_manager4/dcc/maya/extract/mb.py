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
        exposed_settings = {
            "Model": {
                "anim_publish": {
                    "display_name": "Publish with a Anim publish",
                    "type": "boolean",
                    "value": True,
                },
                "abc_publish": {
                    "display_name": "Publish as an .abc",
                    "type": "boolean",
                    "value": False,
                },
            },
            "Rig": {
                "anim_publish": {
                    "display_name": "Publish with a Anim publish",
                    "type": "boolean",
                    "value": True,
                },
                "abc_publish": {
                    "display_name": "Publish as an .abc",
                    "type": "boolean",
                    "value": True,
                },
            },
            "Layout": {
                "anim_publish": {
                    "display_name": "Publish with a Anim publish",
                    "type": "boolean",
                    "value": True,
                },
                "abc_publish": {
                    "display_name": "Publish as an .abc",
                    "type": "boolean",
                    "value": False,
                },
            },            
        }

        super().__init__(exposed_settings=exposed_settings)

        self.extension = ".mb"

        self.category_functions = {
            "Rig": self._extract_rig,
            "Model": self._extract_model,
            "Layout": self._extract_layout,
        }

    def _extract_model(self):

        settings = self.settings.get("Model")
        _file_path = self.resolve_output()

        ##################
        # add flux attrs #
        ##################

        flux_utility.attr_config(settings)

        #######
        # out #
        #######

        cmds.select("asset")

        cmds.file(
            _file_path,
            options="v=1;",
            typ="mayaBinary",
            es=True,
            constructionHistory=True,
            f=1,
            shader=0,
        )

    def _extract_rig(self):

        settings = self.settings.get("Rig")

        ###############
        # exract prep #
        ###############

        try:
            # non destructive shader remove
            mel.eval("deleteShadingGroupsAndMaterials")
            mel.eval(
                'hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");'
            )
        except:
            pass

        ##################
        # add flux attrs #
        ##################

        flux_utility.attr_config(settings)

        #######
        # out #
        #######

        cmds.select("asset")

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

    def _extract_layout(self):
        
        settings = self.settings.get("Layout")

        ##################
        # add flux attrs #
        ##################

        flux_utility.attr_config(settings)

        #######
        # out #
        #######

        cmds.select("asset")

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
