import webbrowser # <= to open the POVRay help
from copy import deepcopy
import re
from .io import render_povstring

from .helpers import WIKIREF, vectorize, format_if_necessary

class Scene:
    """ A scene contains Items and can be written to a file.

    Examples
    ---------

    >>> scene = Scene( Camera('location', [1,1,1], 'look_at', [0,0,0]),
                       items=[light_source, myshpere, my_box],
                       included)

    """
    def __init__(self, camera, objects=[], atmospheric=[],
                 included=[], defaults=[], global_settings=[],
                 declares=[]):

        self.camera = camera
        self.objects = objects
        self.atmospheric = atmospheric
        self.included = included
        self.defaults = defaults
        self.declares = declares
        self.global_settings = global_settings

    def __str__(self):

        included = ['#include "%s"'%e for e in self.included]
        defaults = ['#default { %s }'%e for e in self.defaults]
        declares = ['#declare %s;'%e for e in self.declares]

        global_settings = ["global_settings{\n%s\n}"%("\n".join(
                           [str(e) for e in self.global_settings]))]
        return '\n'.join([str(e)
                          for l in  [included, declares, self.objects, [self.camera],
                              self.atmospheric, global_settings]
                          for e in l])

    def copy(self):
        return deepcopy(self)

    def set_camera(self, new_camera):
        new = self.copy()
        new.camera = new_camera
        return new

    def add_objects(self, objs):

        new = self.copy()
        new.objects +=  objs
        return new

    def render(self, outfile=None, height=None, width=None,
                     quality=None, antialiasing=None, remove_temp=True,
                     auto_camera_angle=True, show_window=False, tempfile=None,
                     includedirs=None, output_alpha=False):

        """ Renders the scene to a PNG, a numpy array, or the IPython Notebook.

        Parameters
        ------------

        outfile
          Name of the output:
          - "myfile.png" to output a PNG file
          - None to output a numpy array (if numpy is installed).
          - 'ipython' (and call this function last in an IPython Notebook)

        height
          height in pixels

        width
          width in pixels

        output_alpha
          If true, the background will be transparent,
        rather than the default black background.  Note
        that this option is ignored if rendering to a
        numpy array, due to limitations of the intermediate
        ppm format.

        """

        if auto_camera_angle and width is not None:
            self.camera = self.camera.add_args(['right', [1.0*width/height, 0,0]])

        return render_povstring(str(self), outfile, height, width,
                                quality, antialiasing, remove_temp, show_window,
                                tempfile, includedirs, output_alpha)


class POVRayElement:
    def __init__(self, *args):
        self.args = list(args)

    def copy(self):
        return deepcopy(self)

    @classmethod
    def transformed_name(cls):
        """ Tranform Sphere=>sphere, and LightSource=>light_source """
        return re.sub(r'(?!^)([A-Z])', r'_\1', cls.__name__)

    @classmethod
    def help(cls):
        webbrowser.open(WIKIREF + cls.transformed_name())

    def add_args(self, new_args):
        new = self.copy()
        new.args += new_args
        return new

    def __str__(self):
        # Tranforms Sphere=>sphere, and LightSource=>light_source
        name = self.transformed_name().lower()

        return "%s {\n%s \n}" % (name, "\n".join([str(format_if_necessary(e))
                                                  for e in self.args]))


class POVRayMap(POVRayElement):
    def __str__(self):
        name = self.transformed_name().lower()
        return "%s { %s }"%(name,
                            "\n".join([ "[ %s ]"%(" ".join(
                                [str(format_if_necessary(e)) for e in l]))
                                        for l in self.args]))


# =============================================================================


class Background(POVRayElement):
    """ Background element. Background(color, *a)."""

class Box(POVRayElement):
    """ Box element. Box(corner1_xyz, corner2_xyz, *a) """

class ColorMap(POVRayMap):
    """ ColorMap( [0, color1], [.5, color2], [0.8, color3], [1, color4]) """

class Cone(POVRayElement):
    """ Cone( )"""

