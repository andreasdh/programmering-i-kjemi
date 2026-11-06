import matplotlib.pyplot as plt

temperature_C = [16, 18, 20, 22, 24]
vapor_pressure_kPa = [1.817, 2.063, 2.339, 2.644, 2.984]

plt.scatter(temperature_C, vapor_pressure_kPa, color="#176b87", s=55, label="Measurements")
plt.xlabel("Temperature (°C)")
plt.ylabel("Vapor pressure (kPa)")
plt.title("Vapor pressure of water")
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()
