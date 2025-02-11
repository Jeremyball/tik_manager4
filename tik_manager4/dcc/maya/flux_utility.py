import maya.cmds as cmds


def colours_tags():
    pass


def add_animated_attr(thing):
    for i in cmds.ls(thing):
        if cmds.nodeType(i) == "transform":
            attr = "extract_abc"

            if not cmds.attributeQuery(attr, node=i, exists=True):
                cmds.addAttr(i, ln=attr, at="bool")

            cmds.setAttr(i + "." + attr, e=True, k=False)
            cmds.setAttr(i + "." + attr, e=1, cb=1)
