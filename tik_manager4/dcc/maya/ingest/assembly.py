"""Ingest Assembly."""

from pathlib import Path
from maya import cmds
from maya import OpenMaya as om
from tik_manager4.dcc.ingest_core import IngestCore

class Assembly(IngestCore):
    """Ingest Assembly."""

    nice_name =  "Ingest Assembly"
    valid_extensions = [".mb"]
    referencable = True

    def __init__(self):
        super().__init__()

        self.category_functions = {"Model": self._bring_in_model,
                                   "Animation": self._bring_in_animation,
                                   "Fx": self._bring_in_fx,
                                   "Layout": self._bring_in_layout,
                                   "Lighting": self._bring_in_lighting,
                                   }

    def _bring_in_model(self):
        pass

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
        print(self._namespace)
        print(self.ingest_path)
        # node = cmds.file(self.ingest_path,
        #                r=True,
        #                ignoreVersion=True,
        #                loadReferenceDepth="asPrefs",
        #                mergeNamespacesOnClash=False,
        #                namespace=ns,
        #                returnNewNodes=1,
        #                options="v=0;"
        #                )