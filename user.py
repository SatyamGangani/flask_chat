from werkzeug.security import check_password_hash
class User:
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username
    
    def is_password_valid(self,password_to_verify):
        return check_password_hash(self.password,password_to_verify)