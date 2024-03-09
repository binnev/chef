def normalise(amount: int | float, unit: str) -> tuple[int | float, str]:
    """
    Converts an amount + unit into the preferred internal format (grams or
    millilitres)

    Should handle:
    - alias (pounds -> lb)
    - system (imperial -> metric) (lb -> kg)
    - denomination (5kg -> 5000g)
    """
    preferred_alias = PREFERRED_ALIASES.get(unit.lower(), unit.lower())
    try:
        multiplier, internal_unit = CONVERSIONS[preferred_alias]
    except KeyError:
        msg = f"Could not normalise {amount} {unit}!"
        raise UnitError(msg)

    return amount * multiplier, internal_unit


# These are the units we will use internally. I've chosen the smallest metric
# denomination so that we can use integers.
GRAM = "g"
ML = "ml"
INTERNAL_UNITS = {GRAM, ML}


# The preferred alias is the key, the alternatives are the value
ALIASES = {
    GRAM: ["gram", "grams", "gs", "gr"],
    ML: [
        "millilitre",
        "millilitres",
        "milliliter",
        "milliliters",
        "mls",
    ],
    "kg": ["kilo", "kilos", "kgs", "kilogram", "kilograms"],
    "l": ["litre", "litres", "liter", "liters", "L"],
    "lb": ["pound", "pounds", "lbs"],
    "oz": ["ounce", "ounces"],
    "cup": ["cups"],
    "fl oz": ["fluid ounce", "fluid ounces"],
}
PREFERRED_ALIASES = {
    alternative: preferred
    for preferred, alternatives in ALIASES.items()
    for alternative in alternatives
}

# Here we relate every unit to our base units of weight and volume (g, ml)
CONVERSIONS = {
    GRAM: (1, GRAM),
    ML: (1, ML),
    "kg": (1000, GRAM),
    "l": (1000, ML),
    "oz": (28, GRAM),
    "lb": (454, GRAM),
    "cup": (240, ML),
    "fl oz": (30, ML),
}


class UnitError(Exception):
    pass
