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

class Macro(POVRayElement):
    """ This special class enables to use macros like
    Tetrahedron_by_Corners(P,Q,R,S, R1, R2, filled), with the syntax
    Macro('Tetrahedron_by_Corners', P,Q,R,S,R1,R2, filled)
    """

    def __str__(self):
        return "%s( %s)"%(self.args[0], " , ".join([str(format_if_necessary(e))
                                                   for e in self.args[1:]]))

# =============================================================================
# =============================================================================
# ======= Included classes In the order they appear in POV help files =========
# =============================================================================
# =============================================================================

class Spline(POVRayElement):
    """Spline(
             *[SPLINE_IDENTIFIER] |
             *[SPLINE_TYPE] |
             *[Val_1, [Point_1],
             Val_2, [Point_2],
             ...
             Val_n, [Point_n]]
             )
       SPLINE_TYPE:
         linear_spline | quadratic_spline | cubic_spline | natural_spline
       SPLINE_USAGE:
         MySpline(Val) | MySpline(Val, SPLINE_TYPE)
    """

class Camera(POVRayElement):
    """Camera( *[CAMERA_ITEMS...] )
       CAMERA_ITEMS:
         CAMERA_TYPE | CAMERA_VECTOR | CAMERA_MODIFIER |
         CAMERA_IDENTIFIER
       CAMERA_TYPE:
         'perspective'  | 'orthographic'  | MeshCamera(MESHCAM_MODIFIERS) |
         'fisheye'  | 'ultra_wide_angle'  | 'omnimax'  | 'panoramic'  | 
         'cylinder', CylinderType | 'spherical'
       CAMERA_VECTOR:
         'location', [Location] | 'right', [Right] | 'up', [Up] |
         'direction', [Direction] | 'sky', [Sky]
       CAMERA_MODIFIER:
         'angle', HORIZONTAL,  *[VERTICAL] | 'look_at', [Look_At] |
         'blur_samples' ,  *[MIN_SAMPLES,] MAX_SAMPLES | 'aperture', Size |
         'focal_point', [Point] | 'confidence', Blur_Confidence |
         'variance', Blur_Variance | *[Bokeh(Pigment(BOKEH))] |
         NORMAL | TRANSFORMATION | *[MESHCAM_SMOOTH]
       MESHCAM_MODIFIERS:
         'rays', 'per'  'pixel'  & 'distribution', 'type'  & 
         *['max', 'distance' ] & MESH_OBJECT & *[MESH_OBJECT...]
       BOKEH:
         'a', COLOR_VECTOR 'in', 'the'  'range', 'of'  [0,0,0] ... [1,1,0]
       MESHCAM_SMOOTH:
         'optional', 'smooth'  'modifier', 'valid'  'only', 
         'when'  'using', 'mesh_camera' """


class Bokeh(POVRayElement):
    """Bokeh( Pigment() )
    """


class Background(POVRayElement):
  """Background(COLOR)"""


class Fog(POVRayElement):
    """Fog( *[FOG_IDENTIFIER],  *[FOG_ITEMS...] )
       FOG_ITEMS:
         'fog_type', Fog_Type | 'distance', Distance | COLOR |
         'turbulence', [Turbulence] | 'turb_depth', Turb_Depth |
         'omega', Omega | 'lambda', Lambda | 'octaves', Octaves |
         'fog_offset', Fog_Offset | 'fog_alt', Fog_Alt |
         'up', [Fog_Up] | TRANSFORMATION"""


class SkySphere(POVRayElement):
    """SkySphere( *[SKY_SPHERE_IDENTIFIER],  *[SKY_SPHERE_ITEMS...] )
       SKY_SPHERE_ITEM:
         PIGMENT | TRANSFORMATION | *[emission]"""


class Rainbow(POVRayElement):
    """Rainbow( *[RAINBOW_IDENTIFIER],  *[RAINBOW_ITEMS...] )
       RAINBOW_ITEM:
         'direction', [Dir] | 'angle', Angle | 'width', Width |
         'distance', Distance | COLOR_MAP | 'jitter', Jitter | 'up', [Up] |
         'arc_angle', Arc_Angle | 'falloff_angle', Falloff_Angle"""


