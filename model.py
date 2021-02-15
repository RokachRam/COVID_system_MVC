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
    def __init__(self, siteName, address:Address) -> None:
        self.siteName = siteName
        self.siteAddress = address # decoupling, in case address will add floor (for example), site won't be affected


class Person:
    def __init__(self, phone: str, firstName: str, surName: str, id: int = None, birthdate: datetime.date = None,
                 mail: str = None, address: Home = None, sick: bool = None, interviewed:bool = False,
                 isolation_begin_date: datetime.date = None) -> None:
        self.phone = phone  # key value
        self.firstName = firstName
        self.surName = surName
        self.id = id
        self.birthdate = birthdate
        self.mail = mail
        self.address = address
        self.sick = sick
        self.interviewed = interviewed
        self.isolation_begin_date = isolation_begin_date
        self.infected_by = None
        pass

    def send_to_isolation(self):
        self.isolation_begin_date = datetime.datetime.now().date

    def set_infected_by(self, infected_by):
        self.infected_by = infected_by  # instance of Person(self) type


class Laboratory:
    class_counter = 0

    def __init__(self):
        self.labId = Laboratory.class_counter
        Laboratory.class_counter += 1

    pass


class Test:
    class_counter = 0

    def __init__(self, person: Person, lab: Laboratory, test_date: datetime.date, result_date: datetime.date = None,
                 test_result: bool = None):
        self.test_id = Test.class_counter
        Test.class_counter += 1
        self.test_result = test_result
        self.person = person
        self.lab = lab
        self.test_date = test_date
        self.result_date = result_date
        pass

    def update_test_result(self, test_result: bool, result_date: datetime.date = datetime.datetime.now().date):
        self.test_result = test_result
        self.result_date = result_date
        pass


class Suspect(Person):
    class_counter = 0
    def __init__(self, infector: Person, phone: str, firstName: str, surName: str):
        super().__init__(phone, firstName, surName)  # calling base class constructor
        self.encounter_id = Suspect.class_counter
        Suspect.class_counter += 1
        self.infector = infector

    def update_suspect_params(self, id: int = None, birthdate: datetime.date = None, mail: str = None,
                              address: Home = None, sick: bool = False, isolation_begin_date: datetime.date = None):
        self.id = id
        self.birthdate = birthdate
        self.mail = mail
        self.address = address
        self.sick = sick
        self.isolation_begin_date = isolation_begin_date

    def is_suspect_infected_by_someone(self):
        return self.sick # a suspect is a suspect because a sick person potentially infected him, if he got sick -
                         # it's because of him


class SickInSite:
    def __init__(self, sick: Person, site:Site, visit_datetime: datetime):
        if sick.sick:
            self.sick = sick
            self.site = site
            self.visit_datetime = visit_datetime
        else:
            raise Exception("The person must be sick")
