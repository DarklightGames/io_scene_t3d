bl_info = {
    "name": "Unreal T3D Exporter",
    "author": "Colin Basnett",
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "location": "File > Export > Unreal T3D Export (.t3d)",
    "description": "Unreal T3D Export (.t3d)",
    "warning": "",
    "doc_url": "https://github.com/DarklightGames/io_scene_t3d",
    "tracker_url": "https://github.com/DarklightGames/io_scene_t3d/issues",
    "category": "Import-Export"
}

if 'bpy' in locals():
    import importlib

    importlib.reload(t3d_data)
    importlib.reload(t3d_builder)
    importlib.reload(t3d_exporter)
else:
    from . import data as t3d_data
    from . import builder as t3d_builder
    from . import exporter as t3d_exporter


import bpy

classes = (
    t3d_data.classes +
    t3d_exporter.classes +
    t3d_builder.classes
)


def t3d_export_menu_func(self, context):
    self.layout.operator(t3d_exporter.T3DExportOperator.bl_idname, text='Unreal T3D (.t3d)')


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(t3d_export_menu_func)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(t3d_export_menu_func)


if __name__ == '__main__':
    register()
