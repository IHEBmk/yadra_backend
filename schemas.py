from marshmallow import Schema, fields, validate
from werkzeug.utils import secure_filename

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[
        validate.Length(min=8),
        validate.Regexp(r"(?=.*\d)", error="Password must include at least one number")
    ])
    name = fields.String(required=True, validate=validate.Length(min=2, max=50))
    phone = fields.String(validate=validate.Regexp(r"^\+?[0-9]\d{1,14}$", error="Invalid phone number format"), allow_none=True)
    role = fields.Integer()
    company_id = fields.String()
    branch_id = fields.String()
    avatar = fields.String()

    



class ReviewSchema(Schema):
    branch_id = fields.UUID(required=True)
    rating = fields.Dict(
        keys=fields.String(validate=validate.Length(min=1)),
        values=fields.Integer(validate=validate.Range(min=1, max=5)),
        required=True
    )
    content = fields.String(required=True, validate=validate.Length(min=10, max=1000))
    is_anonymous = fields.Boolean(missing=False)
    purchase_date = fields.Date(allow_none=True)
    media = fields.List(fields.Raw(), validate=validate.Length(max=5), required=False)
    tags = fields.List(fields.String(validate=validate.Length(min=1)), validate=validate.Length(max=5), required=False)

# Media validation function
def validate_media_files(media_files):
    errors = []
    max_file_size_mb = 1
    allowed_types = {"image/jpeg", "image/png", "image/gif"}

    for file in media_files:
        file_type = file.content_type
        file_size_mb = len(file.read()) / (1024 * 1024)  
        file.seek(0)  

        if file_type not in allowed_types:
            errors.append(f"Invalid file type: {file_type}. Only images are allowed.")
        if file_size_mb > max_file_size_mb:
            errors.append(f"File {secure_filename(file.filename)} exceeds the size limit of {max_file_size_mb}MB.")
    
    return errors