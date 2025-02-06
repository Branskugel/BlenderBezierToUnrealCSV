bl_info = {
    "name": "BezierCSV Exporter for UE4",
    "blender": (4, 3, 0),
    "author": "RYM",
    "description": "Export Bezier curves to CSV files for UE4, supporting single and batch export with customizable naming.",
    "location": "File > Export > BezierCSV For UE4 (.csv)",
    "category": "Import-Export",
}

import bpy
from .exporters import BezierSingleExporter, BezierBatchExporter
from .ui import menu_func_export

def register():
    bpy.utils.register_class(BezierSingleExporter)
    bpy.utils.register_class(BezierBatchExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(BezierBatchExporter)
    bpy.utils.unregister_class(BezierSingleExporter)

if __name__ == "__main__":
    register()