class LightSource(POVRayElement):
    """LightSource(
           [Location], COLOR
           *[LIGHT_MODIFIERS...]
           )
       LIGHT_MODIFIER:
         LIGHT_TYPE | SPOTLIGHT_ITEM | AREA_LIGHT_ITEMS |
         GENERAL_LIGHT_MODIFIERS
       LIGHT_TYPE:
         'spotlight'  | 'shadowless'  | 'cylinder'  | 'parallel'
       SPOTLIGHT_ITEM:
         'radius', Radius | 'falloff', Falloff | 'tightness', Tightness |
         'point_at', [Spot]
       PARALLEL_ITEM:
         'point_at', [Spot]
       AREA_LIGHT_ITEM:
         'area_light', [Axis_1], [Axis_2], Size_1, Size_2 |
         'adaptive', Adaptive | 'area_illumination' ,  *[Bool] |
         'jitter'  | 'circular'  | 'orient'
       GENERAL_LIGHT_MODIFIERS:
         LooksLike( OBJECT ) |
         'TRANSFORMATION', 'fade_distance'  Fade_Distance |
         'fade_power', Fade_Power | 'media_attenuation' ,  *[Bool] |
         'media_interaction' ,  *[Bool] | 'projected_through' """


class LooksLike(POVRayElement):
    """LooksLike(Object())
    """


class ProjectedThrough(POVRayElement):
    """ProjectedThrough(Object())
    """


class LightGroup(POVRayElement):
    """"LightGroup(
         LIGHT_GROUP LIGHT  |
         LIGHT_GROUP OBJECT |
         LIGHT_GROUP
         *[LIGHT_GROUP MODIFIER]
         )
       LIGHT_GROUP LIGHT:
         light_source | light_source IDENTIFIER
       LIGHT_GROUP OBJECT:
         OBJECT | OBJECT IDENTIFIER
       LIGHT_GROUP MODIFIER:
         global_lights BOOL | TRANSFORMATION"
    """


class Radiosity(POVRayElement):
    """Radiosity(*[Radiosity Items])
    """


class Photons(POVRayElement):
    """"Photons(
         spacing <photon_spacing> | count <photons_to_shoot>
         *[gather <min_gather>, <max_gather>]
         *[media <max_steps> *[,<factor>]]
         *[jitter <jitter_amount>]
         *[max_trace_level <photon_trace_level>]
         *[adc_bailout <photon_adc_bailout>]
         *[save_file \"filename\" | load_file \"filename\"]
         *[autostop <autostop_fraction>]
         *[expand_thresholds <percent_increase>, <expand_min>]
         *[radius <gather_radius>, <multiplier>, <media>,<multiplier>]
         )"
    """


class Object(POVRayElement):
    """Object()
    """


class Blob(POVRayElement):
    """Blob( BLOB_ITEM... *[BLOB_MODIFIERS...])
       BLOB_ITEM:
         Sphere([Center], Radius,
           *[ 'strength', ] Strength  *[COMPONENT_MODIFIER...] ) |
         Cylinder([End1], [End2], Radius,
           *[ 'strength', ] Strength,  *[COMPONENT_MODIFIER...] ) |
         'component', Strength, Radius, [Center] |
         'threshold', Amount
       COMPONENT_MODIFIER:
         TEXTURE | PIGMENT | NORMAL | FINISH | TRANSFORMATION
       BLOB_MODIFIER:
         'hierarchy' ,  *[Boolean] | 'sturm' ,  *[Boolean] | OBJECT_MODIFIER"""


class Parametric(POVRayElement):
    """"Parametric(
         Function( FUNCTION_ITEMS ),
         Function( FUNCTION_ITEMS ),
         Function( FUNCTION_ITEMS )

         [u1,v1], [u2,v2]
         *[ContainedBy( SPHERE | BOX )]
         *[max_gradient FLOAT_VALUE]
         *[accuracy FLOAT_VALUE]
         *[precompute DEPTH, VarList]
         )"
    """


class Prism(POVRayElement):
    """Prism(
           *[PRISM_ITEMS...] Height_1, Height_2, Number_Of_Points,
           [Point_1], [Point_2], ... [Point_n]
           *[ 'open', ],  *[PRISM_MODIFIERS...]
           )
       PRISM_ITEM:
         'linear_spline'  | 'quadratic_spline'  | 'cubic_spline'  |
         'bezier_spline'  | 'linear_sweep'  | 'conic_sweep'
       PRISM_MODIFIER:
         'sturm'  | OBJECT_MODIFIER"""


class Sphere(POVRayElement):
    """Sphere(
           [Center], Radius
           *[OBJECT_MODIFIERS...]
           )"""


class SphereSweep(POVRayElement):
    """SphereSweep(
           'linear_spline'  | 'b_spline'  | 'cubic_spline'
           NUM_OF_SPHERES,
           CENTER, RADIUS,
           CENTER, RADIUS,
           ...
           CENTER, RADIUS
           *['tolerance', DEPTH_TOLERANCE]
           *[OBJECT_MODIFIERS]
           )"""


