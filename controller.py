from model import *
from view import Interface_View
from data_access import IDataAccess
from typing import List
import pprint
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
            if debug:
                print("-- debug --")
                print("patients:")
                pprint.pprint([vars(x) for x in self.container.read_list_of_patients()])
                print("sick_in_site:")
                pprint.pprint([vars(x) for x in self.container.read_list_of_sick_in_site()])
                print("tests:",)
                pprint.pprint([vars(x) for x in self.container.read_list_of_tests()])
                print("-- debug --")

            option: list = self.view.get_option_input().split()
            failed_msg = None
            if not option:
                failed_msg='no command inserted'
                self.view.operation_failed(failed_msg)
                continue
            if option[0] == 'Create-sick':
                result=self.create_sick(option[1:])
                if not result:
                    failed_msg="create sick failed"
                else:
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
                    failed_msg="No infector \ wrong encounter details"
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
                string, tests = self.show_person(option[1:])
                self.view.show_person(string, tests)
            elif option[0] == 'Show-person-route':
                list_of_sites = self.show_person_route(option[1:])
                self.view.show_person_route(list_of_sites)
            elif option[0] == 'Show-sick':
                list_of_sick = self.show_sick()
                self.view.show_sick(list_of_sick)
            elif option[0] == 'Show-isolated':
                list_of_isolated = self.show_isolated()
                self.view.show_isolated(list_of_isolated)
            elif option[0] == 'Show-help':
                self.view.show_help()
            else:
                failed_msg="unknown command"

            if failed_msg:
                self.view.operation_failed(failed_msg)

    # args: ["id" "firstname" "lastname" "birthdate" "phone" "mail" "city" "street" "house-number" "apartment" "house-residents"]
    def create_sick(self, args: list):
        # removes the person in case id is shown twice
        id=args[0]
        firstname=args[1]
        lastname=args[2]
        birthdate = datetime.datetime.strptime(args[3], '%Y-%m-%d')
        phone=args[4]
        mail=args[5]
        city=args[6]
        street=args[7]
        house_num=args[8]
        aptmnt=args[9]
        house_res=args[10]
        return self.container.create_patient(phone,firstname,lastname,id,birthdate,mail,city,street,house_num,aptmnt,house_res,sick=True)

    # args: ["id" "01/04/2020" "10:00" "sitename" optional: "city" "street" "number"]
    def add_route_site(self, args: list):
        date_time = datetime.datetime.strptime(
            args[1] + args[2], '%Y-%m-%d%H:%M')
        id=args[0]
        site_name=args[3]
        city=None
        street=None
        number=None
        if len(args) > 4:
            city=args[4]
            street=args[5]
            number=args[6]
        
        return self.container.create_sick_in_site(id,site_name,date_time,city,street,number)

    # "sick-id" "firstname" "lastname" "phone"
    def add_sick_encounter(self, args: list):
        sick_id=args[0]
        first_name=args[1]
        last_name=args[2]
        phone=args[3]
        return self.container.create_sick_encounter(sick_id,first_name,last_name,phone)

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
        sick_id = args[1]
        firstName = args[2]
        surName = args[3]
        birthdate = datetime.datetime.strptime(args[4], '%Y-%m-%d')
        phone = args[5]
        mail = args[6]
        city=args[7]
        street=args[8]
        number=args[9]
        apt_num=args[10]
        house_res=args[11]
        return self.container.update_sick_encounter_details(encounter_id, sick_id,firstName,surName,birthdate,phone,mail,city,street,number,apt_num,house_res)

    def update_lab_test(self, args: list):  # labid testid personid date result
        test_id=args[1]
        lab_id=args[0]
        person_id=args[2]
        result_date=args[3]
        result=args[4]
        return self.container.update_test_result(test_id,lab_id,person_id,result_date,result)

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

    def show_person(self, args): #id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents, source-sick(0 if unknown) ** LAB RESULT BEGIN ** date labid testid result ** LAB RESULT END ** 
        person = self.container.get_person_by_id(args[0])
        test_list_of_person = [str(x.test_date.date) +" "+str(x.lab.lab_id)+" "+str(x.test_id)+" "+str(x.test_result) for x in self.container.read_list_of_tests() if x.id == args[0]]
        string = str(person.id)+" "+person.firstName+" "+person.surName+" "+str(person.birthdate.date)+" "+person.phone+\
        " "+person.mail+" "+person.home.city+" "+person.home.street+" "+str(person.home.number)+" "+str(person.home.apartment_number)+\
            " "+str(person.home.house_residents)+" "+(person.infector.firstName if hasattr(person, "infector") else "0")
        return string, test_list_of_person

    def show_person_route(self, args):
        sick_in_site = self.container.read_list_of_sick_in_site()
        list_of_sites = []
        for x in sick_in_site:
            if (x.sick.id == args[0]):
                list_of_sites.append(str(x.site.siteName))
        return list_of_sites

    def show_sick(self): # id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents, source-sick(0 if unknown)
        list_of_sick = [str(x.id)+" "+x.firstName+" "+x.surName+" "+str(x.birthdate.date)+" "+x.phone+\
        " "+x.mail+" "+x.home.city+" "+x.home.street+" "+str(x.home.number)+" "+str(x.home.apartment_number)+\
            " "+str(x.home.house_residents)+" "+x.infector.firstName if hasattr(x, "infector") else "0" for x in self.container.read_list_of_patients() if x.sick == True]
        return list_of_sick

    def show_isolated(self): # id, firstname, lastname, birthdate, phone, mail, city, street, house-number, apartment, house-residents
        time_now = datetime.datetime.now()
        isolation_period = 14
        isolated = [str(x.id)+" "+x.firstName+" "+x.surName+" "+str(x.birthdate.date)+" "+x.phone+\
        " "+x.mail+" "+x.home.city+" "+x.home.street+" "+str(x.home.number)+" "+str(x.home.apartment_number)+\
            " "+str(x.home.house_residents) for x in self.container.read_list_of_patients() if
                    x.isolation_begin_date and (time_now - x.isolation_begin_date).days < isolation_period]
        return isolated

    # def get_active_suspect(self) -> list:
    #     """
    #     :return: a list of suspects who had no tests
    #     """
    #     return [x for x in self.container.read_list_of_patients if x.sick is None]
