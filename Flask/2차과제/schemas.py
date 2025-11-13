from marshmallow import Schema, fields

class BookSchema(Schema):
    # dump_only => 응답검증에서만 사용됨
    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