class Superellipsoid(POVRayElement):
    """Superellipsoid(
           [Value_E, Value_N]
           *[OBJECT_MODIFIERS...]
           )"""


class Sor(POVRayElement):
    """Sor(
           Number_Of_Points, [Point_1], [Point_2], ... [Point_n]
           *[ 'open', ],  *[SOR_MODIFIERS...]
           )
       SOR_MODIFIER:
         'sturm'  | OBJECT_MODIFIER"""


class Text(POVRayElement):
    """Text(
           'ttf'  'fontname.ttf/ttc' 'String_of_Text'
           Thickness, [Offset]
           *[OBJECT_MODIFIERS...]
           )"""


class Torus(POVRayElement):
    """Torus(
           Major, Minor
           *[TORUS_MODIFIER...]
           )
       TORUS_MODIFIER:
         'sturm'  | OBJECT_MODIFIER"""


class Box(POVRayElement):
    """Box(
           [Corner_1], [Corner_2]
           *[OBJECT_MODIFIERS...]
           )"""


class Cone(POVRayElement):
    """Cone(
           [Base_Point], Base_Radius, [Cap_Point], Cap_Radius
           *[ 'open', ]*[OBJECT_MODIFIERS...]
           )"""


class Cylinder(POVRayElement):
    """Cylinder(
           [Base_Point], [Cap_Point], Radius
           *[ 'open', ]*[OBJECT_MODIFIERS...]
           )"""


class HeightField(POVRayElement):
    """HeightField(
           *[HF_TYPE] 'filename' *['gamma', GAMMA],  *['premultiplied', BOOL] |
           *[HF_FUNCTION]
           *[HF_MODIFIER...]
           *[OBJECT_MODIFIER...]
           )
       HF_TYPE:
         'exr'  | 'gif'  | 'hdr'  | 'iff'  | 'jpeg'  | 'pgm'  | 'png'  | 
         'pot'  | 'ppm'  | 'sys'  | 'tga'  | 'tiff'
       HF_FUNCTION:
         'function', FieldResolution_X, FieldResolutionY(UserDefined_Function)
       HF_MODIFIER:
         'smooth'  & 'water_level', Level
       OBJECT_MODIFIER:
         'hierarchy' ,  *[Boolean]"""



class Isosurface(POVRayElement):
    """Isosurface(
         Function( FUNCTION_ITEMS )
         *[ContainedBy( SPHERE | BOX )]
         *['threshold', FLOAT_VALUE]
         *['accuracy', FLOAT_VALUE]
         *['max_gradient', FLOAT_VALUE]
         *['evaluate', P0, P1, P2]
         *[open]
         *['max_trace', INTEGER] | *[all_intersections]
         *[OBJECT_MODIFIERS...]
         )"""



class ContainedBy(POVRayElement):
    """"ContainedBy( Object() )"
    """



class JuliaFractal(POVRayElement):
    """JuliaFractal(
           [4D_Julia_Parameter]
           *[JF_ITEM...],  *[OBJECT_MODIFIER...]
           )
       JF_ITEM:
         ALGEBRA_TYPE | FUNCTION_TYPE | 'max_iteration', Count |
         'precision', Amt | 'slice', [4D_Normal], Distance
       ALGEBRA_TYPE:
         'quaternion'  | 'hypercomplex'
       FUNCTION_TYPE:
         QUATERNATION:
           'sqr'  | 'cube'
         HYPERCOMPLEX:
           'sqr'  | 'cube'  | 'exp'  | 'reciprocal'  | 'sin'  | 'asin'  |
           'sinh'  |           'asinh'  | 'cos'  | 'acos'  | 'cosh'  | 
           'acosh'  | 'tan'  | 'atan'  |tanh | 'atanh'  | 'ln'  | 
           Pwr( X_Val, Y_Val )"""


class Lathe(POVRayElement):
    """Lathe(
           *[SPLINE_TYPE] Number_Of_Points, [Point_1]
           [Point_2]... [Point_n]
           *[LATHE_MODIFIER...]
           )
       SPLINE_TYPE:
         'linear_spline'  | 'quadratic_spline'  |
         'cubic_spline'  | 'bezier_spline'
       LATHE_MODIFIER:
         'sturm'  | OBJECT_MODIFIER"""


class Ovus(POVRayElement):
    """Ovus(
           Bottom_radius, Top_radius
           *[OBJECT_MODIFIERS...]
           )"""


