import jwt

class JWTUtils:
    @staticmethod
    def encode(body):
        return jwt.encode(payload=body, key="5r@gldmj+p3wp0%k)wdy70x+_7g^aei35i5%vf@$57u51f1buw")

    @staticmethod
    def decode(token):
        return jwt.decode(jwt=token, key="5r@gldmj+p3wp0%k)wdy70x+_7g^aei35i5%vf@$57u51f1buw", algorithms=['HS256'])