from OpenGL.GL import *
import math

def render_particles(particles):
    glPointSize(10)
    glBegin(GL_POINTS)
    for p in particles:
        r, g, b = [c / 255.0 for c in p.color_rgb]
        glColor3f(r, g, b)
        glVertex2f(p.position[0], p.position[1])
    glEnd()