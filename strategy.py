from abc import ABC,abstractmethod

class validatestrategy(ABC):
    @abstractmethod
    def validate(self,data:str)->bool:
        pass

class emailvalidation(validatestrategy):
    def validate(self,data:str)->bool:
        return "@" in data
    
class passwordvalidation(validatestrategy):
    def validate(self, data:str)->bool:
        return len(data)>=8 and any(c.isdigit() for c in data)
    

class Validate():
    def __init__(self,strategy:validatestrategy):
        self.strategy=strategy

    def is_valid(self,data:str)->bool:
        return self.strategy.validate(data)
  
