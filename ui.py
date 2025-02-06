import bpy
from .exporters import BezierSingleExporter, BezierBatchExporter

def menu_func_export(self, context):
    layout = self.layout
    layout.operator(BezierSingleExporter.bl_idname, text="Export BezierCSV For UE4 (.csv)")
    layout.operator(BezierBatchExporter.bl_idname, text="Batch Export BezierCSV For UE4 (.csv)")