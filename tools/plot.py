from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def plotBoard(locations, dimensions):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for l in locations:
        ax.scatter(xs=l[0], ys=l[1], zs=l[2], c='black' if 'd' == l[3] else l[3], marker='v' if 'd' == l[3] else 's', s=100, alpha=.75)
                
    ax.set_xlabel('X', fontsize=15)
    ax.set_ylabel('Z', fontsize=15)
    ax.set_zlabel('Y', fontsize=15)

    ax.set_xlim([0-((dimensions[0]-1)/2), ((dimensions[0]-1)/2)])
    ax.set_ylim([0-((dimensions[1]-1)/2), ((dimensions[1]-1)/2)])
    ax.set_zlim([0, (dimensions[2]-1)])

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.zaxis.set_major_locator(ticker.MultipleLocator(5))

    plt.title('Drone World', fontsize=20)
    plt.show()