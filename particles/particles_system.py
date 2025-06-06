from particles import Particle, Proton, Neutron, Electron, Neutrino
from typing import List

class ParticleSystem:
    def __init__(self, time_scale: float = 1.0):
        self.particles: List[Particle] = []
        self.sim_time: float = 0.0
        self.time_scale = time_scale
        self.running: bool = False
        self.interaction_engine = InteractionEngine()

    def step(self, dt_real: float):
        if not self.running:
            return

        dt_sim = dt_real * self.time_scale
        self.sim_time += dt_sim

        new_particles = []
        for particle in self.particles:
            if particle.alive:
                result = particle.update(self.sim_time)
                if result:
                    new_particles.extend(result)

        interaction_results = self.interaction_engine.process(self.particles, self.sim_time)
        self.particles = [p for p in self.particles if p.alive] + new_particles + interaction_results




class InteractionEngine:
    def process(self, particles: List[Particle], time_now: float) -> List[Particle]:
        new_particles = []

        for p in particles:
            if isinstance(p, Neutron) and not p.bound and time_now - p.birth_time > 880:
                p.destroy()
                new_particles.extend([
                    Proton(position=p.position, momentum=p.momentum, birth_time=time_now),
                    Electron(position=p.position, momentum=(0.0, 0.0, 0.0), birth_time=time_now),
                    Neutrino(position=p.position, momentum=(0.0, 0.0, 0.0), birth_time=time_now, is_antiparticle=True),
                ])

        return new_particles
