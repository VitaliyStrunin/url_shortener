class ImpossibleToAddURL(Exception):
    def __init__(self, reason: str):
            self.message = f"Impossible to add the url. Reason: {reason}"
            super().__init__(self.message)         
        
class ShortURLNotFoundByID(Exception):
    def __init__(self, id: int):
            self.message = f"URL with ID {id} not found"
            super().__init__(self.message)
            
class ShortURLNotFoundByCode(Exception):
    def __init__(self, code: str):
        self.message = f"URL with code {code} not found"
        super().__init__(self.message)
    
    
class UserAlreadyExists(Exception):
    def __init__(self, username: str):
        self.message = f"User with username {username} already exists"
        super().__init__(self.message)
    
    
class UserNotFound(Exception):
    def __init__(self, key: str):
        self.message = f"User with username {key} already exists"
        super().__init__(self.message)
    