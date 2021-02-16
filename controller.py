from model import *
from view import Interface_View
from data_access import IDataAccess
from typing import List
import sys
debug = False
if "-d" in sys.argv:
    debug = True


class Controller:
    def __init__(self, view: Interface_View,container:IDataAccess):
        self.view = view
        self.container=container # can be a DB, can be pythonish, can be anything. must support all IDataAccess functions
        self.list_of_new_patients: List[Person]= []
        
        pass

    def start(self):
        while True:
            # ["Create-sick" "id" "firstname" "lastname" "birthdate" "phone" "mail" "city" "street" "house-number" "apartment" "house-residents"]
            option: list = self.view.get_option_input().split()
            failed_msg = None
            if not option:
                failed_msg='no command inserted'
                self.view.operation_failed(failed_msg)
                continue
            if option[0] == 'Create-sick':
                self.create_sick(option[1:])
                self.view.create_sick()
            elif option[0] == 'Add-route-site':
                self.add_route_site(option[1:])
                self.view.add_route_site()
            elif option[0] == 'Add-route-address':
                self.add_route_site(option[1:])
                self.view.add_route_address()
            elif option[0] == 'Add-sick-encounter':
                if self.add_sick_encounter(option[1:]):
                    self.view.add_sick_encounter()
                else:
                    failed_msg="No infector, wrong encounter details"
            elif option[0] == 'Show-sick-encounter':
                result = self.show_sick_encounter()
                self.view.show_sick_encounter(result)
            elif option[0] == 'Update-sick-encounter-details':
                if self.update_sick_encounter_details(option[1:]):
                    self.view.update_sick_encounter_details()
                else:
                    failed_msg = "There is no such encounter / missing details"
            elif option[0] == 'Update-lab-test':
                if self.update_lab_test(option[1:]):
                    self.view.update_lab_test()
                else:
                    failed_msg = "No such test / missing details"
            elif option[0] == 'Show-new-sick':
                result = self.show_new_sick()
                self.view.show_new_sick(result)
            elif option[0] == 'Show-stat':
                result = self.show_stat(option[1:])
                self.view.show_stat(result)
            elif option[0] == 'Show-person':
                self.advanced_search()
            elif option[0] == 'Show-person-route':
                self.advanced_search()
            elif option[0] == 'Show-sick':
                self.advanced_search()
            elif option[0] == 'Show-isolated':
                self.advanced_search()
            else:
                failed_msg="unknown command"

            if failed_msg:
                self.view.operation_failed(failed_msg)

    # args: ["id" "firstname" "lastname" "birthdate" "phone" "mail" "city" "street" "house-number" "apartment" "house-residents"]
    def create_sick(self, args: list):
        # removes the person in case id is shown twice
        self.container.delete_patient_by_id(args[4])
        home = Home(args[6], args[7], args[8], args[9], args[10])
        person = Person(args[4], args[1], args[2], args[0], args[3], args[5], home,
                        sick=True, interviewed=True, isolation_begin_date=datetime.datetime.now())
        self.container.create_patient(person)
        self.list_of_new_patients.append(person) # this list reset every run of this code (used in show_new_sick)

    # args: ["id" "01/04/2020" "10:00" "sitename" optional: "city" "street" "number"]
    def add_route_site(self, args: list):
        date_time = datetime.datetime.strptime(
            args[1] + args[2], '%Y-%m-%d%H:%M')
        if len(args) == 4:
            site = Site(args[3])
        else:
            address = Address(args[4], args[5], args[6])
            site = Site(args[3], address)
        sick_person=self.container.get_person_by_id(args[0])
        route_site = SickInSite(sick_person, site, date_time)
        self.container.create_sick_in_site(route_site)

    # "sick-id" "firstname" "lastname" "phone"
    def add_sick_encounter(self, args: list):
        sick = self.container.get_person_by_id(args[0])
        if not sick:
            return False
        suspect = Suspect(sick, args[3], args[1], args[2])
        self.container.create_patient(suspect)
        return True

    # encounter-id, sick-id, sick-firstname, sick-lastname, firstname lastname phone
    def show_sick_encounter(self):
        list_to_return = []
        suspects = [x for x in self.container.read_list_of_patients if x.id == None]
        for suspect in suspects:
            string = str(suspect.encounter_id) + " " + str(suspect.infector.id) + " " + suspect.infector.firstName +\
                " " + suspect.infector.surName + " " + suspect.firstName + \
                " " + suspect.surName + " " + suspect.phone
            list_to_return.append(string)
        return list_to_return

    # encounter-id personid firstname lastname birthdate phone mail city street house-number apartment house-residents
    def update_sick_encounter_details(self, args: list):
        encounter_id = args[0]
        suspect = self.container.get_suspect_by_encounter_id(encounter_id)
        if not suspect:
            return False
        self.container.delete_patient_by_id(suspect.id)
        suspect.id = args[1]
        suspect.firstName = args[2]
        suspect.surName = args[3]
        suspect.birthdate = args[4]
        suspect.phone = args[5]
        suspect.mail = args[6]
        suspect.home = Home(args[7], args[8], args[9], args[10], args[11])
        self.container.create_patient(suspect)
        return True

    def update_lab_test(self, args: list):  # labid testid personid date result
        for lab_test in self.container.read_list_of_tests:
            if (lab_test.test_id == args[1] and lab_test.lab.lab_id == args[0] and lab_test.person.id == args[2]):
                self.container.delete_test_by_test_id_and_lab_id(lab_test.test_id,lab_test.lab.lab_id)
                lab_test.update_test_result(args[4], args[3])
                return self.container.create_test(lab_test)
        return False

    def show_new_sick(self): # show in format "id", "firstname", "lastname", "birthdate", "phone", "mail", "city", "street", house-number, apartment, house-residents
        list_to_return = []
        for sick in self.list_of_new_patients:
            string = str(sick.id) + " " + sick.firstName + " " + sick.surName +\
                " " + str(sick.birthdate) + " " + sick.phone + \
                " " + sick.mail + " " + sick.home.city + " " + sick.home.street + " " + str(sick.home.number) +\
                str(sick.home.apartment_number) + " " + str(sick.home.house_residents)
            list_to_return.append(string)
        return list_to_return

    def show_stat(self, args:list): # args could be: sicks, healed, isolated, sick-per-city
        isolation_period = 14
        stats_dict = {}
        for arg in args:
            arg = arg.replace(",", "")
            if arg == "sicks":
                sicks = [x for x in self.container.read_list_of_patients() if x.sick]
                stats_dict["sicks"] = len(sicks)
            if arg == "healed":
                not_sick = [x for x in self.container.read_list_of_patients() if not x.sick]
                all_tests = self.container.read_list_of_tests()
                healed_list = []
                for x in not_sick:
                    for test in all_tests:
                        if (test.test_result and test.person.id == x.id):
                            healed_list.append(x)
                stats_dict["healed"] = len(healed_list)
            if arg == "isolated":
                time_now = datetime.datetime.now()
                isolated = [x for x in self.container.read_list_of_patients() if x.isolation_begin_date and (time_now-x.isolation_begin_date).days < isolation_period]
                stats_dict["isolated"] = len(isolated)
            if arg == "sick-per-city":
                city_sick_dict = {}
                sicks = [x for x in self.container.read_list_of_patients() if x.sick]
                for sick in sicks:
                    if sick.home.city not in city_sick_dict:
                        city_sick_dict[sick.home.city] =0
                    city_sick_dict[sick.home.city] +=1
                stats_dict["sick-per-city"] = city_sick_dict
        return stats_dict


    # def get_active_suspect(self) -> list:
    #     """
    #     :return: a list of suspects who had no tests
    #     """
    #     return [x for x in self.container.read_list_of_patients if x.sick is None]
