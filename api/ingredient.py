from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    amount: int = 0
    unit: str = ""
    prep: str = ""

    @classmethod
    def from_str(cls, s: str) -> "Ingredient":
        """
        :param s: examples:
                    name only:                    "apple"
                    amount and name:              "1, apple"
                    amount, unit and name:        "1, kg, apples"
                    amount, unit, name, and prep: "1, kg, apples; chopped"
        :return:
        """
        amount = unit = name = prep = ""

        match list(map(str.strip, s.split(";"))):
            case [""]:
                raise ParseError("empty input")
            case [s]:
                pass
            case [s, prep]:
                pass
            case _:
                raise ParseError("Too many semicolons")

        match list(map(str.strip, s.split(","))):
            case [""]:
                raise ParseError("Got prep but no ingredients")
            case [amount, name]:  # e.g. 1, apple
                pass
            case [amount, unit, name]:  # e,g. 1, kg, apples
                pass
            case [name]:
                pass
            case _:
                raise ParseError("Too many commas")

        return Ingredient(
            name=name,
            amount=_parse_number(amount),
            unit=unit,
            prep=prep,
        )


def _parse_number(number: str) -> int | float:
    if not number.strip().isdecimal():
        return 0
    if "." in number:
        return float(number)
    else:
        return int(number)


class ParseError(Exception):
    pass
