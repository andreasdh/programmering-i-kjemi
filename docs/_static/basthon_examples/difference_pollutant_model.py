import matplotlib.pyplot as plt

input_per_year = 20.0
removal_fraction = 0.12
years = 40

mass = 0.0
values = [mass]

for year in range(years):
    mass = mass + input_per_year - removal_fraction*mass
    values.append(mass)

plt.plot(range(years + 1), values)
plt.xlabel("Year")
plt.ylabel("Pollutant mass (kg)")
plt.show()
