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

import bpy, os

from bpy.types              import Operator
from mathutils              import Vector

from . properties           import Properties
from . execute_blender      import execute_blender, run_blend_fix_coll

class ImportBase:
    """
    Common functions to import different kinds of data.
    """

    def select_children(self, collection):
        """
        Recursively set selection to true on all objects of a collection 
        all all sub-collections.
        """
        [ o.select_set(True) for o in collection.objects ]
        [ select_children(c) for c in collection.children ]

    def append_objects(self, importFile, link=False, at_cursor=False, lock_xy=False):
        """
        Append objects from import file to scene.
        """
        if importFile.endswith(".fbx"):
            bpy.ops.import_scene.fbx(filepath=importFile)

        elif importFile.endswith(".blend"):
            # Import all objects.
            with bpy.data.libraries.load(importFile, link=link) as (data_from, data_to):
                data_to.objects = data_from.objects
                links = data_to.objects

            # Create new collection based on file name.
            collName = os.path.splitext(os.path.basename(importFile))[0].title()
            coll = bpy.data.collections.new(collName)

            # Append all objects to it.
            offset = bpy.context.scene.cursor.location if at_cursor else Vector((0, 0, 0))
            for l in links:
                coll.objects.link(l)

                # If object has been linked, make a proxy object
                # and continue with this new one.
                if link:
                    l = l.make_local()

                # Do this only, if not parented to another object!
                if l.parent == None:
                    l.location += offset
                    
                if lock_xy:
                    l.lock_location[2] = True
                    l.lock_rotation[0] = True
                    l.lock_rotation[1] = True

            # Append new collection to active collection.
            activeCol = bpy.context.collection
            activeCol.children.link(coll)        

            # Select all objects.
            self.select_children(coll)
            
    def link_collecttion(self, importFile, at_cursor=False, lock_xy=False, coll_is=False):
        """
        
        """
        if importFile.endswith(".fbx"):
            bpy.ops.import_scene.fbx(filepath=importFile)

        elif importFile.endswith(".blend"):
            with bpy.data.libraries.load(importFile, link=False) as (data_from, data_to):
                data_to.collections = data_from.collections
                
            offset = bpy.context.scene.cursor.location if at_cursor else Vector((0, 0, 0))

            if data_to.collections != None:
                for new_coll in data_to.collections:
                    instance = bpy.data.objects.new(new_coll.name, None)
                        
                    instance.instance_type = 'COLLECTION'
                    instance.instance_collection = new_coll
                    
                    if instance.parent == None:
                        instance.location += offset   
                    if lock_xy:
                        instance.lock_location[2] = True
                        instance.lock_rotation[0] = True
                        instance.lock_rotation[1] = True

                    #实例化集合对象
                    activeCol = bpy.context.collection
                    activeCol.objects.link(instance)
                    
                    #设置为激活对象
                    instance.select_set(True)
                    bpy.context.view_layer.objects.active = instance
            else:
                return None
            
    def fix_coll(self, importFile):
        if importFile.endswith(".fbx"):
            pass
            return True
        elif importFile.endswith(".blend"):
            run_blend_fix_coll(importFile)
            return False
    def append_materials(self, blendFile):
        """
        Import all materials from blend file and return list of names (with their new names).
        """
        if "::" in blendFile:
            filename, material = blendFile.split("::")
        else:
            filename, material = blendFile, ""

        with bpy.data.libraries.load(filename, link=False) as (data_from, data_to):
            if material == "" and len(data_from.materials) > 0:
                data_to.materials = [data_from.materials[0], ]
                return data_to.materials[0]
            elif len(material) > 0:
                for m in data_from.materials:
                    if m == material:
                        data_to.materials = [m, ]
                        return data_to.materials[0]

        return None

class FixCollectionOperator(Operator,ImportBase):
    bl_idname = "asset_wizard.fix_coll_op"
    bl_label = "Fix_Coll"
    bl_description = "Fix blend File Addon Into Collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        prop = Properties.get()

        fix_coll_bool = self.fix_coll(prop.iobj_previews)
        
        if fix_coll_bool ==True:
            self.report({'INFO'},"文件后缀为FBX无需修复")
            
        elif fix_coll_bool == False:
            self.report({'INFO'},"已执行修复")
        
        return {'FINISHED'}

class AppendObjectOperator(Operator, ImportBase):
    bl_idname = "asset_wizard.append_object_op"
    bl_label = "Append"
    bl_description = "Appends object to scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all objects.
        [ o.select_set(False) for o in context.scene.objects ]
        
        prop = Properties.get()
        self.append_objects(
            prop.iobj_previews, 
            False,
            prop.iobj_at_cursor,
            prop.iobj_lock_xy,
        )
        return{'FINISHED'}

class LinkCollectionOperator(Operator, ImportBase):
    bl_idname = "asset_wizard.link_coll_op"
    bl_label = "Link"
    bl_description = "Link collection to scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        [ o.select_set(False) for o in context.scene.objects ]
        
        prop = Properties.get()
    
        if self.link_collecttion(prop.iobj_previews,prop.iobj_at_cursor,prop.iobj_lock_xy) == None:
            self.report({'INFO'},"文件内没有集合")
        return{'FINISHED'}

class LinkObjectOperator(Operator, ImportBase):
    bl_idname = "asset_wizard.link_object_op"
    bl_label = "Link"
    bl_description = "Links object to scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all objects.
        [ o.select_set(False) for o in context.scene.objects ]
        
        prop = Properties.get()
        self.append_objects(
            prop.iobj_previews, 
            True,
            prop.iobj_at_cursor,
            prop.iobj_lock_xy
        )
        return{'FINISHED'}


class SetMaterialOperator(Operator, ImportBase):
    bl_idname = "asset_wizard.set_material_op"
    bl_label = "Set"
    bl_description = "Import material and apply to active objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        material = self.append_materials(Properties.get().imat_previews)

        # If we have at least one material imported, apply the first one to
        # all slots of selected objects. If no slot is available, create one.
        if material:
            m = bpy.data.materials[material]
            for o in context.selected_objects:
                if len(o.material_slots) < 1:
                    o.data.materials.append(m)
                else:
                    o.material_slots[o.active_material_index].material = m
        return{'FINISHED'}        


class AppendMaterialOperator(Operator, ImportBase):
    bl_idname = "asset_wizard.append_material_op"
    bl_label = "Append"
    bl_description = "Adds material to blendfile"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.append_materials(Properties.get().imat_previews)
        return{'FINISHED'}


class OpenObjectOperator(Operator):
    bl_idname = "asset_wizard.open_object_op"
    bl_label = "Open"
    bl_description = "Open the asset file"
    bl_options = {'REGISTER'}

    def execute(self, context):
        execute_blender([ Properties.get().iobj_previews, ])
        return{'FINISHED'}


class OpenMaterialOperator(Operator):
    bl_idname = "asset_wizard.open_material_op"
    bl_label = "Open"
    bl_description = "Open the asset file"
    bl_options = {'REGISTER'}

    def execute(self, context):
        execute_blender([ Properties.get().imat_previews, ])
        return{'FINISHED'}        
