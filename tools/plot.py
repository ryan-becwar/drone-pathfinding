from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from itertools import product, combinations

def __plot_cube_at(loc, size):
    r = size/2
    points = np.array([[-r, -r, 0],
                       [r, -r, 0],
                       [r, r, 0],
                       [-r, r, 0],
                       [-r, -r, 2*r],
                       [r, -r, 2*r],
                       [r, r, 2*r],
                       [-r, r, 2*r]])
    points[:, 0] += loc[0]
    points[:, 1] += loc[1]
    points[:, 2] += loc[2]
    verts = [[points[0], points[1], points[2], points[3]],
             [points[4], points[5], points[6], points[7]],
             [points[0], points[1], points[5], points[4]],
             [points[2], points[3], points[7], points[6]],
             [points[1], points[2], points[6], points[5]],
             [points[4], points[7], points[3], points[0]],
             [points[2], points[3], points[7], points[6]]]
    return points, verts

def plot(sim):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 110)
    ax.set_zlim(0, 50)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_zticklabels([])
    for x in range(len(sim.map)):
        for z in range(len(sim.map[x])):
            for y in range(len(sim.map[x][z])):
                color = sim.map[x][z][y]
                if color == 'd':
                    rx = x*10
                    ry = y*10
                    rz = z*10
                    points, verts = __plot_cube_at((rx, rz, ry), 4)
                    collection = Poly3DCollection(verts, alpha=1.0)
                    collection.set_facecolor('black')
                    ax.add_collection3d(collection)
                    continue
                if color != ' ':
                    rx = x*10
                    ry = y*10
                    rz = z*10
                    points, verts = __plot_cube_at((rx, rz, ry), 10)
                    collection = Poly3DCollection(verts, alpha=0.5)
                    collection.set_facecolor(color)
                    ax.add_collection3d(collection)
    plt.title('Drone World', fontsize=20)
    plt.show()




def plotBoard(locations, dimensions=(101, 101, 51)):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for l in locations:
        ax.scatter(xs=(l[0]-((dimensions[0]-1)/2)), ys=(l[1]-((dimensions[1]-1)/2)), zs=l[2], c='black' if 'd' == l[3] else l[3], marker='v' if 'd' == l[3] else 's', s=25, alpha=.75)
                
    ax.set_xlabel('X', fontsize=15)
    ax.set_ylabel('Z', fontsize=15)
    ax.set_zlabel('Y', fontsize=15)

    ax.set_xlim([(0-((dimensions[0]-1)/2)), ((dimensions[0]-1)/2)])
    ax.set_ylim([(0-((dimensions[1]-1)/2)), ((dimensions[1]-1)/2)])
    ax.set_zlim([0, (dimensions[2]-1)])

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(5))

    plt.title('Drone World', fontsize=20)
    plt.show()