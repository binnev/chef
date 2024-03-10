"""
Handles normalising and converting between units.
"""

Number = int | float


def normalise(amount: Number, unit: str) -> tuple[Number, str]:
    """
    Converts an amount + unit into the preferred internal format (grams or
    millilitres) if possible

    Handles:
        - alias: (pounds -> lb)
        - system (imperial -> metric): (lb -> kg)
        - denomination: (5kg -> 5000g)

    Args:
        amount: the input amount e.g. 2.5
        unit: the input unit e.g. "kilos"

    Returns:
        The converted amount and unit
    """
    unit = unit.lower()
    unit = SINGULARS.get(unit, unit)
    unit = PREFERRED_ALIASES.get(unit, unit)
    multiplier, internal_unit = CONVERSIONS.get(unit, (1, unit))
    return amount * multiplier, internal_unit


# These are the units we will use internally. I've chosen the smallest metric
# denomination so that we can use integers.
GRAM = "g"
ML = "ml"
TSP = "tsp"
INTERNAL_UNITS = {GRAM, ML, TSP}

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
    TSP: ["teaspoon", "teaspoons", "tsps"],
    "tbsp": ["tbsps", "tablespoon", "tablespoons"],
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
    TSP: (1, TSP),
    "kg": (1000, GRAM),
    "l": (1000, ML),
    "oz": (28, GRAM),
    "lb": (454, GRAM),
    "cup": (240, ML),
    "fl oz": (30, ML),
    "tbsp": (3, TSP),
}

# singular to the left; plural to the right
PLURALS = {
    "clove": "cloves",  # of garlic
    "sprig": "sprigs",
}
SINGULARS = {plural: singular for singular, plural in PLURALS.items()}
