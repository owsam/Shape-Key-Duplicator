bl_info = {
    "name": "Shapekey Duplicator",
    "author": "Osamu Watanabe",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shapekey Tools",
    "description": "Duplicate a selected shape key from the active object",
    "category": "Object",
}

import bpy

class SKDProperties(bpy.types.PropertyGroup):
    key_enum: bpy.props.EnumProperty(
        name="Shape Key",
        description="Select a shapekey to duplicate",
        items=lambda self, context: [
            (key.name, key.name, "") 
            for key in context.object.data.shape_keys.key_blocks
            if key.name != "Basis"
        ] if context.object and context.object.data.shape_keys else []
    )

class OBJECT_OT_duplicate_shape_key(bpy.types.Operator):
    bl_idname = "object.duplicate_shape_key"
    bl_label = "Duplicate Shapekey"
    bl_description = "Duplicate the selected shape key"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        key_name = context.scene.skd_props.key_enum
        shape_keys = obj.data.shape_keys

        if not shape_keys:
            self.report({'WARNING'}, "No shapekeys found.")
            return {'CANCELLED'}

        source_key = shape_keys.key_blocks.get(key_name)
        if not source_key:
            self.report({'WARNING'}, f"Shapekey '{key_name}' not found.")
            return {'CANCELLED'}

        # Create a new shape key
        new_key = obj.shape_key_add(name=key_name + "_Copy", from_mix=False)
        for i, coord in enumerate(source_key.data):
            new_key.data[i].co = coord.co

        self.report({'INFO'}, f"Shapekey '{key_name}' duplicated.")
        return {'FINISHED'}

class OBJECT_PT_shape_key_tools(bpy.types.Panel):
    bl_label = "Shapekey Tools"
    bl_idname = "OBJECT_PT_shape_key_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shapekey Tools'

    def draw(self, context):
        layout = self.layout
        skd_props = context.scene.skd_props

        layout.prop(skd_props, "key_enum")
        layout.operator("object.duplicate_shape_key")

classes = (
    SKDProperties,
    OBJECT_OT_duplicate_shape_key,
    OBJECT_PT_shape_key_tools,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.skd_props = bpy.props.PointerProperty(type=SKDProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.skd_props

if __name__ == "__main__":
    register()

