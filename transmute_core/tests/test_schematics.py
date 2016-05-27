import pytest
from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.types.compound import DictType


class Card(Model):
    name = StringType()
    price = IntType()

card_dict = {"name": "foo", "price": 10}
card = Card(card_dict)


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card, card_dict),
    ([Card], [card], [card_dict])
])
def test_schematics_integration_dump(serializer, typ, inp, out):
    assert serializer.dump(typ, inp) == out


@pytest.mark.parametrize("typ,inp,out", [
    (Card, card_dict, card),
    ([Card], [card_dict], [card])
])
def test_schematics_integration_load(serializer, typ, inp, out):
    assert serializer.load(typ, inp) == out


def test_schematics_to_json_schema(serializer):
    assert serializer.to_json_schema(Card) == {
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"}
        },
        "title": "Card",
        "type": "object"
    }


def test_schematics_to_json_schema_required_value(serializer):

    class CardNameRequired(Model):
        name = StringType(required=True)
        price = IntType()

    assert serializer.to_json_schema(CardNameRequired) == {
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number"}
        },
        "title": "CardNameRequired",
        "required": ["name"],
        "type": "object"
    }


def test_to_json_list(serializer):
    assert serializer.to_json_schema([int]) == {
        "type": "array",
        "items": {"type": "number"}
    }


def test_to_json_dict(serializer):
    assert serializer.to_json_schema(DictType(IntType())) == {
        "type": "object",
        "additionalProperties": {"type": "number"}
    }


def test_serialize_type(serializer):
    """ serializer should be able to serialize a raw type. """
    assert serializer.dump(DictType(StringType()), {"key": "foo"}) == {"key": "foo"}
