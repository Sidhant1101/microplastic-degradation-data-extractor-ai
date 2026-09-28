def validate_result(data):
    errors=[]; warnings=[]; experiments=data.get('experiments',[])
    if not experiments: warnings.append('No experiments were extracted from the paper.')
    for i,e in enumerate(experiments,1):
        if not e.get('polymer'): warnings.append(f'Experiment {i}: polymer is missing.')
        if not e.get('treatment_category'): warnings.append(f'Experiment {i}: treatment category is missing.')
        if e.get('initial_mass_mg') is not None and e.get('final_mass_mg') is not None and e['final_mass_mg']>e['initial_mass_mg']: warnings.append(f'Experiment {i}: final mass is greater than initial mass.')
    return errors,warnings
