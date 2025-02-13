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
        super().__init__()
        self.extension = ".mb"

        self.category_functions = {
            "Lighting": self._render
        }

    def _render(self):
        print(self.resolve_output())
      