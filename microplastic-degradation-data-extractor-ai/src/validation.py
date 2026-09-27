def validate_result(result: dict):
    errors, warnings = [], []
    for i, exp in enumerate(result.get("experiments", []), start=1):
        temp = exp.get("temperature_c")
        if temp is not None and temp < -273.15:
            errors.append(f"Experiment {i}: temperature below absolute zero.")
        ph = exp.get("pH")
        if ph is not None and not 0 <= ph <= 14:
            warnings.append(f"Experiment {i}: unusual pH ({ph}). Verify source.")
        initial, final = exp.get("initial_mass_mg"), exp.get("final_mass_mg")
        if initial is not None and final is not None:
            if initial < 0 or final < 0:
                errors.append(f"Experiment {i}: negative mass.")
            if final > initial:
                warnings.append(f"Experiment {i}: final mass > initial mass; verify sampling/residue context.")
        for ep in exp.get("endpoints", []):
            value = ep.get("value")
            typ = ep.get("endpoint_type")
            if value is not None and typ in {
                "mass_loss", "toc_removal", "mineralization",
                "molecular_weight_reduction", "particle_size_reduction"
            } and not 0 <= value <= 100:
                errors.append(f"Experiment {i}: {typ} is outside 0–100%.")
    return errors, warnings
