""" Just a purple sphere """

from vapory import *
import matplotlib.pyplot as plt


scene = Scene(

    Camera( 'location', [0, 2, -3],
            'look_at',  [0, 1, 2]),

    objects = [ LightSource( [2, 4, -3], 'color', [1,1,1] ),
                Sphere( [0, 1, 2] , 2,   Texture( Pigment( 'color', [1,0,1])))]
)


nparray=scene.render(width = 600, height=400, remove_temp=1)

plt.imshow(nparray)
