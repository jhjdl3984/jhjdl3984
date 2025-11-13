from marshmallow import Schema, fields

class ItemSchema(Schema):
    # dump_only=True => 서버에서 관리하겠다
    # => post맨에서 "id":"123" 이런식으로 하면 오류남
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()