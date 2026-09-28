def normalize_result(data):
    aliases={'POLYETHYLENE':'PE','POLYPROPYLENE':'PP','POLYSTYRENE':'PS','POLYETHYLENE TEREPHTHALATE':'PET','POLYVINYL CHLORIDE':'PVC','POLYAMIDE':'PA','NYLON':'PA'}
    for e in data.get('experiments',[]):
        p=e.get('polymer')
        if isinstance(p,str): e['polymer']=aliases.get(p.strip().upper(),p.strip())
    return data
