from typing import TextIO, Iterable

from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

from .builder import build_t3d
from .data import Map


class T3DExportOperator(Operator, ExportHelper):
    bl_idname = 'export.t3d'
    bl_label = 'Export'
    bl_options = {'INTERNAL', 'UNDO'}
    __doc__ = 'Export mesh(es) to T3D'
    filename_ext = '.t3d'
    filter_glob: StringProperty(default='*.t3d', options={'HIDDEN'})

    filepath: StringProperty(
        name='File Path',
        description='File path used for exporting the T3D file',
        maxlen=1024,
        default='')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    @classmethod
    def poll(cls, context):
        has_selected_meshes = any(map(lambda x: x.type == 'MESH', context.view_layer.objects.selected))
        if not has_selected_meshes:
            cls.poll_message_set('No meshes are selected')
            return False
        return True

    def draw(self, context):
        pass

    def execute(self, context):
        t3d = build_t3d(context)
        export_t3d(t3d, self.filepath)
        return {'FINISHED'}


class T3DWriter:
    def __init__(self, fp: TextIO):
        self.fp = fp
        self.indentation = 0

    def write_line(self, line: str):
        self.fp.write('    ' * self.indentation + line + '\n')
        return self

    def indent(self):
        self.indentation += 1
        return self

    def dedent(self):
        self.indentation -= 1
        return self


def format_vector(vector: Iterable[float]) -> str:
    return ','.join(map(lambda element: '%+013.6f' % element, vector))


def export_t3d(t3d: Map, path: str):
    with open(path, 'w') as fp:
        writer = T3DWriter(fp)
        writer.write_line('Begin Map')
        writer.indent()
        for actor in t3d.actors:
            writer.write_line(f'Begin Actor Class=Brush Name={actor.name}').indent()
            writer.write_line(f'Begin Brush Name={actor.brush.name}').indent()
            writer.write_line(f'Begin PolyList').indent()
            for polygon in actor.brush.polygons:
                writer.write_line(f'Begin Polygon Link={polygon.link}').indent()
                writer.write_line(f'{"Origin":8} {format_vector(polygon.origin)}')
                writer.write_line(f'{"Normal":8} {format_vector(polygon.normal)}')
                writer.write_line(f'{"TextureU":8} {format_vector(polygon.texture_u)}')
                writer.write_line(f'{"TextureV":8} {format_vector(polygon.texture_v)}')
                writer.write_line(f'{"Vertex":8} {format_vector(polygon.vertices[0])}')
                writer.write_line(f'{"Vertex":8} {format_vector(polygon.vertices[1])}')
                writer.write_line(f'{"Vertex":8} {format_vector(polygon.vertices[2])}')
                writer.dedent().write_line('End Polygon')
            writer.dedent().write_line('End PolyList')
            writer.dedent().write_line('End Brush')
            writer.write_line(f'Brush=Model\'myLevel.{actor.brush.name}\'')
            writer.dedent().write_line('End Actor')
        writer.dedent().write_line('End Map')
    pass


classes = (
    T3DExportOperator,
)
