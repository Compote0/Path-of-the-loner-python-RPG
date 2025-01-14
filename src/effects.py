import random

def apply_effect(target, effect):
    """
    Applies a status effect to a target.
    
    Args:
        target: The target to apply the effect to.
        effect: The status effect to apply.
    """
    if effect == "frozen":
        target["status"] = "Frozen"
        print(f"{target['name']} is frozen and cannot act!")
    elif effect == "stunned":
        target["status"] = "Stunned"
        print(f"{target['name']} is stunned and skips their turn!")
    elif effect == "bleed":
        target["status"] = "Bleeding"
        target["hp"] -= 5  # Bleeding inflicts constant damage
        print(f"{target['name']} is bleeding and loses 5 HP!")
    else:
        target["status"] = None
        print(f"{target['name']} is in a normal state.")

def random_effect():
    """
    Generates a random status effect.
    
    Returns:
        str: The randomly chosen status effect or None.
    """
    return random.choice(["frozen", "stunned", "bleed", None])
