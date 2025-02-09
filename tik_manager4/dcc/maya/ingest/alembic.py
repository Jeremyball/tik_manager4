"""Ingest Alembic."""

from pathlib import Path
from maya import cmds
from maya import OpenMaya as om
from tik_manager4.dcc.ingest_core import IngestCore

class Alembic(IngestCore):
    """Ingest Alembic."""

    nice_name =  "Ingest Alembic"
    valid_extensions = [".abc"]
    referencable = True

    def __init__(self):
        super(Alembic, self).__init__()
        if not cmds.pluginInfo("AbcImport", loaded=True, query=True):
            try:
                cmds.loadPlugin("AbcImport")
            except Exception as exc:
                om.MGlobal.displayInfo("Alembic Import Plugin cannot be initialized")
                raise exc

        self.category_functions = {"Model": self._bring_in_model,
                                   "Animation": self._bring_in_animation,
                                   "Fx": self._bring_in_fx,
                                   "Layout": self._bring_in_layout,
                                   "Lighting": self._bring_in_lighting,
                                   }

    def _bring_in_model(self):
        """Import Alembic File."""
        om.MGlobal.displayInfo("Bringing in Alembic Model")
        cmds.AbcImport(self.ingest_path, mode="import", fitTimeRange=False, setToStartFrame=False)

    def _bring_in_animation(self):
        pass

    def _bring_in_fx(self):
        pass

    def _bring_in_layout(self):
        pass

    def _bring_in_lighting(self):
        pass

    def _bring_in_default(self):
        pass

    def _reference_default(self):
        pass