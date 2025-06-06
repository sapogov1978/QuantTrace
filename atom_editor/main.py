import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
#from particles.particles_system import ParticleSystem
#from .render import render_particles
from .gui import draw_particle_control

def main():
    if not glfw.init():
        return

    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    width, height = mode.size.width, mode.size.height

    window = glfw.create_window(width, height, "Atom Simulator", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    imgui.create_context()
    impl = GlfwRenderer(window)

    use_antiparticles_ref = [False]

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        draw_particle_control(use_antiparticles_ref)

        from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()