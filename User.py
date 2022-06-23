class User:
    def __init__(self, userId, name, email, password, mobile, latitude, longitude, role):
        self.userId = userId
        self.name = name
        self.email = email
        self.password = password
        self.mobile = mobile
        self.latitude = latitude
        self.longitude = longitude
        self.role = role

    def toDict(self):
        return {"userId": self.userId,
                "name": self.name,
                "email": self.email,
                "mobile": self.mobile,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "role": self.role}
