.. image:: http://i.imgur.com/XN7e2IP.gif
   :alt: [logo]
   :align: center


Vapory
========

Vapory is a Python library to render photo-realistic 3D scenes with the free ray-tracing engine `POV-Ray <http://en.wikipedia.org/wiki/POV-Ray>`_.

Here is how you would draw a purple sphere:

.. code:: python

    from vapory import *

    camera = Camera( 'location', [0,2,-3], 'look_at', [0,1,2] )
    light = LightSource( [2,4,-3], 'color', [1,1,1] )
    sphere = Sphere( [0,1,2], 2, Texture( Pigment( 'color', [1,0,1] )))

    scene = Scene( camera, objects= [light, sphere])
    scene.render("purple_sphere.png", width=400, height=300)


Vapory enables to pipe the rendered images back into Python and integrates very well in the Python libraries ecosystem (see `this blog post <http://zulko.github.io/blog/2014/11/13/things-you-can-do-with-python-and-pov-ray/>`_ for examples)

Vapory is an open-source software originally written by Zulko_, released under the MIT licence, and hosted on Github_, where everyone is welcome to contribute or ask for support.


Installation
--------------

Vapory should work on any platform with Python 2.7+ or Python 3.

You first need to install POV-Ray. See `here <http://www.povray.org/download/>`_ for the Windows binaries. For Linux/MacOS you must `compile the source <https://github.com/POV-Ray/povray/>`_ (tested on Ubuntu, it's easy).

If you have PIP installed you can : ::

    (sudo) pip install vapory

If you have neither setuptools nor ez_setup installed the command above will fail, is this case type this before installing: ::

    (sudo) pip install ez_setup


Vapory can also be installed manually by unzipping the source code in one directory and typing in a terminal: ::

    (sudo) python setup.py install

Getting started
----------------

In Vapory you create a scene, and then render it:

.. code:: python

    from vapory import *

    scene = Scene( camera = mycamera , # a Camera object
               objects= [light, sphere], # POV-Ray objects (items, lights)
               atmospheric = [fog], # Light-interacting objects
               included = ["colors.inc"]) # headers that POV-Ray may need

    scene.render("my_scene.png", # output to a PNG image file
      width = 300, height=200, # in pixels. Determines the camera ratio.
      antialiasing = 0.01 # The nearer from zero, the more precise the image.
      quality=1) # quality=1 => no shadow/reflection, quality=10 is 'normal'

    # passing 'ipython' as argument at the end of an IPython Notebook cell
    # will display the picture in the IPython notebook.
    scene.render('ipython', width=300, height=500)

    # passing no 'file' arguments returns the rendered image as a RGB numpy array
    image = scene.render(width=300, height=500)


Objects are defined by passing a list of arguments: ::

    camera = Camera( 'location', [0,2,-3], 'look_at', [0,1,2] )

Keep in mind that this snippet will later be transformed into POV-Ray code by converting each argument to a string and placing them on different lines, to make a valid POV-Ray code ::

    camera {
        location
        <0,1,0>
        look_at
        <0,0,0>
    }

All the objects (Sphere, Box, Plane... with a few exceptions) work the same way. Therefore syntax of Vapory is the same as the syntax of POV-Ray. To learn how to use the different objects:

- Have a look at the scenes in the ``examples`` folder
- See the docstring of the different objects, which provides a basic example.
- See the online `POV-Ray documentation <http://www.povray.org/documentation/3.7.0/t2_0.html/>`_ which will give you all the possible uses of each object (there can be many !). This documentation is easily accessible from Vapory, just type ```Sphere.help()``, ``Plane.help()`` etc., it will open it in your browser.
- Finally, it is easy to find POV-Ray examples online and transcribe them back into Vapory.


Missing Features
""""""""""""""""""

For the moment a many features (Sphere, Fog, etc.) are implemented but not all of them (POV-Ray has a LOT of possible shapes and capabilities).

It is really easy to add new features, because they all basically do the same thing, are just empty classes. For instance here is how Camera is implemented: ::

    class Camera(POVRayElement):
        """ Camera([type,]  'location', [x,y,z], 'look_at', [x,y,z]) """

Yep, that's all, but just the name of the class is sufficient for Vapory to understand that this will translate into POV-Ray code ``camera{...}``. So in most case it shouldn't be difficult to create your own new feature. If you need a non-implemented feature to be included in the package, just open an issue or push a commit.

.. _Zulko : https://github.com/Zulko
.. _Github: https://github.com/Zulko/vapory
