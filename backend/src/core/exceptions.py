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