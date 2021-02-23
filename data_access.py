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
    def create_patient(self, phone, firstName, surName, id=None, birthdate:datetime=None,mail=None, city=None,street=None,num=None,apt_num=None,house_resdients=None, sick=None,  isolation_begin_date=None):
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

    @abstractmethod
    def read_list_of_sick(self):
        pass




    


class PythonDataAccess(IDataAccess):
    def __init__(self) -> None:
        self.list_of_patients: List[Person] = [] 
        self.list_of_sick_in_Site : List[SickInSite]=[]
        self.list_of_tests : List[Test]=[]
    
    
    def create_patient(self, phone, firstName, surName, id=None, birthdate:datetime=None,mail=None, city=None,street=None,num=None,apt_num=None,house_resdients=None, sick=None,  isolation_begin_date=None):
        self.delete_patient_by_id(id)
        home=Home(city,street,num,apt_num,house_resdients)
        person=Person(phone, firstName, surName, id, birthdate,mail, home, sick, isolation_begin_date)
        self.list_of_patients.append(person)
        return person
        
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
        return route_site
    
    def create_sick_encounter(self,sick_id,first_name,last_name,phone):
        infector=self.get_person_by_id(sick_id)
        if not infector:
            return False # sick not found
        sick_encounter=Suspect(infector,phone,first_name,last_name)
        self.list_of_patients.append(sick_encounter)
        return sick_encounter

    def create_test(self,test_id,lab_id,person_id,result_date:datetime,result:bool=None):
        isolation_period = 14
        time_now = datetime.datetime.now()
        person=self.get_person_by_id(person_id)
        if not person:
            return False # person not found
    
        test=Test(person,Laboratory(lab_id),test_id,result_date,result)
        # update person isolation date if neccesary
        if result and (not person.isolation_begin_date or result_date>person.isolation_begin_date): # if result is positive AND (current isolatin date > result date OR doesnt have an isolation date)
            person.isolation_begin_date=result_date
            # self.update_patient(person)
        ##
        self.list_of_tests.append(test)
        return test

    def read_list_of_patients(self):
        return self.list_of_patients

    def read_list_of_sick_in_site(self):
        return self.list_of_sick_in_Site

    def read_list_of_tests(self):
        return self.list_of_tests

    def update_test_result(self,test_id,lab_id,person_id,result_date:datetime,result:bool):
        return self.create_test(test_id,lab_id,person_id,result_date,result)

    def update_patient(self,person:Person):
        person_id=person.id
        for i_person in self.list_of_patients:
            if i_person.id == person_id:
                self.list_of_patients.remove(i_person)
                self.list_of_patients.append(person)
                return True
        return False
        
    def update_sick_encounter_details(self,encounter_id, person_id,first_name,sur_name,birth_date,phone,mail,city,street,number,apart_num,house_residents):
        """
        Suspect == sick encountered
        Update sick-encountered's empty values.
        If the suspect wasn't found by encounter_id the function returns False
        """
        suspect = self.get_suspect_by_encounter_id(encounter_id)
        if not suspect:
            return False # "encounter_id not found"
        self.list_of_patients.remove(suspect)
        home = Home(city, street, number, apart_num, house_residents)
        suspect.id = person_id
        suspect.phone=phone
        suspect.firstName = first_name
        suspect.surName = sur_name
        suspect.birthdate = birth_date
        suspect.mail = mail
        suspect.home = home
        self.list_of_patients.append(suspect)
        
        return suspect
    
    def delete_patient_by_id(self, person_id) -> bool:
        for person in self.list_of_patients:
            if person.id == person_id:
                self.list_of_patients.remove(person)
                return True
        return False

    def delete_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int)-> bool:
        """
        test_id and lab_id are together a key
        """
        for test in self.list_of_tests:
            if test.test_id == test_id and test.lab.lab_id == lab_id:
                self.list_of_tests.remove(test)
                return True
        return False

    def get_person_by_id(self, id: int) -> Person:
        for person in self.list_of_patients:
            if person.id and int(id) == int(person.id):
                return person

    def get_suspect_by_encounter_id(self, encounter_id: int) -> Suspect:
        """
        Suspect == sick encountered 
        """
        for suspect in self.list_of_patients:
            if hasattr(suspect, 'encounter_id'):
                if (int(suspect.encounter_id) == int(encounter_id)):
                    return suspect

    def get_test_by_test_id_and_lab_id(self,test_id:int,lab_id:int):
        """
        test_id and lab_id are together a key
        """
        for test in self.list_of_tests:
            if int(test.test_id) == test_id and int(test.lab_id) == lab_id:
                return test

    def read_list_of_sick(self):
        """
        sick person is somebody who answers at least one of the following:
        1. Has a positive COVID test.
        2. Was inserted by a nurse with "create-sick" command and didn't get a negative test result.
        """
        list_of_sick =[]
        for test in self.read_list_of_tests(): # this loop assures that if there's a new negative test for someone - he's not sick anymore
            if test.test_result == True:
                for test2 in self.read_list_of_tests():
                    if test.person.id == test2.person.id and test.result_date < test2.result_date and not test2.test_result:
                        break
                    if test.person not in list_of_sick:
                        list_of_sick.append(test.person)
        for person in self.read_list_of_patients():  # deals with sick person who got inserted to the list of sick via 'create-sick'
            if person.sick and (person not in list_of_sick):
                list_of_sick.append(person)
        return list_of_sick