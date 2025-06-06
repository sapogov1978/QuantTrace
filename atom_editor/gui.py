import imgui
import inspect
from particles.particles import Particle

antiparticle_flags = {}

def get_particle_classes():
    return {
        cls.__name__: cls for cls in Particle.__subclasses__()
        if not inspect.isabstract(cls)
    }

WIDTH_FIXED = 1 << 3  # 8
WIDTH_STRETCH = 1 << 4  # 16

def draw_particle_control(use_antiparticles_ref):
    particle_classes = get_particle_classes()
    
    num_rows = len(particle_classes) + 2
    height = 25 * num_rows + 60

    imgui.set_next_window_size(220, height, imgui.ALWAYS)
    imgui.begin("Add Particles", True, imgui.WINDOW_NO_RESIZE)

    if imgui.begin_table("particles_table", 4, 0):
        imgui.table_setup_column("Remove", WIDTH_FIXED, 30)
        imgui.table_setup_column("Name", WIDTH_STRETCH)
        imgui.table_setup_column("Add", WIDTH_FIXED, 30)
        imgui.table_setup_column("Anti", WIDTH_FIXED, 60)
        
        for name, cls in particle_classes.items():
            if name not in antiparticle_flags:
                antiparticle_flags[name] = False

            instance = cls()
            symbol = instance.symbol

            imgui.table_next_row()
            
            # Кнопка удалить (минус)
            imgui.table_set_column_index(0)
            if imgui.button(f"-##{symbol}"):
                if antiparticle_flags[name]:
                    particle = cls().antiparticle()
                else:
                    particle = cls()
                # system.remove(particle)

            # Имя частицы
            imgui.table_set_column_index(1)
            imgui.text(name)

            # Кнопка добавить (плюс)
            imgui.table_set_column_index(2)
            if imgui.button(f"+##{symbol}"):
                if antiparticle_flags[name]:
                    particle = cls().antiparticle()
                else:
                    particle = cls()
                # system.add(particle)

            # Чекбокс переключения античастицы для строки
            imgui.table_set_column_index(3)
            changed, new_val = imgui.checkbox(f"anti##anti_checkbox_{symbol}", antiparticle_flags[name])
            if changed:
                antiparticle_flags[name] = new_val

        imgui.end_table()

    imgui.end()
