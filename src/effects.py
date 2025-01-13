def apply_effect(target, effect):
    if effect == "frozen":
        target["status"] = "Gelé"
        print(f"{target['name']} est gelé et ne peut pas agir !")
    elif effect == "stunned":
        target["status"] = "Étourdissant"
        print(f"{target['name']} est étourdi et saute son tour !")
