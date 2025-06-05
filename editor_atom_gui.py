import imgui
import glfw
from OpenGL.GL import *
from imgui.integrations.opengl import FixedPipelineRenderer

class EditorAtomGUI:
    def __init__(self):
        # Initialize the library
        if not glfw.init():
            raise Exception("GLFW initialization failed")

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(800, 600, "Atom Editor", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")

        # Make the window's context current
        glfw.make_context_current(self.window)

        imgui.create_context()
        io = imgui.get_io()
        io.display_size = (800, 600)

        # Fix for the font atlas error
        io.fonts.get_tex_data_as_rgba32()

        # Initialize the OpenGL renderer
        self.renderer = FixedPipelineRenderer()

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            # Start the ImGui frame
            imgui.new_frame()

            # Set window positions correctly
            imgui.set_next_window_pos(50, 50, condition=imgui.FIRST_USE_EVER)
            imgui.begin("Panel 1")
            imgui.text("This is Panel 1")
            imgui.end()

            imgui.set_next_window_pos(300, 50, condition=imgui.FIRST_USE_EVER)
            imgui.begin("Panel 2")
            imgui.text("This is Panel 2")
            imgui.end()

            imgui.set_next_window_pos(50, 300, condition=imgui.FIRST_USE_EVER)
            imgui.begin("Panel 3")
            imgui.text("This is Panel 3")
            imgui.end()

            imgui.set_next_window_pos(300, 300, condition=imgui.FIRST_USE_EVER)
            imgui.begin("Panel 4")
            imgui.text("This is Panel 4")
            imgui.end()

            # Rendering
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            imgui.render()
            self.renderer.render(imgui.get_draw_data())

            glfw.swap_buffers(self.window)

        glfw.terminate()

if __name__ == "__main__":
    gui = EditorAtomGUI()
    gui.run()
