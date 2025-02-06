import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
import csv
import os
from .bezier_exporter_base import BezierExporterBase


class BezierSingleExporter(bpy.types.Operator, ExportHelper, BezierExporterBase):
    bl_idname = "export_bezier.single_beziercsv"
    bl_label = "Export BezierCSV For UE4"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        obj = context.active_object

        if obj and obj.type == 'CURVE':
            beziers = obj.data.splines
            if len(beziers) > 1:
                # Используем bpy.ops для вызова оператора батч-экспорта
                bpy.ops.export_bezier.batch_beziercsv('INVOKE_DEFAULT', filepath=self.filepath, naming_option='OBJECT_NAME')
                return {'FINISHED'}
            else:
                # Экспортируем как обычно
                if context.mode == 'EDIT_CURVE':
                    spline = obj.data.splines.active
                    if spline and spline.type == 'BEZIER':
                        success = self.export_bezier(spline, self.filepath)
                        if success:
                            self.report({'INFO'}, "The curve was exported")
                            return {'FINISHED'}
                        else:
                            self.report({'WARNING'}, "Selected spline isn't a Bezier curve")
                            return {'CANCELLED'}
                    else:
                        self.report({'WARNING'}, "No active Bezier spline selected")
                        return {'CANCELLED'}
                else:
                    success = self.export_bezier(obj.data.splines[0], self.filepath)
                    if success:
                        self.report({'INFO'}, "The curve was exported")
                        return {'FINISHED'}
                    else:
                        self.report({'WARNING'}, "Selected object isn't a Bezier curve")
                        return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "Selected object isn't a curve")
            return {'CANCELLED'}

class BezierBatchExporter(bpy.types.Operator, ExportHelper, BezierExporterBase):
    bl_idname = "export_bezier.batch_beziercsv"
    bl_label = "Batch Export BezierCSV For UE4"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )

    naming_option: EnumProperty(
        name="Naming Option",
        description="Choose naming option for exported files",
        items=[
            ('OBJECT_NAME', "Object Name", "Use object name as file name"),
            ('TEMPLATE', "Template with Number", "Use template with incremental number"),
        ],
        default='OBJECT_NAME',
    )

    template: StringProperty(
        name="Template",
        description="Template for file naming with incremental number",
        default="BezierCurve_###",
    )

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        selected_objects = context.selected_objects

        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        export_path = os.path.dirname(self.filepath)

        for obj in selected_objects:
            if obj.type == 'CURVE':
                self.process_splines(obj, export_path)
            else:
                self.report({'WARNING'}, f"Object '{obj.name}' is not a curve")
        self.report({'INFO'}, "Batch export completed")
        return {'FINISHED'}

    def process_splines(self, obj, export_path):
        beziers = obj.data.splines
        for i, spline in enumerate(beziers, start=1):
            if spline.type == 'BEZIER':
                if self.naming_option == 'OBJECT_NAME':
                    file_path = os.path.join(export_path, f"{obj.name}_curve_{i}.csv")
                elif self.naming_option == 'TEMPLATE':
                    file_name = self.template.replace('###', f"{i:03}")
                    file_path = os.path.join(export_path, f"{file_name}_{obj.name}.csv")
                success = self.export_bezier(spline, file_path)
                if not success:
                    self.report({'WARNING'}, f"Object '{obj.name}' export failed")
            else:
                self.report({'WARNING'}, f"Curve '{obj.name}' spline {i} is not a Bezier curve")