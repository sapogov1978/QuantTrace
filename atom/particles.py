from dataclasses import dataclass
from enum import Enum
from typing import Tuple, TypeVar

class Charge(Enum):
    POSITIVE = +1
    NEGATIVE = -1
    NEUTRAL = 0

T = TypeVar('T', bound='Particle')

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
        return self.symbol.startswith("anti-")

    def antiparticle(self: T) -> T:
        """
        Returns the corresponding antiparticle.
        If this particle is already an antiparticle, returns the original particle.
        """
        is_anti = self.is_antiparticle()
        if is_anti and self.symbol.startswith("anti-"):
            new_symbol = self.symbol[len("anti-"):]  # remove exactly one "anti-" prefix
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
        
    def as_dict(self) -> dict:
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

class Proton(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False
    ):
        super().__init__(
            color_rgb=(255, 0, 0),
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=1.67262192369e-27,
            charge=Charge.POSITIVE,
            spin=0.5,
            magnetic_moment=2.79,
            radius_m=0.84e-15,
            symbol="p+"
        )


class Neutron(Particle):
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        momentum: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        bound: bool = False
    ):
        super().__init__(
            color_rgb=(128, 128, 128),
            position=position,
            momentum=momentum,
            bound=bound,
            mass_kg=1.67492749804e-27,
            charge=Charge.NEUTRAL,
            spin=0.5,
            magnetic_moment=-1.91,
            radius_m=0.84e-15,
            symbol="n0"
        )