#Codigo ayuda: https://github.com/churly92/Engine3D/blob/main/gl.py
#Repositorio perteneciente a Prof. Carlos Alonso

#Mirka Monzon 18139
#RT1: Spheres and Materials

import collections

#Constantes
V2 = collections.namedtuple('Point2', ['x', 'y'])
V3 = collections.namedtuple('Point3', ['x', 'y', 'z'])
V4 = collections.namedtuple('Point4', ['x', 'y', 'z', 'w'])

def sum(v0, v1):
    #Vector suma
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
    #Vector resta
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
    #Vector multiplicacion 
    return V3(v0.x * k, v0.y * k, v0.z * k)

def div(v0, k):
    #Vector division
    return V3(v0.x / k, v0.y / k, v0.z / k)

def dot(v0, v1):
    #Producto punto
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
    #Producto cruz
    x = v0.y * v1.z - v0.z * v1.y
    y = v0.z * v1.x - v0.x * v1.z
    z = v0.x * v1.y - v0.y * v1.x

    return V3(x, y, z)

def magnitud(v0):
    #Vector magnitud
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    #Vector normal
    l = magnitud(v0)
    if l == 0:
        return V3(0, 0, 0)
    else:
        return V3(v0.x/l, v0.y/l, v0.z/l)

def multMatrices(m1,m2):
    #Multiplicacion de matrices 
    if len(m1[0]) == len(m2):
        resultMatrix = [[0] * len(m2[0]) for i in range(len(m1))]
        for x in range(len(m1)):
            for y in range(len(m2[0])):
                for z in range(len(m1[0])):
                    try:
                        resultMatrix[x][y] += m1[x][z] * m2[z][y]
                    except IndexError:
                        pass
        return resultMatrix
    else:
        print("\nERROR: No se pudo realizar la multiplicación de matrices porque el número de columnas de la primera matriz no es igual al número de filas de la segunda matriz")
        return 0