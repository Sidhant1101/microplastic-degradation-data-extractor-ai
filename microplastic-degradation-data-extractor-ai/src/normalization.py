POLYMERS = {
    "polyethylene": "PE", "pe": "PE",
    "polypropylene": "PP", "pp": "PP",
    "polystyrene": "PS", "ps": "PS",
    "polyethylene terephthalate": "PET", "pet": "PET",
    "polyvinyl chloride": "PVC", "pvc": "PVC",
    "polyamide": "PA", "nylon": "PA", "pa": "PA",
}
TREATMENTS = {
    "photocatalysis": "photocatalysis",
    "photocatalytic degradation": "photocatalysis",
    "photodegradation": "photodegradation",
    "biodegradation": "biological",
    "enzymatic degradation": "enzymatic",
    "plasma treatment": "plasma",
    "plasma": "plasma",
    "thermal degradation": "thermal",
    "hydrolysis": "hydrolysis",
    "advanced oxidation": "AOP",
    "aop": "AOP",
}

def normalize_result(result: dict) -> dict:
    result = dict(result)
    for exp in result.get("experiments", []):
        if isinstance(exp.get("polymer"), str):
            raw = exp["polymer"].strip().lower()
            exp["polymer"] = POLYMERS.get(raw, exp["polymer"])
        if isinstance(exp.get("treatment_category"), str):
            raw = exp["treatment_category"].strip().lower()
            exp["treatment_category"] = TREATMENTS.get(raw, exp["treatment_category"])
        if exp.get("duration_h") is not None:
            exp["duration_days"] = exp["duration_h"] / 24
        for ep in exp.get("endpoints", []):
            if ep.get("endpoint_type") == "mass_loss" and ep.get("value") is not None and exp.get("duration_h"):
                ep["rate_percent_day"] = ep["value"] / (exp["duration_h"] / 24)
    return result
