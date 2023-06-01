from marshmallow import fields, validate


class Types(object):
    class UUID(fields.UUID):
        pass

    class Integer(fields.Integer):
        pass

    class String(fields.String):
        pass

    class Date(fields.Date):
        pass

    class Email(fields.Email):
        pass

    class Devices(fields.List):
        pass

    class Boolean(fields.Boolean):
        pass

    class List(fields.List):
        pass

    class Counter(fields.Integer):
        pass

    class Nested(fields.Nested):
        pass

    class Dict(fields.Dict):
        pass

    class Float(fields.Float):
        pass