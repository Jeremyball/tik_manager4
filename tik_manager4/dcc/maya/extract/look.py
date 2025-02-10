"""Extract Alembic from Maya scene"""

from maya import cmds

from tik_manager4.dcc.extract_core import ExtractCore
from tik_manager4.dcc.maya import utils


class Look(ExtractCore):
    """Extract Alembic from Maya scene."""

    nice_name = "Look"
    color = (244, 132, 132)

    def __init__(self):
        super().__init__()

        self.shading_groups = []
        self.mtls = []
        self.shapes = []
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
        # get mtls
        for shape in cmds.listRelatives(self.thing, allDescendents=True, typ="shape"):
            sg = cmds.listConnections(shape, t="shadingEngine")
            if sg:
                self.shapes.append(shape)
                self.shading_groups.append(sg[0])

                for mtl in cmds.listConnections(sg[0] + ".surfaceShader"):
                    self.mtls.append(mtl)

        # select sg's for export
        cmds.select(self.shading_groups, ne=True)

        # export the shaders
        cmds.file(self.resolve_output(), type="mayaBinary", es=True, f=True)

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
