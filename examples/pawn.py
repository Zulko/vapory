""" Just a purple sphere """

from vapory import *


objects = [

    # SUN
    LightSource([1500,2500,-2500], 'color',1),

    # SKY
    Sphere(  [0,0,0],1, 'hollow',
              Texture( 
                        Pigment(  'gradient', [0,1,0],
                                  'color_map{[0 color White] [1 color Blue  ]}'
                                  'quick_color', 'White'
                               ),
                        Finish( 'ambient', 1, 'diffuse', 0)
                    ), 

              'scale', 10000
            ),
    
    # GROUND
    Plane(  [0,1,0], 0 ,
            Texture( Pigment( 'color', [1.1*e for e in [0.80,0.55,0.35]])),
            Normal( 'bumps', 0.75, 'scale', 0.035),
            Finish(  'phong', 0.1 )
         ),

    # PAWN
    Union(  Sphere([0,1,0],0.35),
            Cone([0,0,0],0.5,[0,1,0],0.0),
            Texture( Pigment( 'color', [1,0.65,0])),
            Finish( 'phong', 0.5)
         )
]


scene = Scene( Camera( 'ultra_wide_angle',
                       'angle',45,
                       'location',[0.0 , 0.6 ,-3.0],
                       'look_at', [0.0 , 0.6 , 0.0]
                     ),
               
               objects= objects,
               included=['colors.inc']
              )

scene.render('pawn.png', remove_temp=False)