class BicubicPatch(POVRayElement):
    """BicubicPatch(
           PATCH_ITEMS...
           [Point_1],[Point_2],[Point_3],[Point_4],
           [Point_5],[Point_6],[Point_7],[Point_8],
           [Point_9],[Point_10],[Point_11],[Point_12],
           [Point_13],[Point_14],[Point_15],[Point_16]
           *[OBJECT_MODIFIERS...]
           )
       PATCH_ITEMS:
         'type', Patch_Type | 'u_steps', Num_U_Steps | 'v_steps', Num_V_Steps |
         'flatness', Flatness"""


class Disc(POVRayElement):
    """Disc(
           [Center], [Normal], Radius,  *[, Hole_Radius]
           *[OBJECT_MODIFIERS...]
           )"""


class Mesh(POVRayElement):
    """Mesh(
           MESH_TRIANGLE...
           *[MESH_MODIFIER...]
           )
       MESH_TRIANGLE:
         Triangle(
           [Corner_1], [Corner_2], [Corner_3]
           *['uv_vectors', [uv_Corner_1], [uv_Corner_2], [uv_Corner_3]]
           *[MESH_TEXTURE]
           ) |
         SmoothTriangle(
           [Corner_1], [Normal_1],
           [Corner_2], [Normal_2],
           [Corner_3], [Normal_3]
           *['uv_vectors', [uv_Corner_1], [uv_Corner_2], [uv_Corner_3]]
           *[MESH_TEXTURE]
           )
       MESH_TEXTURE:
         Texture( TEXTURE_IDENTIFIER )
         TextureList(
           'TEXTURE_IDENTIFIER', TEXTURE_IDENTIFIER TEXTURE_IDENTIFIER
           )
       MESH_MODIFIER:
         'inside_vector', [direction] | 'hierarchy' ,  *[ 'Boolean', ] |
         OBJECT_MODIFIER"""



class Mesh2(POVRayElement):
    """"MESH2 :
         Mesh2(
           VECTORS...
           LISTS...   |
           INDICES... |
           MESH_MODIFIERS
           )
       VECTORS :
         VertexVectors(
         number_of_vertices,
         [vertex1], [vertex2], ...
         )|
         NormalVectors(
           number_of_normals,
           [normal1], [normal2], ...
           )|
         UvVectors(
           number_of_uv_vectors,
           [uv_vect1], [uv_vect2], ...
           )
       LISTS :
         TextureList(
           number_of_textures,
           Texture( Texture1 ),
           Texture( Texture2 ), ...
           )|
       INDICES :
         FaceIndices(
           number_of_faces,
             [index_a, index_b, index_c] *[,texture_index *[,
           texture_index, texture_index]],
             [index_d, index_e, index_f] *[,texture_index *[,
             texture_index, texture_index]],
             ...
             )|
         NormalIndices(
           number_of_faces,
             [index_a, index_b, index_c],
             [index_d, index_e, index_f],
             ...
             )|
         UvIndices(
           number_of_faces,
             [index_a, index_b, index_c],
             [index_d, index_e, index_f],
             ...
             )
       MESH_MODIFIER :
         inside_vector [direction] | OBJECT_MODIFIERS"
    """

class FaceIndices(POVRayElement):
    """FaceIndices(
         number_of_faces,
         [index_a, index_b, index_c],
         [index_d, index_e, index_f],
         ...
         )
    """


class NormalIndices(POVRayElement):
    """
    """


class NormalVectors(POVRayElement):
    """
    """


class UvIndices(POVRayElement):
    """
    """


class VertexVectors(POVRayElement):
    """
    """


class Polygon(POVRayElement):
    """Polygon(
           Number_Of_Points, [Point_1] [Point_2]... [Point_n]
           *[OBJECT_MODIFIER...]
           )"""


class Triangle(POVRayElement):
    """Triangle(
         [Corner_1],
         [Corner_2],
         [Corner_3]
         *[MESH_TEXTURE]
         )   |
       SmoothTriangle(
         [Corner_1], [Normal_1],
         [Corner_2], [Normal_2],
         [Corner_3], [Normal_3]
         *[MESH_TEXTURE]
         )
       MESH_TEXTURE:
         Texture( TEXTURE_IDENTIFIER ) |
         TextureList(
           'TEXTURE_IDENTIFIER', TEXTURE_IDENTIFIER TEXTURE_IDENTIFIER
           )"""


