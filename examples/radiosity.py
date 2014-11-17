""" Just a purple sphere """

from vapory import *

radiosity = Radiosity(
'brightness', 2.0,
'count', 100,
'error_bound', 0.15,
'gray_threshold', 0.0,
'low_error_factor', 0.2,
'minimum_reuse', 0.015,
'nearest_count', 10,
'recursion_limit', 5,
'adc_bailout', 0.01,
'max_sample', 0.5,
'media off',
'normal off',
'always_sample', 1,
'pretrace_start', 0.08,
'pretrace_end', 0.01)


sun = LightSource([-1500,2500,-2500], 'color', 'White')


sky = Plane([0,1,0], 1, 'hollow',  
            Texture( Pigment( 'bozo',
                              'turbulence', 0.92,
                               ColorMap( [0.00, 'rgb', [0.18, 0.18, .9]],
                                         [0.50, 'rgb', [0.18, 0.18, .9]],
                                         [0.70, 'rgb', [1,1,1]],
                                         [0.85, 'rgb', [0.25,0.25,0.25]],
                                         [1.0 , 'rgb', [0.5,0.5,0.5]]),
                              'scale', [2.5,2.5,3.75],
                              'translate', [-1.25,0,0]),
            Finish('ambient', 1, 'diffuse', 0)),
            'scale', 10000)

ground = Plane( [0,1,0], 0, 
            Texture( Pigment( 'color', 'rgb', [0.8*i for i in [1.00,0.95,0.8]]),
                     Normal('bumps', 0.75, 'scale', 0.0125),
                     Finish('phong', 0.1))) 

fog = Fog('fog_type',   2,
          'distance',   20,
          'color',     [1.00,0.98,0.9],
          'fog_offset', 0.1,
          'fog_alt',    1,
          'turbulence', 1.8)


chessboard = Union( Box([-1.01, 0, -1.01], [1.01, 0.049, 1.01],
                        Texture( Pigment( 'color', [0.37, 0.25, 0.15] ))),
                    Box([-1, 0, -1], [1, 0.05, 1],
                         Texture( Pigment( 'checker',
                                          'color', [1,1,1],
                                          'color', [0,0,0]),
                                  'scale', 0.25),   
                         ),
                    'rotate', [-25, 30,0],
                    'translate', [0.05, 0.6, 0])


scene = Scene( Camera('angle', 75,'location',  [0.0 , 1.0,-2.0],
                      'look_at', [0 , 0.2 , 0.0]),
               objects = [ sky, ground, fog, chessboard],
               included = ["colors.inc", "textures.inc"],
               defaults = [Finish( 'ambient', 0.1, 'diffuse', 0.9)],
               global_settings=[radiosity] )

scene.render("radiosity.png", width=400, height=300, antialiasing=0.001)