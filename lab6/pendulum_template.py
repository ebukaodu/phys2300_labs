import numpy as np
from vpython import *
from matplotlib import pyplot as plt

g = 9.81    # m/s**2
l = 1     # meters
l2 = 2
W = 0.002   # arm radius
R = 0.06     # ball radius
R2 = 0.06
framerate = 150
steps_per_frame = 10


def set_scene():
    """
    Set Vpython Scene
    :param: data: list of the data for the simple pendulum motion
    """
    scene.title = "Assignment 6: simple pendulum motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc
    scene.background = color.black
    scene.center = vector(0,0.1,0)
    
    
   
    


def plot_data(t, y, z):
    """
    Create plot for the information from the simple pendulum motion.
    :param: t: list of the time for the pendulum motion
    :param: y: list of the angle for the pendulum motion
    """
    
    plt.plot(t, y, label='Shorter pendulum')
    plt.plot(t, z, label='Longer pendulum')
    plt.title('Pendulum Motion:')
    plt.xlabel('time (s)')
    plt.ylabel('angle (rad)')
    plt.grid(True)
    plt.show()
    



def f(r):
    """
    Pendulum
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta) - 2 * omega
    return np.array([ftheta, fomega], float)

def f2(r2):
    """
    Pendulum
    """
    theta = r2[0]
    omega = r2[1]
    ftheta = omega
    fomega = -(g/l2)*np.sin(theta) - 0.9 * omega
    return np.array([ftheta, fomega], float)


def main():
    """
    """
    # Set up initial values
    h = 1.0/(framerate * steps_per_frame)
    r = np.array([np.pi*179/180, 0], float) #angles
    r2 = np.array([np.pi*179/180, 0], float) #angles

    # Initial x and y
    x = l*np.sin(r[0])
    y = -l*np.cos(r[0])

    x2 = l2*np.sin(r2[0])
    y2 = -l2*np.cos(r2[0])
    

    ang = []
    time = []
    ang2 = []

    roof = box(pos=vector(x,y,0), size=vector(1,0.1,1), color=color.red)

    ball = sphere(pos=vector(x, y, 0),radius=R, color=color.green)
    rod = cylinder(pos=ball.pos, axis=vector(cos(r[0]), -sin(r[0]), 0), radius=0.02, color=color.cyan)

    ball2 = sphere(pos=vector(x2, y, 0), radius=R2, color=color.yellow)
    rod2 = cylinder(pos=ball2.pos, axis=vector(x2,y2, 0), radius=0.02, color=color.green)

    # Set Scene
    
    set_scene()
    
    # Loop over some time interval
    dt = 0.01 # time interval 
    t = 0 # time 



        
    # Use the 4'th order Runga-Kutta approximation
	# for i in range(steps_per_frame):
    #r += h*f(r)

    for k in range(framerate):
        rate(5) # maximum 100 calculations per second
        # Calculate the 4th Order Rung-Kutta
        k1 = f(r)
        k2 = h*f(r + 0.5*k1)
        k3 = h*f(r + 0.5*k2)
        k4 = h*f(r + k3)
        r += (k1 + 2*k2 + 2*k3 + k4) / 6 # Update your vector
        
        k12 = f2(r2)
        k22 = h*f2(r2 + 0.5 * k12)
        k32 = h*f2(r2 + 0.5 * k22)
        k42 = h*f2(r2 + k32)
        r2 += (k12 + 2 * k22 + 2 * k32 + k42) / 6 # Update your vector
        
        
        time.append(t)
        ang.append(r[0])
        ang2.append(r2[0])


        # Update positions
        x = np.cos(r[0] - np.pi/2)
        y = -abs(np.sin(r[0] - np.pi/2))

        x2 = l2*np.cos(r2[0] - np.pi/2)
        y2 = -abs(l2*np.sin(r2[0] - np.pi/2))

        # Update the cylinder axis
        rod.axis = vector(x, y, 0)
        rod2.axis = vector(x2, y2, 0)
    

        # Update the pendulum's bob
        ball.pos = vector(x + 0.025, y + 1, 0)
        ball2.pos = vector(x2 + 0.025, y2 + 1, 0)

        t += dt

        #t=t+dt # updating time

    plot_data(time, ang, ang2)


if __name__ == "__main__":
    main()
    exit(0)
			