class Camera(POVRayElement):
    """ Camera([type,]  'location', [x,y,z], 'look_at', [x,y,z]) """

class Cylinder(POVRayElement):
    """ Cylinder([type,]  'location', [x,y,z], 'look_at', [x,y,z]) """

class Difference(POVRayElement):
    """ Difference(object1, object2, *a) """

class Finish(POVRayElement):
    """ Finish('phong', 1, 'brilliance', 0.9, 'ambient', 0.5) """

class Fog(POVRayElement):
    """ Fog('fog_type',   2, 'distance', 20, 'color',     [1.00,0.98,0.9],
          'fog_offset', 0.1, 'fog_alt', 1, 'turbulence', 1.8) """

class ImageMap(POVRayElement):
    """ ImageMap('my_image.png') """
    povray_name= 'image_map'
    url = WIKIREF+'Image_Map'

class Interior(POVRayElement):
    """ Interior('I_Glass3') """

class Intersection(POVRayElement):
    """ Intersection(obj1, obj2, *a) """

class LightSource(POVRayElement):
    """ LightSource( location_xyz, [light_type], 'color', [r,g,b],
                     'point_at', [x,y,z])) """

class Macro(POVRayElement):
    """ This special class enables to use macros like
    Tetrahedron_by_Corners(P,Q,R,S, R1, R2, filled), with the syntax
    Macro('Tetrahedron_by_Corners', P,Q,R,S,R1,R2, filled)
    """

    def __str__(self):
        return "%s( %s)"%(self.args[0], " , ".join([str(format_if_necessary(e))
                                                   for e in self.args[1:]]))

class Merge(POVRayElement):
    """ Merge(object1, object2, *a) """


class Normal(POVRayElement):
    """ Normal()s"""

class NormalMap(POVRayMap):
    """ NormalMap( [0, normal1], [.5, normal2], [0.8, normal3], [1, normal4]) """

class Pigment(POVRayElement):
    """ Pigment(color_xyz) """

class PigmentMap(POVRayMap):
    """ PigmentMap( [0, pigment1], [.5, pigment2], [0.8, pigment3], [1, pigment4]) """

class Plane(POVRayElement):
    """ Plane(normal_xyz, distance, *a) """

class Polygon(POVRayElement):
    """ Polygon(nsides, vertice_xy1, vertice_xy2, ...) """

class Object(POVRayElement):
    """ Object(some_povrayelement, 'translate', [x,y,z] ) """


class Radiosity(POVRayElement):
    """ Radiosity(...)
    (put in global settings)"""

class SlopeMap(POVRayMap):
    """ SlopeMap( [0, slope1], [.5, slope2], [0.8, slope3], [1, slope4]) """

class SkySphere(POVRayElement):
    """ SkySphere( Pigment(color_rgb) ) """

class Sphere(POVRayElement):
    """ Sphere(location_xyz, radius, *a) """

class Text(POVRayElement):
    """  Text('ttf', 'Hello', 'crystall.ttf', 1,0) """

class Texture(POVRayElement):
    """ Texture ( Pigment(color_rgb), 'phong', 0.1, 'reflection', 0.5) """

class TextureMap(POVRayMap):
    """ TextureMap( [0, texture1], [.5, texture2], [0.8, texture3], [1, texture4]) """

class Triangle(POVRayElement):
    """ Triangle() """

class Union(POVRayElement):
    """ Union(obj1, obj2, obj3, *a) """

class Blob(POVRayElement):
    """ Blob(blob_item1, blob_item2, ...) """

class Prism(POVRayElement):
    """ Prism('linear_spline', 'linear_sweep', Height_1, Height_2, Number_Of_Points, ...) """

class VertexVectors(POVRayElement):
    """ VertexVectors()"""

class NormalVectors(POVRayElement):
    """ NormalVectors()"""

class FaceIndices(POVRayElement):
    """ FaceIndices()"""

class Mesh2(POVRayElement):
    """ Mesh2()"""

class Media(POVRayElement):
    """ Media()"""

