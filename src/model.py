import datetime


class Address:
    def __init__(self, city: str, street: str, number: int):
        self.city = city
        self.street = street
        self.number = number


class Home(Address):
    def __init__(self, city: str, street: str, number: int, apartment_number: int, house_residents: int) -> None:
        super().__init__(city, street, number)
        self.apartment_number = apartment_number
        self.house_residents = house_residents


class Site:
    def __init__(self, siteName, address:Address=None) -> None:
        self.siteName = siteName
        self.siteAddress = address # decoupling, in case address will add floor (for example), site won't be affected


class Person:
    def __init__(self, phone: str, firstName: str, surName: str, id: int = None, birthdate: datetime = None,
                 mail: str = None, home: Home = None, sick: bool = None, 
                 isolation_begin_date: datetime = None) -> None:
        self.phone = phone 
        self.firstName = firstName
        self.surName = surName
        self.id = id
        self.birthdate = birthdate
        self.mail = mail
        self.home = home
        self.sick = sick
        self.isolation_begin_date = isolation_begin_date
        pass

    def send_to_isolation(self):
        self.isolation_begin_date = datetime.datetime.now()

class Laboratory:
    #test_counter = 0

    def __init__(self,lab_id):
        self.lab_id = lab_id


class Test:
    def __init__(self, person: Person, lab: Laboratory,test_id, result_date: datetime = None,
                 test_result: bool = None):

        self.test_result = test_result
        self.person = person
        self.lab = lab
        self.test_id = test_id
        self.result_date = result_date

    def update_test_result(self, test_result: bool, result_date: datetime = datetime.datetime.now()):
        self.test_result = test_result
        self.result_date = result_date


class Suspect(Person):
    class_counter = 0
    def __init__(self, infector: Person, phone: str, firstName: str, surName: str):
        super().__init__(phone, firstName, surName,isolation_begin_date=datetime.datetime.now())  # calling base class constructor and updating isolation date
        self.encounter_id = Suspect.class_counter
        Suspect.class_counter += 1
        self.infector = infector

    def update_suspect_params(self, id: int = None, birthdate: datetime = None, mail: str = None,
                              address: Home = None, sick: bool = False, isolation_begin_date: datetime = None):
        self.id = id
        self.birthdate = birthdate
        self.mail = mail
        self.address = address
        self.sick = sick
        self.isolation_begin_date = isolation_begin_date



class SickInSite:
    def __init__(self, sick: Person, site:Site, visit_datetime: datetime):
        if hasattr(sick,'sick'):
            self.sick = sick
            self.site = site
            self.visit_datetime = visit_datetime
        else:
            raise Exception("SickInSite: person must be sick")