class SmoothTriangle(POVRayElement):
    """SmoothTriangle(
         [Corner_1], [Normal_1], [Corner_2],
         [Normal_2], [Corner_3], [Normal_3]
         *[OBJECT_MODIFIER...]
         )"""


class Plane(POVRayElement):
    """Plane(
           [Normal], Distance
           *[OBJECT_MODIFIERS...]
           )"""


class Poly(POVRayElement):
    """Poly(
           Order, [A1, A2, A3,... An]
           *[POLY_MODIFIERS...]
           )
       POLY_MODIFIERS:
         'sturm'  | OBJECT_MODIFIER"""


class Cubic(POVRayElement):
    """Cubic(
           [A1, A2, A3,... A20]
           *[POLY_MODIFIERS...]
           )"""


class Quartic(POVRayElement):
    """Quartic(
           [A1, A2, A3,... A35]
           *[POLY_MODIFIERS...]
           )"""


class Polynomial(POVRayElement):
    """Polynomial(
           Order, *[COEFFICIENTS...]
           *[POLY_MODIFIERS...]
           )
       COEFFICIENTS:
         Xyz([x_power],[y_power],[z_power]):[value]*[,]
       POLY_MODIFIERS:
         'sturm'  | OBJECT_MODIFIER"""


class Quadric(POVRayElement):
    """Quadric(
           [A,B,C],[D,E,F],[G,H,I],J
           *[OBJECT_MODIFIERS...]
           )"""


class Union(POVRayElement):
    """Union(
           OBJECTS...
           *[OBJECT_MODIFIERS...]
           )"""


class Intersection(POVRayElement):
    """Intersection(
           SOLID_OBJECTS...
           *[OBJECT_MODIFIERS...]
           )"""


class Difference(POVRayElement):
    """Difference(
           SOLID_OBJECTS...
           *[OBJECT_MODIFIERS...]
           )"""


class Merge(POVRayElement):
    """Merge(
           SOLID_OBJECTS...
           *[OBJECT_MODIFIERS...]
           )"""


class ClippedBy(POVRayElement):
    """ClippedBy( UNTEXTURED_SOLID_OBJECT... ) |
         ClippedBy( 'bounded_by'  )                 |
         BoundedBy( UNTEXTURED_SOLID_OBJECT... ) |
         BoundedBy( 'clipped_by'  )                 |
         'no_shadow'                   |
         'no_image' ,  *[ 'Bool', ]          |
         'no_radiosity' ,  *[ 'Bool', ]      |
         'no_reflection' ,  *[ 'Bool', ]     |
         'inverse'                     |
         'sturm' ,  *[ 'Bool', ]             |
         'hierarchy' ,  *[ 'Bool', ]         |
         'double_illuminate' ,  *[ 'Bool', ] |
         'hollow' ,   *[ 'Bool', ]           |
         Interior( INTERIOR_ITEMS... )                        |
         Material( *[MATERIAL_IDENTIFIER]*[MATERIAL_ITEMS...] ) |
         Texture( TEXTURE_BODY )   |
         InteriorTexture( TEXTURE_BODY ) |
         Pigment( PIGMENT_BODY )   |
         Normal( NORMAL_BODY )     |
         Finish( FINISH_ITEMS... ) |
         Photons( PHOTON_ITEMS...)
         Radiosity( RADIOSITY_ITEMS...)
         TRANSFORMATION"""


class BoundedBy(POVRayElement):
    """BoundedBy( UNTEXTURED_SOLID_OBJECT... ) |
         BoundedBy( 'clipped_by'  )"""


class Material(POVRayElement):
    """Material( *[MATERIAL_IDENTIFIER]*[MATERIAL_ITEMS...] )
       MATERIAL_ITEMS:
         TEXTURE | INTERIOR_TEXTURE | INTERIOR | TRANSFORMATIONS"""


class Texture(POVRayElement):
    """Texture(
           *[PATTERNED_TEXTURE_ID]
           *[TRANSFORMATIONS...]
           ) |
         Texture(
           PATTERN_TYPE
           *[TEXTURE_PATTERN_MODIFIERS...]
           ) |
         Texture(
           'tiles', TEXTURE 'tile2', TEXTURE
           *[TRANSFORMATIONS...]
           ) |
         Texture(
           MaterialMap(
             BITMAP_TYPE 'bitmap.ext'
             *[BITMAP_MODS...] TEXTURE... *[TRANSFORMATIONS...]
             )
           )
       TEXTURE_PATTERN_MODIFIER:
         PATTERN_MODIFIER | TEXTURE_LIST |
         TextureMap(
           TEXTURE_MAP_BODY
           )"""


