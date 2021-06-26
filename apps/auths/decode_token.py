import jwt


def decode_token(token):
    try:
        decoded_token = jwt.decode(
            token,
            "temporalSecret",
            algorithms="HS256",
        )
    except jwt.exceptions.DecodeError:
        return False
    return decoded_token
