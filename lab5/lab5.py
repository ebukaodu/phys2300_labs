#! /usr/bin/python3
from vpython import *
from math import sin, cos
import argparse
import matplotlib.pyplot as plt 


def set_scene(data):
    """
    Set Vpython Scene
    :param: data: list of the data for the projectile motion
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc
    scene.background = color.white
    scene.center = vector(10,data['init_height'],0)
    num = 0
    if data['init_height'] > 4:
        num = 2
    else:
        num = 0
    floor = box(pos=vector(35,0,0), length=75, width = 3, height = 0.5, color=color.magenta)
    table = box(pos=vector(0, data['init_height'] / 2 ,0), length=5, width = 2, height = data['init_height'] - num, color=color.blue)
    

def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param: data: list of the data for the projectile motion
    """
    ball_nd = sphere(pos=vector(0, data['init_height'], 0),
                        radius=1, color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position
    
    ball_nd.velocity = vector(data['init_velocity'] * cos(data['theta'] * pi / 180),
                              data['init_velocity'] * sin(data['theta'] * pi / 180), 0)
    
    data["init_vel_x"] = data['init_velocity'] * cos(data['theta'] * pi / 180)
    data["init_vel_y"] = data['init_velocity'] * sin(data['theta'] * pi / 180)
    
    #floor = box(pos = (0,0,0), size = (100, 0.25, 10))
    t = 0
    g = vector(0, data['gravity'], 0)
    
    data['pos_x'] = 0
    x1 = []
    y1 = []
    
    # Animate
    mass = data['ball_mass'] * g
    fBallg = (mass / data['ball_mass']) * data["deltat"]
    while ball_nd.pos.y > 0:
        rate(100)  # refresh rate 
        
        ball_nd.velocity = ball_nd.velocity + fBallg
        ball_nd.pos = ball_nd.pos + ball_nd.velocity * data["deltat"]
        
        t = t + data["deltat"]  #update the time
         
        x1.append(ball_nd.pos.x)
        y1.append(ball_nd.pos.y)

    data["x1"] = x1
    data["y1"] = y1


def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param: data: list of the data for the projectile motion
    """
    ball_ar = sphere(pos=vector(0, data['init_height']+ 0.5, 0),
                        radius=1, color=color.yellow, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_ar)

    t = 0
    AR_x = -1/2 * data['rho'] * data["init_vel_x"] * data['Cd']
    AR_y = -1/2 * data['rho'] * data["init_vel_y"] * data['Cd']
    
    g = vector(AR_x, data['gravity'] + AR_y, 0)
    
    ball_ar.velocity = vector(data["init_vel_x"], data["init_vel_y"], 0)
    x_ar = []
    y_ar = []
    
    while ball_ar.pos.y > 0:
        
        rate(100)  # refresh rate 
        mass_ar = data['ball_mass']* g
        ball_ar.velocity = ball_ar.velocity + ( mass_ar/data['ball_mass']) * data["deltat"]
        ball_ar.pos = ball_ar.pos + ball_ar.velocity * data["deltat"]
        
        t = t + data["deltat"] #update the time
        
         #get points for plotting
        x_ar.append(ball_ar.pos.x)
        y_ar.append(ball_ar.pos.y)

    data["x_ar"] = x_ar
    data["y_ar"] = y_ar

    
def plot_data(data):
    """
    Create plot for the information from the two projectile motion.
    :param: data: list of the data for the projectile motion
    """
    fig=plt.figure()
    fig.suptitle('Plot with and without Air resistance')
    plt.subplot(2,1,1) #Plot of the drag motion
    plt.title("Drag projectile motion")
    #plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.plot(data["x_ar"],data["y_ar"])

    plt.subplot(2,1,2) #Plot of the none drag motion
    plt.title("No drag projectile motion")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.plot(data["x1"],data["y1"])
    plt.show()
    

def main():
    """
    "Main" Function
    """
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Description for my parser", add_help=False)
    parser.add_argument("-v", "--velocity", action="store", type=float, required=True, help="The velocity of the object is required")
    parser.add_argument("-a", "--angle", action="store", type=float, required=True, help="The angle of the object is required")
    parser.add_argument("-h", "--height", required=False, type=float, default= 1.2, help="The height of the object is not required. Default is set to 1.2 meters." )
    parser.add_argument("--help", action='help')
    args = parser.parse_args()

    int_vel = 0
    angles = 0
    int_height = 0
    
    if args.velocity:
        int_vel = args.velocity
    if args.angle:
        angles = args.angle
    if args.height:
        int_height = args.height

    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['init_height'] = int_height   # y-axis
    data['init_velocity'] = int_vel  # m/s
    data['theta'] = angles       # degrees
	
    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
	
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
    plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)
