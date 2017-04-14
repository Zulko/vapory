#version 3.6; // 3.7;
#global_settings{ assumed_gamma 1.0 }

from vapory import *

sun = LightSource([1000,2500,-2500], 'color', 'White')


sky = SkySphere(Pigment( 'gradient', [0,1,0],
                         ColorMap([0.0, 'color', 'White'],
                                  [0.5, 'color', 'CadetBlue'],
                                  [1.0, 'color', 'CadetBlue']),
                         "quick_color", "White"))



ground = Plane( [0,1,0], 0,
                Texture( Pigment( 'color', [0.85,0.55,0.30]),
                         Finish( 'phong', 0.1)
                      )
                )

balls = Object( Union(*[Sphere([0,0,i],0.35,
                              Texture( Pigment('color', [1,0.65,0]),
                                       Finish('phong',1)))
                    for i in range(20)]),

               'scale', [0.4, 0.75, 0.75],
               'rotate', [0,5,0],
               'translate', [-1.9, 0.5, 0])

 
box = Box([-1,-1,-1], [1,1,1],
          'scale', [1.5,0.75,0.75],
          'rotate', [0,35, 0],
          'translate', [1.75,1.2,4.0],
          Texture( Pigment( 'Candy_Cane', 
                            'scale', 0.5,
                            'translate', [-2.0,0,0],
                            'quick_color', 'Orange'),
                   Finish( 'phong', 1)
          )
      )

r, over = 6.0, 0.1 # sphere radius, and spheres overlap

lens = Intersection( Sphere( [0,0,0], r,  'translate', [0,0,-r+over]),
                     Sphere( [0,0,0], r,  'translate', [0,0, r-over]),
                     Texture('T_Glass3'),
                     Interior('I_Glass3'),
                     'translate', [0,1.2,0])

scene = Scene( Camera('angle', 75,
                      'location',  [0.0 , 1.0,-3.0],
                      'look_at', [-0.3 , 1.0 , 0.0]),
               objects = [sun, sky, ground, balls, box, lens],
               included = ["colors.inc", "textures.inc", "glass.inc"],
               defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)] )

scene.render("lens.png", width=400, height=300, antialiasing=0.01)
