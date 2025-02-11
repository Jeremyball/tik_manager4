"""Ingest Assembly."""

from pathlib import Path
from maya import cmds
from maya import OpenMaya as om
from tik_manager4.dcc.ingest_core import IngestCore


class Assembly(IngestCore):
    """Ingest Assembly."""

    nice_name = "Ingest Assembly"
    valid_extensions = [".mb"]
    referencable = True

    def __init__(self):
        super().__init__()

        self.category_functions = {"Model": self._bring_in_model}

    def _bring_in_model(self):
        pass

    def _reference_default(self):
        cmds.file(
            self.ingest_path,
            r=True,
            ignoreVersion=True,
            loadReferenceDepth="asPrefs",
            mergeNamespacesOnClash=False,
            namespace=self._namespace,
            returnNewNodes=1,
            options="v=0;",
        )
