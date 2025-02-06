import bpy
import csv
import os

class BezierExporterBase:
    def export_bezier(self, spline, filepath):
        bezier_points = []

        for point in spline.bezier_points:
            bezier_points.append({
                'co': point.co,
                'handle_left': point.handle_left,
                'handle_right': point.handle_right
            })

        if bezier_points:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(["name", "px", "py", "pz", "hlx", "hly", "hlz", "hrx", "hry", "hrz"])

                count = 1
                for point in bezier_points:
                    writer.writerow([
                        count,
                        point['co'].x,
                        -point['co'].y,
                        point['co'].z,
                        point['handle_left'].x,
                        -point['handle_left'].y,
                        point['handle_left'].z,
                        point['handle_right'].x,
                        -point['handle_right'].y,
                        point['handle_right'].z
                    ])
                    count += 1
            return True
        else:
            return False