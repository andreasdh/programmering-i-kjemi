def dilution(initial_concentration, initial_volume, final_volume):
    final_concentration = (
        initial_concentration * initial_volume / final_volume
    )
    dilution_factor = final_volume / initial_volume
    amount_moles = initial_concentration * initial_volume / 1000

    return final_concentration, dilution_factor, amount_moles


concentration, factor, amount = dilution(0.50, 10.0, 100.0)

print(f"Final concentration: {concentration:.3f} mol/L")
print(f"Dilution factor: {factor:.0f}")
print(f"Amount of substance: {amount:.4f} mol")
