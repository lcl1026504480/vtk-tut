# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:59:29 2020

@author: lenovouser
"""

#get data of several cities and get their longitude as well as latitude)
from clyent import color
cities_data = """
Bei Jing, 116.23,39.54
Shang Hai, 121.52, 30.91
Hong Kong,114.19,22.38
Delhi,77.21,28.67
Johannesburg,28.04,-26.19
Doha,51.53,25.29
Sao Paulo,-46.63,-23.53
Toronto,-79.38,43.65
New York,-73.94,40.67
San Francisco,-122.45,37.77
Dubai,55.33,25.27
Sydney,151.21,-33.87
"""
# part2_create a list consisting of cities' indexes about their longtitudes and latitudes
import csv
#create a dict and a list
cities = dict()
coords = list()
# print(cities,coords)

# read data
for line in list(csv.reader(cities_data.split("\n")))[1:-1]:
    name, long_, lat = line
    cities[name] = len(coords)
    coords.append((float(long_),float(lat)))

# data transformation
import numpy as np
# from [1 line n row] to [n line, 1 list]
coords = np.array(coords)
# transform the angle to the arc
lat, long = coords.T * np.pi / 180
# transform 2D data to 3D data
# lat = ori_long
# long = ori_lat
x = np.cos(long) * np.cos(lat)
y = np.cos(long) * np.sin(lat)
z = np.sin(long)

#create a window
from mayavi import mlab
mlab.figure(bgcolor=(0.48,0.48,0.48), size=(400,400))

# to define a sphere
# set the opacity of the surface of earth to 0.7
sphere = mlab.points3d(0, 0, 0, scale_factor=2,
                       color = (0.67, 0.77, 0.93),
                       resolution = 100,
                       opacity = 0.7,
                       name = "Earth")

# to adjust the parameter of mirror reflection
sphere.actor.property.specular = 0.45
sphere.actor.property.specular_power = 5
# delete the opposite side to better show the effect of opacity
sphere.actor.property.backface_culling = True
# use points to describe sites of cities
points = mlab.points3d(x, y, z,
                       scale_mode = "none",
                       scale_factor = 0.03,
                       color = (0, 0, 1))

#create names of cities
# for cities.items output the names of cities and the series of cities
for city, index in cities.items():
    #x,y,z mean x,y,z coordinates; color means text's color; width means text's width; name means text's object
    label = mlab.text(x[index], y[index], city,
                      z=z[index], color=(0,0,1),
                      width=0.016 * len(city), name=city)

#create continents
from mayavi.sources.builtin_surface import BuiltinSurface
continents_src = BuiltinSurface(source="earth", name="Continents")
#set the LDD to 2
continents_src.data_source.on_ratio = 2
continents = mlab.pipeline.surface(continents_src, color=(0,0,0))

#create the equitor
# distribute every 360 to 100
theta = np.linspace(0, 2 * np.pi, 50)
x = np.cos(theta)
y = np.sin(theta)
z = np.zeros_like(theta)
mlab.plot3d(x,y,z,color=(1,1,1),opacity=0.2,tube_radius=None)

#show the window for interation
mlab.view(100,60,4,[-0.05,0,0])
mlab.show()