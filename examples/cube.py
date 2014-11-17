""" Just a purple sphere """

from vapory import *

scene = Scene(  Camera('location',  [0.0, 0.5, -4.0],
                       'direction', [0,0,1.5],
                       'look_at',  [0, 0, 0]),

                objects = [

                    Background("color", [0.85, 0.75, 0.75]),

                    LightSource([0, 0, 0],
                                  'color',[1, 1, 1],
                                  'translate', [-5, 5, -5]),

                    LightSource ([0, 0, 0],
                                    'color', [0.25, 0.25, 0.25],
                                    'translate', [6, -6, -6]),


                    Box([-0.5, -0.5, -0.5], [0.5, 0.5, 0.5],
                         Texture( Pigment( 'color', [1,0,0]),
                                  Finish('specular', 0.6),
                                  Normal('agate', 0.25, 'scale', 0.5)),
                        'rotate', [45,46,47])
               ]
)

# We use antialiasing. Remove this option for faster rendering.
scene.render("cube.png", width=300, height=300, antialiasing=0.001)