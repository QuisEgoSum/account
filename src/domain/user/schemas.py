from qstd_core.marshmallow import Schema, fields


class RegisterSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
