""" Fibonacci spiral - Originally written by Simon Burton """

from vapory import *
from math import pi, sqrt, sin, cos

# Compute the characteristics of the spheres
n_spheres=200
angles = [pi*(sqrt(5) - 1)*i for i in range(n_spheres)]
distances  = [0.5*i for i in range(n_spheres)]
radii = [0.7*sqrt(i) for i in range(n_spheres)]


light_sources = [ LightSource(location, color) for location, color in
                             [((100, 100, -100),    (1, 1, 1)),
                              ((150, 150, -100),    (0, 0, 0.3)),
                              ((-150, 150, -100),   (0, 0.3, 0)),
                              ((150, -150, -100),   (0.3, 0, 0))]
                ]

spheres = [Sphere([d*sin(a), d*cos(a), 0], r,
                   Texture( Finish( 'ambient', 0,
                                    'diffuse', 0,
                                    'reflection', 0,
                                    'specular', 1),
                    Pigment('color', [1,1,1])))

            for d,r,a in zip(distances, radii, angles)]


scene = Scene( Camera( 'location', [0, 0, -128], 
                       'look_at', [0, 0, 0]),
               objects = light_sources + spheres)

scene.render("spiral.png", width=300, height=260)