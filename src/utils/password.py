import bcrypt


class Password:
    def hash(password):
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())

    def compare(password, hash):
        return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))