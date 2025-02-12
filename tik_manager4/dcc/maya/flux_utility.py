import maya.cmds as cmds


def colours_tags():
    pass


def add_attr(type, attr, thing, value, cb):

    if not cmds.attributeQuery(attr, node=thing, exists=True):
        if type == "bool":
            cmds.addAttr(thing, ln=attr, at="bool")
        if type == "int":
            cmds.addAttr(thing, ln=attr, at="long")
        if type == "string":
            cmds.addAttr(thing, ln=attr, dt="string")

    cmds.setAttr(thing + "." + attr, e=True, k=False)

    if type == "string":
        cmds.setAttr(thing + "." + attr, value, type="string")
        cmds.setAttr(thing + "." + attr, e=True, k=False)
    else:
        cmds.setAttr(thing + "." + attr, value)

    if cb:
        cmds.setAttr(thing + "." + attr, e=1, cb=1)


def attr_config(settings):
    add_attr("bool", "extract_abc", "asset", settings.get("abc_publish"), True)
    add_attr("bool", "extract_anim", "asset", settings.get("anim_publish"), True)
    add_attr("bool", "tik_publish", "asset", True, True)