class Pigment(POVRayElement):
    """Pigment(
           ImageMap(
             *[BITMAP_TYPE] 'bitmap*[.ext]' *['gamma', GAMMA],  
             *['premultiplied', BOOL]
             *[IMAGE_MAP_MODS...]
             )
         *[PIGMENT_MODFIERS...]
         )
        IMAGE_MAP:
         Pigment(
          ImageMap(
            FUNCTION_IMAGE
            )
         *[PIGMENT_MODFIERS...]
         )
        BITMAP_TYPE:
          'exr'  | 'gif'  | 'hdr'  | 'iff'  | 'jpeg'  | 'pgm'  | 'png'  | 'ppm'
          'sys'  | 'tga'  | 'tiff'
        IMAGE_MAP_MODS:
          'map_type', Type | 'once'  | 'interpolate', Type |
          'filter', Palette, Amount | 'filter', 'all'  Amount |
          'transmit', Palette, Amount | 'transmit', 'all'  Amount
        FUNCTION_IMAGE:
          'function', I_WIDTH, IHEIGHT( FUNCTION_IMAGE_BODY )
        FUNCTION_IMAGE_BODY:
          PIGMENT | FN_FLOAT | Pattern( PATTERN,  *[PATTERN_MODIFIERS] ) """


class ColorMap(POVRayMap):
    """ColorMap( COLOR_MAP_BODY ) | ColourMap( COLOR_MAP_BODY )
       COLOR_MAP_BODY:
         COLOR_MAP_IDENTIFIER | COLOR_MAP_ENTRY...
       COLOR_MAP_ENTRY:
         *[ 'Value', COLOR ] |
         *[ Value_1, 'Value_2', 'color'  'COLOR_1', 'color'  'COLOR_2', ]"""


class ColourMap(POVRayMap):
    """
    """


class PigmentMap(POVRayMap):
    """PigmentMap( PIGMENT_MAP_BODY )
       PIGMENT_MAP_BODY:
         PIGMENT_MAP_IDENTIFIER | PIGMENT_MAP_ENTRY...
       PIGMENT_MAP_ENTRY:
         *[ 'Value', PIGMENT_BODY ]"""


class Normal(POVRayElement):
    """Normal(
           BumpMap(
             BITMAP_TYPE 'bitmap.ext' *['gamma', GAMMA],  
             *['premultiplied', BOOL], *[BUMP_MAP_MODS...]
             )
         *[NORMAL_MODFIERS...]
         )
       BITMAP_TYPE:
         'exr'  | 'gif'  | 'hdr'  | 'iff'  | 'jpeg'  | 'pgm'  | 'png'  | 'ppm'
         'sys'  | 'tga'  | 'tiff'
       BUMP_MAP_MOD:
         'map_type', Type | 'once'  | 'interpolate', Type | 'use_color'  |
         'use_colour'  | 'bump_size', Value"""


class NormalMap(POVRayMap):
    """NormalMap( NORMAL_MAP_BODY )
       NORMAL_MAP_BODY:
         NORMAL_MAP_IDENTIFIER | NORMAL_MAP_ENTRY...
       NORMAL_MAP_ENTRY:
         *[ 'Value', NORMAL_BODY ]"""


class SlopeMap(POVRayMap):
    """SlopeMap( SLOPE_MAP_BODY )
       SLOPE_MAP_BODY:
         SLOPE_MAP_IDENTIFIER | SLOPE_MAP_ENTRY...
       SLOPE_MAP_ENTRY:
         *[ Value, [Height, Slope] ]"""


class BumpMap(POVRayElement):
    """BUMP_MAP:
         Normal(
           BumpMap(
             BITMAP_TYPE "bitmap.ext" *[gamma GAMMA] *[premultiplied BOOL]
             *[BUMP_MAP_MODS...]
             )
         *[NORMAL_MODFIERS...]
         )
       BITMAP_TYPE:
         exr | gif | hdr | iff | jpeg | pgm | png | ppm | sys | tga | tiff
       BUMP_MAP_MOD:
         map_type Type | once | interpolate Type | use_color |
         use_colour | bump_size Value
    """


