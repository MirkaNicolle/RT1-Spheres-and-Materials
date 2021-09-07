#Codigo ayuda: https://github.com/churly92/Engine3D/blob/main/gl.py
#Repositorio perteneciente a Prof. Carlos Alonso

#Mirka Monzon 18139
#RT1: Spheres and Materials

import struct
import math
import time
from random import randint as random
from random import uniform as randomDec
from obj import ObjReader
from arithmetics import *

#Definicion
def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r,g,b):
    return bytes([b, g, r])

#Convertidor de vértices en coordenadas baricéntricas
def barycentric(A, B, C, P):
    cx, cy, cz = cross(V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y))

    #CZ no puede ser menos de 1
    if cz == 0:
        return -1, -1, -1

    #Calcula las coordenadas baricéntricas
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return  w, v, u

BLACK = color(0,0,0)
WHITE = color(255,255,255)
PI = 3.14159265359

#Raytracer 
class Raytracer(object):

    def __init__(self, width, height):

        self.current_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

        self.camPosition = V3(0, 0, 0)
        self.fov = 60

        self.scene = []

    #Inicializacion de software render 
    def glInit(self):
        pass
 
    #Inicializacion de framebuffer
    def glCreateWindow(self, height, width):
        self.height = height
        self.width = width
        self.glClear()
        self.glViewPort(0, 0, width, height)
    
    #Creacion de espacio para dibujar
    def glViewPort(self, x, y, width, height):
        self.x = x
        self.y = y
        self.vpx = width
        self.vpy = height

    #Mapa de bits de un solo color
    def glClear(self):
        self.framebuffer = [
            [
                self.clear_color for x in range(self.width)
                ]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [
                float('inf') for x in range(self.width)
                ]
            for y in range(self.height)
        ]

    #Fondo
    def glBackground(self, texture):
        self.framebuffer = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    #Cambio de color de punto en pantalla, funcion en conjunto con glViewPort 
    def glVertex(self, x, y, color = None):

        pixelX = ( x + 1) * (self.vpx  / 2 ) + self.x
        pixelY = ( y + 1) * (self.vpy / 2 ) + self.y

        if pixelX >= self.width or pixelX < 0 or pixelY >= self.height or pixelY < 0:
            return

        try:
            self.framebuffer[round(pixelY)][round(pixelX)] = color or self.current_color
        except:
            pass

    def glVertex_coord(self, x, y, color = None):
        if x < self.x or x >= self.x + self.vpx or y < self.y or y >= self.y + self.vpy:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.framebuffer[y][x] = color or self.current_color
        except:
            pass

    #Cambio de color con el que funciona glVertex
    def glColor(self, r, g, b):
        try:
            self.rv = round(255*r)
            self.gv = round(255*g)
            self.bv = round(255*b)
            self.vertex_color = color(self.rv,self.gv,self.bv)
        except ValueError:
                print('\nERROR: Ingrese un número entre 1 y 0\n')

    #Cambio de color de glClear
    def glClearColor(self, r, g, b):
        try:
            self.rc = round(255*r)
            self.gc = round(255*g)
            self.bc = round(255*b)
            self.clear_color = color(self.rc, self.rg, self.rb)
        except ValueError:
            print('\nERROR: Ingrese un número entre 1 y 0\n')
    
    #Bitmap 
    def glFinish(self, file_name):
        
        bmp_file = open(file_name, 'wb')

        #Header 14 bytes
        bmp_file.write(char('B'))
        bmp_file.write(char('M'))
        bmp_file.write(dword(14 + 40 + self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(14 + 40))
        
        #File 40 bytes
        bmp_file.write(dword(40))
        bmp_file.write(dword(self.width))
        bmp_file.write(dword(self.height))
        bmp_file.write(word(1))
        bmp_file.write(word(24))
        bmp_file.write(dword(0))
        bmp_file.write(dword(self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))

        # Pixeles, 3 bytes cada uno
        for x in range(self.height):
            for y in range(self.width):
                bmp_file.write(self.framebuffer[x][y])
            
        bmp_file.close()

    def glZBuffer(self, filename):
        bmp_file = open(filename, 'wb')

        #Header 14 bytes
        bmp_file.write(bytes('B'.encode('ascii')))
        bmp_file.write(bytes('M'.encode('ascii')))
        bmp_file.write(dword(14 + 40 + self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(14 + 40))

        #Image Header 40 bytes
        bmp_file.write(dword(40))
        bmp_file.write(dword(self.width))
        bmp_file.write(dword(self.height))
        bmp_file.write(word(1))
        bmp_file.write(word(24))
        bmp_file.write(dword(0))
        bmp_file.write(dword(self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                bmp_file.write(color(depth,depth,depth))

        bmp_file.close()

    def rtRender(self):
        for y in range(self.height):
            for x in range(self.width):
                # NDC
                Px = 2 * ( (x+0.5) / self.width) - 1
                Py = 2 * ( (y+0.5) / self.height) - 1

                # FOV
                t = math.tan( (self.fov * PI / 180) / 2 )
                r = t * self.width / self.height
                Px *= r
                Py *= t

                # Cam always towards -k
                direction = V3(Px, Py, -1)
                direction = div(direction, magnitud(direction))

                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camPosition, direction)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material

                if material is not None:
                    self.glVertex_coord(x, y, material.diffuse)