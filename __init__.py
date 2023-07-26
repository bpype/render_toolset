# Copyright (C) 2023 Aditia A. Pratama | aditia.ap@gmail.com
#
# This file is part of bpype.
#
# bpype is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bpype is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bpype.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Render Toolset",
    "author": "bpype, aditiavfx",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "Bpype Toolset for Rendering Workflow",
    "warning": "",
    "doc_url": "",
    "category": "Pipeline",
}

import bpy
import importlib
from bpy.utils import register_class, unregister_class
from typing import List
from . import ops, props, ui, keymaps, icons, prefs

modules = (
    props,
    keymaps,
    ops,
    ui,
    icons,
    prefs,
)


#! REGISTRATION
def register_unregister_modules(modules: List, register: bool):
    """Recursively register or unregister modules by looking for either
    un/register() functions or lists named `registry` which should be a list of
    registerable classes.
    """
    register_func = register_class if register else unregister_class

    for m in modules:
        if register:
            importlib.reload(m)
        if hasattr(m, "registry"):
            for c in m.registry:
                try:
                    register_func(c)
                except Exception as e:
                    un = "un" if not register else ""
                    print(f"Warning: Failed to {un}register class: {c.__name__}")
                    print(e)

        if hasattr(m, "modules"):
            register_unregister_modules(m.modules, register)

        if register and hasattr(m, "register"):
            m.register()
        elif hasattr(m, "unregister"):
            m.unregister()


def register():
    # importlib.reload(quad_swords)
    register_unregister_modules(modules, True)


def unregister():
    register_unregister_modules(modules, False)
