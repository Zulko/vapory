#version 3.6; // 3.7;
#global_settings{ assumed_gamma 1.0 }

from vapory import *

sphere = Sphere( (1,0,-6), 0.5,
                  Finish('ambient', 0.1,
                         'diffuse', 0.6),
                  Pigment('NeonPink'))

box = Box( (-1, -1, -1), (1,  1,  1),
            Finish( 'ambient', 0.1,
                    'diffuse', 0.6),
            Pigment('Green'),
            'rotate', (0, -20, 0))

cylinder = Cylinder((-6, 6, 30), (-6, -1, 30), 3,
                     Finish('ambient', 0.1, 'diffuse', 0.6),
                     Pigment("NeonBlue"))

ground = Plane([0,1,0],-1.0, Texture(Pigment('checker', 'color', 'Gray65',
                                          'color', 'Gray30')))

light1 = LightSource((5, 30, -30), 'White')
light2 = LightSource((-5, 30, -30), 'White')

scene = Scene( Camera( 'location', [0, 1, -10],
                       'look_at', [0, 1, 0],
                       'focal_point', [1, 1, -6],
                       'aperture', 0.4,
                       'blur_samples', 50), # <= Increase for better quality
               
               objects = [light1, light2, sphere, box, cylinder, ground],
               included = ["colors.inc", "shapes.inc", "textures.inc"])

scene.render("focal.png", width=300, height=225, antialiasing=0.01,
             remove_temp=False)

