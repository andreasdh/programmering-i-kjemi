elements = {
    "hydrogen": {
        "symbol": "H",
        "atomic_mass": 1.008,
        "melting_point": -259.16,
    },
    "vanadium": {
        "symbol": "V",
        "atomic_mass": 50.942,
        "melting_point": 1910,
    },
}

print("Available elements:", list(elements.keys()))
print("Hydrogen data:", elements["hydrogen"])
print("Vanadium atomic mass:", elements["vanadium"]["atomic_mass"])

for name, properties in elements.items():
    print(name, "->", properties)
