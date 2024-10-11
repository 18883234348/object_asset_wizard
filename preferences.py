# Copyright (C) 2019 h0bB1T
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
#
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import bpy, os,platform
from bpy.types import AddonPreferences
from bpy.props import StringProperty, EnumProperty, BoolProperty, FloatProperty

from .t3dn_bip.ops import InstallPillow

if platform.system() == 'Windows':
    AW_lib = 'Z:/Projects/Code/AW_lib'
elif platform.system() == 'Darwin':  # MacOS的系统平台名称
    AW_lib = '/user/test'
    
class T3DN_OT_bip_showcase_install_pillow(bpy.types.Operator, InstallPillow):
    bl_idname = 't3dn.bip_showcase_install_pillow'


class PreferencesPanel(AddonPreferences):
    bl_idname = __package__

    preview_engine_type = (
        ('CYCLES', "Cycles", ""),
        ('BLENDER_EEVEE', "Eevee", ""),
    )

    root: StringProperty(name="Asset root directory",
        default=AW_lib,
        description="Path to Root Asset Directory",
        subtype="DIR_PATH"
        )# type: ignore

    preview_engine: EnumProperty(name="Preview render engine", items=preview_engine_type)# type: ignore
    show_blend: BoolProperty(name="Show .blend", default=True)# type: ignore
    show_fbx: BoolProperty(name="Show .fbx", default=True)# type: ignore
    compact_panels: BoolProperty(name="Use compact panels", default=True)# type: ignore
    separate_categories: BoolProperty(name="Visually separate top categories", default=True)# type: ignore

    preview_scale: FloatProperty(
        name="Scale factor for previews",
        default=1.0,
        soft_min=0.2,
        soft_max=5.0
    )# type: ignore

    use_category_icons: BoolProperty(name="Use category icons", default=False)# type: ignore

    export_remap: EnumProperty(
        name="Remap export paths:",
        items=[
            ('NONE', "NONE", "No path manipulation (default)"),
            ('RELATIVE', "RELATIVE", "Remap paths that are already relative to the new location"),
            ('RELATIVE_ALL', "RELATIVE_ALL", "Remap all paths to be relative to the new location"),
            ('ABSOLUTE', "ABSOLUTE", "Make all paths absolute on writing"),
        ],
        default='ABSOLUTE'
    )# type: ignore

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "root", text="Root Asset Directory")
        c = layout.column(align=True)
        r = c.row(align=True)
        r.prop(self, "show_blend", toggle=True)
        r.prop(self, "show_fbx", toggle=True)
        c.prop(self, "compact_panels", toggle=True)
        c.prop(self, "separate_categories", toggle=True)
        # self.layout.row().prop(self, "use_category_icons", toggle=True)
        c.prop(self, "preview_scale")

        layout.prop(self, "preview_engine")
        from .utils import blender_2_8x
        if not blender_2_8x():
            self.layout.row().prop(self, "export_remap", expand=True)

        layout.operator('t3dn.bip_showcase_install_pillow')

    @staticmethod
    def get():
        return bpy.context.preferences.addons[__package__].preferences