class Finish(POVRayElement):
    """Finish( *[FINISH_IDENTIFIER],  *[FINISH_ITEMS...] )
       FINISH_ITEMS:
         'ambient', COLOR | 'diffuse' ,  *[albedo] Amount,  *[, Amount] |
         'emission', COLOR | 'brilliance', Amount | 'phong' ,  *[albedo] Amount
         'phong_size', Amount | 'specular' ,  *[albedo] Amount |
         'roughness', Amount | 'metallic' ,  *[Amount] | 'reflection', COLOR |
         'crand', Amount | 'conserve_energy', BOOL_ON_OFF |
         Reflection( Color_Reflecting_Min,  *[REFLECTION_ITEMS...] ) |
         Subsurface( 'translucency', COLOR ) |
         Irid( Irid_Amount,  *[IRID_ITEMS...] )
       REFLECTION_ITEMS:
         COLOR_REFLECTION_MAX | 'fresnel', BOOL_ON_OFF |
         'falloff', FLOAT_FALLOFF | 'exponent', FLOAT_EXPONENT |
         'metallic', FLOAT_METALLIC
       IRID_ITEMS:
         'thickness', Amount | 'turbulence', Amount"""


class Subsurface(POVRayElement):
    """ Subsurface( translucency COLOR ) |
        Subsurface( samples INT, INT )|
        Subsurface( radiosity BOOL )"
    """


class Reflection(POVRayElement):
    """Reflection(
           *[COLOR_REFLECTION_MIN,] COLOR_REFLECTION_MAX
           *[fresnel BOOL_ON_OFF]
           *[falloff FLOAT_FALLOFF]
           *[exponent FLOAT_EXPONENT]
           *[metallic FLOAT_METALLIC]
           )
    """


class Irid(POVRayElement):
    """Irid( Irid_Amount,  *[IRID_ITEMS...] )
       IRID_ITEMS:
         'thickness', Amount | 'turbulence', Amount"""


class TextureList(POVRayElement):
    """Texture(
           *[PATTERNED_TEXTURE_ID]
           *[TRANSFORMATIONS...]
           ) |
         Texture(
           PATTERN_TYPE
           *[TEXTURE_PATTERN_MODIFIERS...]
           ) |
         Texture(
           tiles TEXTURE tile2 TEXTURE
           *[TRANSFORMATIONS...]
           ) |
         Texture(
           MaterialMap(
             BITMAP_TYPE "bitmap.ext"
             *[BITMAP_MODS...] TEXTURE... *[TRANSFORMATIONS...]
             )
           )
       TEXTURE_PATTERN_MODIFIER:
         PATTERN_MODIFIER | TEXTURE_LIST |
         TextureMap(
           TEXTURE_MAP_BODY
           )
    """


class TextureMap(POVRayMap):
    """TextureMap( TEXTURE_MAP_BODY )
       TEXTURE_MAP_BODY:
         TEXTURE_MAP_IDENTIFIER | TEXTURE_MAP_ENTRY...
       TEXTURE_MAP_ENTRY:
         *[ 'Value', TEXTURE_BODY ]"""


class MaterialMap(POVRayElement):
    """"MATERIAL_MAP:
         Texture(
           MaterialMap(
             BITMAP_TYPE \"bitmap.ext\"
             *[BITMAP_MODS...] TEXTURE... *[TRANSFORMATIONS...]
             )
           )
       BITMAP_TYPE:
         exr | gif | hdr | iff | jpeg | pgm | png | ppm | sys | tga | tiff
       BITMAP_MOD:
         map_type Type | once | interpolate Type"
    """



class InteriorTexture(POVRayElement):
    """InteriorTexture([TextureItems...]):
    """



class PigmentPattern(POVRayElement):
    """PigmentPattern(PIGMENT_BODY)
    """


class Slope(POVRayElement):
    """Pigment(
         Slope(
           [Direction] *[, Lo_slope, Hi_slope ]
           *[ altitude [Altitude] *[, Lo_alt, Hi_alt ]]
           )
         *[PIGMENT_MODIFIERS...]
         )
    """


class ImagePattern(POVRayElement):
    """IMAGE_PATTERN:
         ImagePattern(
           BITMAP_TYPE "bitmap.ext" *[gamma GAMMA] *[premultiplied BOOL]
           *[IMAGE_MAP_MODS...]
           )
       IMAGE_MAP_MOD:
         map_type Type | once | interpolate Type | use_alpha
         ITEM_MAP_BODY:
         ITEM_MAP_IDENTIFIER | ITEM_MAP_ENTRY...
         ITEM_MAP_ENTRY:
         *[ GRAY_VALUE  ITEM_MAP_ENTRY... ]
    """


