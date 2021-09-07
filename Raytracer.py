#Codigo ayuda: https://github.com/churly92/Engine3D/blob/main/gl.py
#Repositorio perteneciente a Prof. Carlos Alonso

#Mirka Monzon 18139
#RT1: Spheres and Materials

from gl import *
from texture import Texture
from obj import ObjReader
from sphere import Sphere, Material

#Main 
if __name__ == '__main__':

    snow = Material(diffuse = color(224, 224, 224))
    buttons = Material(diffuse = color(112, 112, 112 ))
    smile = Material(diffuse = color(0, 0, 0))
    carrot = Material(diffuse = color(255, 92, 57))
    eye = Material(diffuse = color(153, 153, 153))


    width = 500
    height = 300
    r = Raytracer(width,height)

    #Cuerpo
    r.scene.append( Sphere(V3(0, 0.80, -5), 0.60, snow) ) #Cabeza
    r.scene.append( Sphere(V3(0, 0,  -5), 0.75, snow) ) #Torso
    r.scene.append( Sphere(V3(0, -1, -5), 1, snow) ) #Piernas

    #Botoner
    r.scene.append( Sphere(V3(0, 0, -2), 0.05, buttons) )
    r.scene.append( Sphere(V3(0, -0.25, -2), 0.05, buttons) )
    r.scene.append( Sphere(V3(0, -0.5, -2), 0.05, buttons) )

    #Sonrisa
    r.scene.append( Sphere(V3(0.045, 0.25, -2), 0.02, smile) )
    r.scene.append( Sphere(V3(0.1, 0.30, -2), 0.02, smile) )
    r.scene.append( Sphere(V3(-0.045, 0.25, -2), 0.02, smile) )
    r.scene.append( Sphere(V3(-0.1, 0.30, -2), 0.02, smile) )

    #Nariz
    r.scene.append( Sphere(V3(0, 0.32, -2), 0.02, carrot) )

    #Ojos
    r.scene.append( Sphere(V3(0.075, 0.4, -2), 0.04, eye) )
    r.scene.append( Sphere(V3(-0.075, 0.4, -2), 0.04, eye) )
    
    r.rtRender()

    r.glFinish('output.bmp')