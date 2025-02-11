import maya.cmds as cmds


def colours_tags():
    pass


def add_bool_attr(attr, thing, value):
    for i in cmds.ls(thing):
        if cmds.nodeType(i) == "transform":

            if not cmds.attributeQuery(attr, node=i, exists=True):
                cmds.addAttr(i, ln=attr, at="bool")

            cmds.setAttr(i + "." + attr, e=True, k=False)
            cmds.setAttr(i + "." + attr, e=1, cb=1)
            cmds.setAttr(i + "." + attr, value)


def add_int_attr(attr, thing, value):
    for i in cmds.ls(thing):
        if cmds.nodeType(i) == "transform":

            if not cmds.attributeQuery(attr, node=i, exists=True):
                cmds.addAttr(i, ln=attr, at="long")

            cmds.setAttr(i + "." + attr, e=True, k=False)
            cmds.setAttr(i + "." + attr, e=1, cb=1)
            cmds.setAttr(i + "." + attr, value)


def add_attr(type, attr, thing, value):
    for i in cmds.ls(thing):
        if cmds.nodeType(i) == "transform":

            if not cmds.attributeQuery(attr, node=i, exists=True):
                if type == "bool":
                    cmds.addAttr(i, ln=attr, at="bool")
                if type ==  "int":
                    cmds.addAttr(i, ln=attr, at="long")    
                if type == "string":
                    cmds.addAttr(i, ln=attr, dt="string")

            cmds.setAttr(i + "." + attr, e=True, k=False)
            
            if type == "string":
                cmds.setAttr(i + "." + attr, value, type="string")
                cmds.setAttr(i + "." + attr, e=True, k=False)      
            else:          
                cmds.setAttr(i + "." + attr, e=1, cb=1)
                cmds.setAttr(i + "." + attr, value)