class Warp(POVRayElement):
    """Warp( WARP_ITEM )
       WARP_ITEM:
         'repeat', [Direction],  *[REPEAT_ITEMS...] |
         'black_hole', [Location], Radius,  *[BLACK_HOLE_ITEMS...] |
         'turbulence', [Amount],  *[TURB_ITEMS...]
         'cylindrical' ,   *[ 'orientation', VECTOR | 'dist_exp', FLOAT ]
         'spherical' ,   *[ 'orientation', VECTOR | 'dist_exp', FLOAT ]
         'toroidal' ,   *[ 'orientation', VECTOR | 'dist_exp', FLOAT |
         'major_radius', FLOAT ] | 'planar' ,  *[ VECTOR , 'FLOAT', ]
       REPEAT_ITEMS:
         'offset', [Amount] |
         'flip', [Axis]
       BLACK_HOLE_ITEMS:
         'strength', Strength | 'falloff', Amount | 'inverse'  |
         'repeat', [Repeat] | 'turbulence', [Amount]
       TURB_ITEMS:
         'octaves', Count | 'omega', Amount | 'lambda', Amount"""



class ImageMap(POVRayElement):
    """IMAGE_MAP:
         Pigment(
           ImageMap(
            *[BITMAP_TYPE] "bitmap*[.ext]" *[gamma GAMMA] *[premultiplied BOOL]
            *[IMAGE_MAP_MODS...]
             )
         *[PIGMENT_MODFIERS...]
         )
        IMAGE_MAP:
         Pigment(
          ImageMap(
            FUNCTION_IMAGE
            )
         *[PIGMENT_MODFIERS...]
         )
        BITMAP_TYPE:
          exr | gif | hdr | iff | jpeg | pgm | png | ppm | sys | tga | tiff
        IMAGE_MAP_MODS:
          map_type Type | once | interpolate Type |
          filter Palette, Amount | filter all Amount |
          transmit Palette, Amount | transmit all Amount
        FUNCTION_IMAGE:
          function I_WIDTH, IHEIGHT( FUNCTION_IMAGE_BODY )
        FUNCTION_IMAGE_BODY:
          PIGMENT | FN_FLOAT | Pattern( PATTERN *[PATTERN_MODIFIERS] )
    """


class Media(POVRayElement):
    """Media( *[MEDIA_IDENTIFIER],  *[MEDIA_ITEMS...] )
       MEDIA_ITEMS:
         'method', Number | 'intervals', Number | 'samples', Min, Max |
         'confidence', Value  | 'variance', Value | 'ratio', Value | 
         'jitter', Value | 'absorption', COLOR | 'emission', COLOR |
         'aa_threshold', Value | 'aa_level', Value |
         Scattering(
           Type, COLOR,  *[ 'eccentricity', Value ],  *[ 'extinction', Value ]
           )  |
         Density(
           *[DENSITY_IDENTIFIER],  *[PATTERN_TYPE],  *[DENSITY_MODIFIER...]
           )   |
         TRANSFORMATIONS
       DENSITY_MODIFIER:
         PATTERN_MODIFIER | DENSITY_LIST | COLOR_LIST |
         ColorMap( COLOR_MAP_BODY ) | ColourMap( COLOR_MAP_BODY ) |
         DensityMap( DENSITY_MAP_BODY )"""


class Interior(POVRayElement):
    """Interior( *[INTERIOR_IDENTIFIER],  *[INTERIOR_ITEMS...] )
       INTERIOR_ITEM:
         'ior', Value | 'caustics', Value | 'dispersion', Value |
         'dispersion_samples', Samples | 'fade_distance', Distance |
         'fade_power', Power | 'fade_color', [Color]
         MEDIA..."""


class Scattering(POVRayElement):
    """Scattering(
           Type, COLOR,  *[ 'eccentricity', Value ],  *[ 'extinction', Value ]
           )"""


class Density(POVRayElement):
    """Density(
           *[DENSITY_IDENTIFIER]
           *[DENSITY_TYPE]
           *[DENSITY_MODIFIER...]
           )
       DENSITY_TYPE:
         PATTERN_TYPE | COLOR
         DENSITY_MODIFIER:
         PATTERN_MODIFIER | DENSITY_LIST | ColorMap( COLOR_MAP_BODY ) |
         ColourMap( COLOR_MAP_BODY ) | DensityMap( DENSITY_MAP_BODY )"""


class DensityMap(POVRayMap):
    """DensityMap( DENSITY_MAP_BODY )
       DENSITY_MAP_BODY:
         DENSITY_MAP_IDENTIFIER | DENSITY_MAP_ENTRY...
       DENSITY_MAP_ENTRY:
         *[ 'Value', DENSITY_BODY ]"""
