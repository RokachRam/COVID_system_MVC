from abc import ABC, abstractmethod
from model import *
from typing import List
debug=True
class IDataAccess:
    """
    "DLA" == data layer access
    "CRUD"== Create, Read, Update and Delete
    This interface class is responsible of containing the different modules.
    it can be implemented using different databases (python,MySQL, MSSQL,etc..)
    """
    @abstractmethod
    def create_patient(self, phone, firstName, surName, id=None, birthdate:datetime=None,mail=None, city=None,street=None,num=None,apt_num=None,house_resdients=None, sick=None, interviewed=None, isolation_begin_date=None):
        pass
    @abstractmethod
    def create_sick_in_site(self,sick_id,site_name,date_in_site,city=None,street=None,number=None):
        pass
    @abstractmethod
    def create_sick_encounter(self,sick_id,first_name,last_name,phone):
        pass
    
    @abstractmethod
    def create_test(self,test:Test):
        pass

    @abstractmethod
    def read_list_of_patients(self):
        pass

    @abstractmethod
    def read_list_of_sick_in_site(self):
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def read_list_of_tests(self):
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def update_test_result(self,test_id,lab_id,person_id,result_date:datetime,result:True):
        """
        return True if success, else False
        """
        pass

    @abstractmethod
    def update_patient(self,person:Person):
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def update_sick_encounter_details(self,encounter_id, person_id,first_name,sur_name,birth_date,phone,mail,city,street,number,apart_num,house_residents):
        """
        return True if success, else False
        """
        pass
    @abstractmethod
    def delete_patient_by_id(self, person_id) -> bool:
        pass
    @abstractmethod
    def delete_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int)-> bool:
        pass

    @abstractmethod
    def get_person_by_id(self, id: int) -> Person:
        pass




    


class PythonDataAccess(IDataAccess):
    def __init__(self) -> None:
        self.list_of_patients: List[Person] = [] 
        self.list_of_sick_in_Site : List[SickInSite]=[]
        self.list_of_tests : List[Test]=[]
    
    
    def create_patient(self, phone, firstName, surName, id=None, birthdate:datetime=None,mail=None, city=None,street=None,num=None,apt_num=None,house_resdients=None, sick=None, interviewed=None, isolation_begin_date=None):
        self.delete_patient_by_id(id)
        home=Home(city,street,num,apt_num,house_resdients)
        person=Person(phone, firstName, surName, id, birthdate,mail, home, sick, interviewed, isolation_begin_date)
        self.list_of_patients.append(person)
        return True
        
    def create_sick_in_site(self,sick_id,site_name,date_in_site,city=None,street=None,number=None):
        sick_person=self.get_person_by_id(sick_id)
        if not sick_person:
            return False
        if (city and street and number):
            address=Address(city,street,number)
            site=Site(site_name,address)
        elif not (city or street or number):
            site=Site(site_name)
        else: 
            return False
        
        route_site = SickInSite(sick_person, site, date_in_site)
        self.list_of_sick_in_Site.append(route_site)
        return True
    
    def create_sick_encounter(self,sick_id,first_name,last_name,phone):
        if not self.get_person_by_id(sick_id):
            return False # sick not found
        self.create_patient(phone,first_name,last_name)
        return True

    def create_test(self,test:Test):
        if isinstance(test,Test):
            self.list_of_tests.append(test)
            return True
        return False

    def read_list_of_patients(self):
        return self.list_of_patients

    def read_list_of_sick_in_site(self):
        return self.list_of_sick_in_Site

    def read_list_of_tests(self):
        return self.list_of_tests

    def update_test_result(self,test_id,lab_id,person_id,result_date:datetime,result:True):
        for lab_test in self.list_of_tests:
            if (lab_test.test_id == test_id and lab_test.lab.lab_id == lab_id and lab_test.person.id == person_id):
                self.delete_test_by_test_id_and_lab_id(lab_test.test_id,lab_test.lab.lab_id)
                lab_test.result_date=result_date
                lab_test.test_result=result
                return self.create_test(lab_test)

    def update_patient(self,person:Person):
        person_id=person.id
        for i_person in self.list_of_patients:
            if i_person.id == person_id:
                self.list_of_patients.remove(i_person)
                self.list_of_patients.append(person)
                return True
        return False
        
    def update_sick_encounter_details(self,encounter_id, person_id,first_name,sur_name,birth_date,phone,mail,city,street,number,apart_num,house_residents):
        if not self.get_suspect_by_encounter_id(encounter_id):
            return False
        self.container.delete_patient_by_id(person_id)
        self.create_patient(self, phone, first_name, sur_name, person_id,birth_date,mail, city,street,number,apart_num,house_residents)
        return True
    
    def delete_patient_by_id(self, person_id) -> bool:
        for person in self.list_of_patients:
            if person.id == person_id:
                self.list_of_patients.remove(person)
        return True 

    def delete_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int)-> bool:
        for test in self.list_of_tests:
            if test.test_id == test_id and test.lab_id == lab_id:
                self.read_list_of_tests.remove(test)
        return True

    def get_person_by_id(self, id: int) -> Person:
        for person in self.list_of_patients:
            if id == person.id:
                return person

    def get_suspect_by_encounter_id(self, encounter_id: int) -> Suspect:
        for suspect in self.list_of_patients:
            if hasattr(suspect, 'encounter_id'):
                if suspect.encounter_id == encounter_id:
                    return suspect

    def get_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int):
        for test in self.list_of_tests:
            if test.test_id == test_id and test.lab_id == lab_id:
                return test
