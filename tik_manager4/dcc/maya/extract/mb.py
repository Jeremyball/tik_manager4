"""Extract Maya scene."""

from maya import cmds
from maya import OpenMaya as om
import maya.mel as mel
from tik_manager4.dcc.extract_core import ExtractCore


# The Collector will only collect classes inherit ExtractCore
class MayaBinary(ExtractCore):
    """Extract Source Maya scene."""

    nice_name = "Maya Binary"
    color = (255, 255, 255)

    def __init__(self):
        super(MayaBinary, self).__init__()
        self.extension = ".mb"
        self.category_functions = {"Rig": self._extract_rig}

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
