from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    amount: int = 0
    unit: str = ""
    prep: str = ""

    @classmethod
    def from_str(cls, s: str) -> "Ingredient":
        return Ingredient(**parse_ingredient_str(s))


def parse_ingredient_str(s: str) -> dict:
    """
    :param s: examples:
                name only:                    "apple"
                amount and name:              "1, apple"
                amount, unit and name:        "1, kg, apples"
                amount, unit, name, and prep: "1, kg, apples; chopped"
    :return:
    :raises: IngredientParseError
    """
    output = {}

    match list(map(str.strip, s.split(";"))):
        case [""]:
            raise IngredientParseError("empty input")
        case [s]:
            pass
        case [s, ""]:  # trailing ";" and empty prep
            pass
        case [s, prep]:  # non-empty prep
            output["prep"] = prep
        case _:
            raise IngredientParseError("Too many semicolons")

    match list(map(str.strip, s.split(","))):
        case [""]:
            raise IngredientParseError("Got prep but no ingredients")
        case [amount, name]:  # e.g. 1, apple
            if not name:
                raise IngredientParseError("empty value: name")
            if not amount:
                raise IngredientParseError("empty value: amount")
            output["name"] = name
            output["amount"] = _parse_number(amount)
        case [amount, unit, name]:  # e,g. 1, kg, apples
            output["name"] = name
            output["amount"] = _parse_number(amount)
            output["unit"] = unit
        case [name]:
            output["name"] = name
        case _:
            raise IngredientParseError("Too many commas")

    return output


class IngredientParseError(Exception):
    pass


def _parse_number(number: str) -> int | float:
    if not number.strip().isdecimal():
        return 0
    if "." in number:
        return float(number)
    else:
        return int(number)
