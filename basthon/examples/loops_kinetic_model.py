rate_constant = 0.15      # s^-1
concentration_A = 1.00    # mol/L
concentration_B = 0.00    # mol/L
time_step = 0.10          # s
end_time = 10             # s

number_of_steps = int(end_time / time_step)

for step in range(number_of_steps):
    change = rate_constant * concentration_A * time_step
    concentration_A = concentration_A - change
    concentration_B = concentration_B + change

print(f"After {end_time} s, [A] = {concentration_A:.3f} mol/L.")
print(f"After {end_time} s, [B] = {concentration_B:.3f} mol/L.")
print(f"Total concentration: {concentration_A + concentration_B:.3f} mol/L.")
