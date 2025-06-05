from particles import Proton, Neutron, Electron

# IUPAC 2018
# 1 amu = 1.66053906660e-27 kg
amu = 1.66053906660e-27
reference_masses = {
    "H": 1.00784 * amu,
    "He": 4.00260 * amu,
    "Li": 6.94 * amu,
    "Be": 9.01218 * amu,
    "C": 12.0107 * amu,
    "O": 15.999 * amu,
}

# Simple atomic model with protons, neutrons, and electrons
class Atom:
    def __init__(self, symbol: str, protons: int, neutrons: int, electrons: int):
        self.symbol = symbol
        self.protons = [Proton() for _ in range(protons)]
        self.neutrons = [Neutron() for _ in range(neutrons)]
        self.electrons = [Electron() for _ in range(electrons)]

    def computed_mass(self) -> float:
        return (
            sum(p.mass_kg for p in self.protons) +
            sum(n.mass_kg for n in self.neutrons) +
            sum(e.mass_kg for e in self.electrons)
        )

    def summary(self) -> dict:
        ref = reference_masses.get(self.symbol)
        comp = self.computed_mass()
        delta_pct = 100 * abs(comp - ref) / ref if ref else None
        return {
            "symbol": self.symbol,
            "Z (protons)": len(self.protons),
            "N (neutrons)": len(self.neutrons),
            "electrons": len(self.electrons),
            "computed_mass (kg)": comp,
            "reference_mass (kg)": ref,
            "delta %": delta_pct
        }

atoms = [
    Atom("H", 1, 0, 1),
    Atom("He", 2, 2, 2),
    Atom("Li", 3, 4, 3),
    Atom("Be", 4, 5, 4),
    Atom("C", 6, 6, 6),
    Atom("O", 8, 8, 8),
]

print(f"{'Atom':^6} | {'Z':^3} | {'N':^3} | {'e-':^3} | {'Computed mass (kg)':^20} | {'Ref. mass (kg)':^20} | {'Δ %':^6}")
print("-" * 80)

for atom in atoms:
    s = atom.summary()
    print(f"{s['symbol']:^6} | {s['Z (protons)']:^3} | {s['N (neutrons)']:^3} | {s['electrons']:^3} | "
          f"{s['computed_mass (kg)']:.4e}     | {s['reference_mass (kg)']:.4e}     | {s['delta %']:.2f}")

