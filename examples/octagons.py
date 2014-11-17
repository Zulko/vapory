""" Octogons, after Friedrich A. Lohmueller 
http://www.f-lohmueller.de

This example demonstrates well how you make an intersection or
difference between geometrical shapes in POV-Ray."""

from vapory import *


camera = Camera( 'ultra_wide_angle', 'angle', 30, 
                 'location', [0.0 , 6.8 ,-6.0],
                 'look_at',  [0.0 , 0.8 , 0.0])


sun = LightSource([1500,2500,-2500], 'color',1)

sky = Sphere(  [0,0,0],1, 'hollow',
              Texture(  Pigment(  'gradient', [0,1,0],
                                  ColorMap([0, 'color', 'White'],
                                           [1, 'color', 'Blue' ]),
                                  'quick_color', 'White'),
                        Finish( 'ambient', 1, 'diffuse', 0)),
              'scale', 10000)

ground =    Plane(  [0,1,0], 0 ,
            Texture( Pigment( 'color', [1.1*e for e in [0.40,0.45,0.85]])),
            Finish(  'phong', 0.1 ))

octagon1 = Intersection(
   Box( [-1, 0.0,-1], [ 1,1.0,1 ] ),
   Box( [-1,-0.1,-1], [ 1,1.1,1 ], 'rotate', [0,45,0] ),
   
   'scale', [0.5,2.5,0.5],
   Texture( Pigment( 'color', [1.3,0.91,0.58]),
            Finish ( 'phong', 1)),
   'rotate', [10,30,0],
   'translate', [1.1,-1.00,0])

octagon2 = Intersection(
   Box( [-1, 0.0,-1], [ 1,1.0,1 ] ),
   Box( [-1,-0.1,-1], [ 1,1.1,1 ], 'rotate', [0,45,0] ),
   Cylinder([0,-0.1,0],[0,1.1,0],0.5, 'inverse'),
   
   'scale', [1,0.5,1],
   Texture( Pigment( 'color', [1.3,1.17,0.75]),
            Finish ( 'phong', 1)),
   'rotate', [0,-25,0],
   'translate', [-0.7,0.50,0.5])

scene = Scene( camera, [sun, sky, ground, octagon1, octagon2],
               included=['colors.inc', 'textures.inc'])

scene.render('octagons.png', width=300, height=200, antialiasing=0.001)