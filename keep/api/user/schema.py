register_schema = {
    "type": "object",
    "properties": {
        "email":   {
            "type": "string",
            "pattern": "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        },
        "password": {
            "type": "string",
            "minLength": 6
        },
        "tokens": {
            "type": "array",
            "items": [
                {"access": {"type": "string"}},
                {"token": {"type": "string"}}
            ]
        }
    },
    "required": ["email", "password"]
}

login_schema = {
    "type": "object",
    "properties": {
        "email":   {
            "type": "string",
            "pattern": "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        },
        "password": {
            "type": "string",
            "minLength": 6
        }
    },
    "required": ["email", "password"]
}
