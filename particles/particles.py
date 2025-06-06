from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional, List
import math

c = 299_792_458  # lightspeed, m/s

class Charge(Enum):
    POSITIVE = +1
    NEGATIVE = -1
    NEUTRAL = 0

@dataclass
class Particle:
    """
    Base class for physical particles with shared and dynamic properties.
    """

    # --- Dynamic (instance) fields ---
    color_rgb: Tuple[int, int, int]
    position: Tuple[float, float, float]
    momentum: Tuple[float, float, float]
    bound: bool

    # --- Static (shared) properties ---
    mass_kg: float
    charge: Charge
    spin: float
    magnetic_moment: float
    radius_m: float
    symbol: str
    
    # --
    birth_time: float = 0.0
    alive: bool = True
    
    def __str__(self):
        return (
            f"{self.symbol}: mass={self.mass_kg:.2e} kg, charge={self.charge.name}, "
            f"spin={self.spin} ħ, μ={self.magnetic_moment} μN, "
            f"position={self.position}, bound={self.bound}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"position={self.position}, momentum={self.momentum}, bound={self.bound})"
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.position == other.position and
            self.momentum == other.momentum and
            self.bound == other.bound
        )

    def __hash__(self):
        return hash((self.position, self.momentum, self.bound))

    def is_antiparticle(self) -> bool:
        if self.symbol == "γ":
            return True  # Photon is its own antiparticle
        return self.symbol.startswith("anti-")

    def antiparticle(self) -> 'Particle':
        """
        Returns the corresponding antiparticle.
        If the particle is its own antiparticle (like the photon), returns itself.
        """
        if self.symbol == "γ":
            return self  # photon is its own antiparticle

        is_anti = self.is_antiparticle()
        if is_anti and self.symbol.startswith("anti-"):
            new_symbol = self.symbol[len("anti-"):]  # remove "anti-" prefix
        else:
            new_symbol = f"anti-{self.symbol}"

        return self.__class__(
            color_rgb=self.color_rgb,
            position=self.position,
            momentum=self.momentum,
            bound=self.bound,
            mass_kg=self.mass_kg,
            charge=Charge(-self.charge.value),
            spin=self.spin,
            magnetic_moment=-self.magnetic_moment,
            radius_m=self.radius_m,
            symbol=new_symbol
        )
        
    def as_dict(self) -> dict[str, str | float | bool | tuple | int]:
        """
        Returns a dictionary representation of the particle, useful for
        serialization, visualization, or debugging.
        """
        return {
            "type": self.__class__.__name__,
            "symbol": self.symbol,
            "position": self.position,
            "momentum": self.momentum,
            "bound": self.bound,
            "charge": self.charge.name,
            "mass_kg": self.mass_kg,
            "spin": self.spin,
            "magnetic_moment": self.magnetic_moment,
            "radius_m": self.radius_m,
            "color_rgb": self.color_rgb,
            "is_antiparticle": self.is_antiparticle()
        }
    
    def destroy(self):
        self.alive = False

    def update(self, time_now: float) -> Optional[List['Particle']]:
        """
        Called on Particle System updates.
        Return new particles list or None.
        """
        return None
    
    def age(self, sim_time_now: float) -> float:
        return sim_time_now - self.birth_time
    
    def energy(self) -> float:
        """
        E = sqrt((pc)^2 + (m c^2)^2)
        """
        px, py, pz = self.momentum
        p2 = px*px + py*py + pz*pz
        return math.sqrt(p2 * c**2 + (self.mass_kg * c**2)**2)
    
    def velocity(self) -> Tuple[float, float, float]:
        px, py, pz = self.momentum
        p_magnitude = math.sqrt(px*px + py*py + pz*pz)

        if p_magnitude == 0:
            return (0.0, 0.0, 0.0)

        if self.mass_kg == 0.0:
            vx = (px / p_magnitude) * c
            vy = (py / p_magnitude) * c
            vz = (pz / p_magnitude) * c
        else:
            E = self.energy()
            # relative speed: v = pc² / E
            vx = (px * c**2) / E
            vy = (py * c**2) / E
            vz = (pz * c**2) / E

        # Ensure speed does not exceed the speed of light
        speed = math.sqrt(vx*vx + vy*vy + vz*vz)
        if speed > c:
            factor = c / speed
            return (vx * factor, vy * factor, vz * factor)

        return (vx, vy, vz)
    
    def move(self, dt: float):
        vx, vy, vz = self.velocity()
        x, y, z = self.position
        self.position = (x + vx * dt, y + vy * dt, z + vz * dt)


class Proton(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False,
        birth_time: float = 0.0
    ):
        super().__init__(
            color_rgb=(255, 0, 0), # Red for proton
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=1.67262192369e-27,
            charge=Charge.POSITIVE,
            spin=0.5,
            magnetic_moment=2.79,
            radius_m=0.84e-15,
            birth_time=birth_time,
            symbol="p+"
        )


class Neutron(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False,
        birth_time: float = 0.0
    ):
        super().__init__(
            color_rgb=(128, 128, 128), # Gray for neutron
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=1.67492749804e-27,
            charge=Charge.NEUTRAL,
            spin=0.5,
            magnetic_moment=-1.91,
            radius_m=0.84e-15,
            birth_time=birth_time,
            symbol="n0"
        )
    

class Electron(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False,
        birth_time: float = 0.0
    ):
        super().__init__(
            color_rgb=(0, 0, 255),  # Blue for electron
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=9.1093837015e-31,
            charge=Charge.NEGATIVE,
            spin=0.5,
            magnetic_moment=-1.00115965218128,
            radius_m=2.8179403227e-15,    # Classical electron radius (model parameter)
            birth_time=birth_time,
            symbol="e-"
        )

class Photon(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False,
        birth_time: float = 0.0
    ):
        super().__init__(
            color_rgb=(255, 255, 0),  # Yellow for photon
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=0.0,
            charge=Charge.NEUTRAL,
            spin=1.0,
            magnetic_moment=0.0,
            radius_m=0.0,
            birth_time=birth_time,
            symbol="γ"
        )

class Neutrino(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False,
        is_antiparticle: bool = False,
        birth_time: float = 0.0
    ):
        super().__init__(
            color_rgb=(0, 255, 0),  # Зеленый, условно
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=1e-36,
            charge=Charge.NEUTRAL,
            spin=0.5,
            magnetic_moment=0.0,
            radius_m=0.0,
            birth_time=birth_time,
            symbol="νₑ"
        )