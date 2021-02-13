import datetime
class Address:
    def __init__(self,city:str,street:str,number:int):
        self.city=city
        self.street=street
        self.number=number

class Home(Address):
    def __init__(self,city:str,street:str,number:int,apartment_number:int,house_residents:int) -> None:
        super().__init__(city,street,number)
        self.apartment_number=apartment_number
        self.house_residents=house_residents


class Site:
    def __init__(self,siteName,city:str=None,street:str=None,number:int=None) -> None:
        self.siteName=siteName
        self.siteAddress=Address(city,street,number) if city and street and number else None

class Person:
    def __init__(self,phone:str,firstName:str,surName:str,id:int=None,birthdate:datetime.date=None,mail:str=None,address:Home=None,sick:bool=False,isolation_begin_date:datetime.date=None) -> None:
        self.phone=phone # key value
        self.firstName=firstName
        self.surName=surName
        self.id=id 
        self.birthdate=birthdate
        self.mail=mail
        self.address=address
        self.sick=sick
        self.isolation_begin_date=isolation_begin_date
        self.infected_by=None
        pass
    
    def send_to_isolation(self):
        self.isolation_begin_date=datetime.datetime.now().date
    
    def update_person_params(self,id:int=None,birthdate:datetime.date=None,mail:str=None,address:Home=None,sick:bool=False,isolation_begin_date:datetime.date=None):
        self.id=id 
        self.birthdate=birthdate
        self.mail=mail
        self.address=address
        self.sick=sick
        self.isolation_begin_date=isolation_begin_date
    
    def set_infected_by(self,infected_by):
        self.infected_by=infected_by # instance of Person(self) type
