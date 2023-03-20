from tkinter import Tk, Canvas
from graphics_template import *
import math, time

vp_width, vp_height = 1024, 768
w_xmin, w_ymin, w_xmax = -10, 0, 10
w_ymax = w_ymin + (w_xmax - w_xmin)/vp_width * vp_height

simulation_done = False
DELTA_TSIM = 0.0005
DELTA_TDRAW = 0.02  # 50 fps

CEILING = w_ymax - 0.5
FLOOR = w_ymin + 0.5
KS = 3.0
KD = 0.1
MASS = 0.20

pos_x = 0.0
pos_y = []
prev_pos_y = []

def left_click (event):
    global simulation_done
    simulation_done = True

def Verlet(dt):
    #calculates position at time t+dt, using position at time t and at time t-dt,
    #and acceleration (=f/m) at time t
    #calculates velocity at time t using position at time t+dt and at time t-dt
        y_temp = pos_y[1]
        #link to slides:
        #y(t+dt) = 2*y(t) - y(t-dt) + y''(t)*dt*dt
        v = pos_y[1] - prev_pos_y[1]
        x = pos_y[1] - pos_y[0]
        pos_y[1] = 2.0 * pos_y[1] - prev_pos_y[1] + (-9.81 + ((-KS * x)/MASS) + ((-KD*(v/dt))/MASS)) * dt * dt
        prev_pos_y[1] = y_temp

def do_simulation (dt):
    global simulation_done
    Verlet (dt)
    #mass point 2 -> position via h(t) = -1/2*9.81*t^2 + v0*t + h0
    #v0 == 0 en h0 == CEILING
    t = time.perf_counter() - init_time
    pos_y[2] = -1/2*9.81*t*t + CEILING
    if (pos_y[1] < FLOOR):
         simulation_done = True
         pos_y[1] = FLOOR
         canvas.delete("all")
         draw_scene()
         canvas.update()

def draw_scene ():
    #draw_grid (canvas)
    RED = rgb_col (255,0,0)
    GREEN = rgb_col (0, 255, 0)
    YELLOW = rgb_col (255, 255, 0) 
    draw_line (canvas, w_xmin, FLOOR, w_xmax, FLOOR, RED)
    draw_line (canvas, w_xmin/2, CEILING, w_xmax/2, CEILING, GREEN)
    draw_line (canvas, pos_x, pos_y[0], pos_x, pos_y[1], YELLOW)
    draw_dot (canvas, pos_x, pos_y[1], RED) #draw mass point 1
    draw_dot (canvas, pos_x, pos_y[0], YELLOW) #draw mass point 2


def init_scene ():
    #fix mass point at CEILING
    pos_y.append(CEILING) # init y-coord
    prev_pos_y.append(pos_y[0])
    #mass point 1 -> position via Verlet
    pos_y.append(pos_y[0])
    prev_pos_y.append(pos_y[1])
    #mass point 2 -> position via h(t) = -1/2*9.81*t^2 + v0*t + h0
    pos_y.append(pos_y[0])
    draw_scene()
    
    
window = Tk()
canvas = Canvas(window, width=vp_width, height=vp_height, bg=rgb_col(0,0,0))
canvas.pack()
canvas.bind("<Button-1>", left_click)

init_graphics (vp_width, vp_height, w_xmin, w_ymin, w_xmax)


# time.perf_counter() -> float. Return the value (in fractional seconds)
# of a performance counter, i.e. a clock with the highest available resolution
# to measure a short duration. It does include time elapsed during sleep and
# is system-wide. The reference point of the returned value is undefined,
# so that only the difference between the results of consecutive calls is valid.

init_time = time.perf_counter()
prev_draw_time = 0
prev_sim_time = 0

init_scene ()

while (not simulation_done):
    # simulating
    sim_dt = time.perf_counter() - init_time - prev_sim_time
    if (sim_dt > DELTA_TSIM):
        do_simulation(DELTA_TSIM)
        prev_sim_time += DELTA_TSIM
    # drawing
    draw_dt = time.perf_counter() - init_time - prev_draw_time
    if (draw_dt > DELTA_TDRAW): # 50 fps
        canvas.delete("all")
        draw_scene()
        canvas.update()
        prev_draw_time += DELTA_TDRAW 

