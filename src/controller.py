from model import *
from view import Interface_View
from data_access import IDataAccess
from typing import List
import pprint
import sys
debug = False
if "-d" in sys.argv:
    debug = True

isolation_period = 14 # how long a person needs to be isolated if one has been in contact with a COVID-sick person
class Controller:
    def __init__(self, view: Interface_View,container:IDataAccess):
        self.view = view
        self.container=container # can be a DB, can be pythonish, can be anything. must support all IDataAccess functions
        self.list_of_new_patients: List[Person]= []
        pass

    def start(self):
        while True:
            if debug:
                print("-- START  debug --")
                print("patients:")
                pprint.pprint([vars(x) for x in self.container.read_list_of_patients()])
                print("sick_in_site:")
                pprint.pprint([vars(x) for x in self.container.read_list_of_sick_in_site()])
                print("tests:",)
                pprint.pprint([vars(x) for x in self.container.read_list_of_tests()])
                print("-- END debug --")

            option: list = self.view.get_option_input().split() # makes a list of input args, for ex: # ["Create-sick" "id" "firstname" "lastname" "birthdate" "phone" "mail" "city" "street" "house-number" "apartment" "house-residents"]
            failed_msg = None
            if not option:
                failed_msg='no command inserted'
                self.view.operation_failed(failed_msg)
                continue
            if option[0] == 'Create-sick':
                result=self.create_sick(option[1:])
                if not result:
                    failed_msg="Create-sick failed"
                else:
                    self.view.create_sick()
            elif option[0] == 'Add-route-site':
                if self.add_route_site(option[1:]):
                    self.view.add_route_site()
                else:
                    failed_msg="Add-route-site failed"
            elif option[0] == 'Add-route-address':
                if self.add_route_site(option[1:]):
                    self.view.add_route_address()
                else:
                    failed_msg="Add-route-address failed"
            elif option[0] == 'Add-sick-encounter':
                if self.add_sick_encounter(option[1:]):
                    self.view.add_sick_encounter()
                else:
                    failed_msg="Add-sick-encounter failed: no infector found or wrong encounter details"
            elif option[0] == 'Show-sick-encounter':
                result = self.show_sick_encounter()
                if result:
                    self.view.show_sick_encounter(result)
                else:
                    failed_msg="Show-sick-encounter failed"
            elif option[0] == 'Update-sick-encounter-details':
                if self.update_sick_encounter_details(option[1:]):
                    self.view.update_sick_encounter_details()
                else:
                    failed_msg = "Update-sick-encounter-details failed: there is no such encounter or missing details"
            elif option[0] == 'Update-lab-test':
                if self.update_lab_test(option[1:]):
                    self.view.update_lab_test()
                else:
                    failed_msg = "Update-lab-test failed: No such test or missing details"
            elif option[0] == 'Show-new-sick':
                result = self.show_new_sick()
                if result:
                    self.view.show_new_sick(result)
                else:
                    failed_msg="Show-new-sick: no new sick people"
            elif option[0] == 'Show-stat':
                result = self.show_stat(option[1:])
                if result:
                    self.view.show_stat(result)
                else:
                    failed_msg="Show-stat failed"
            elif option[0] == 'Show-person':
                string, tests = self.show_person(option[1:])
                if string:
                    self.view.show_person(string, tests)
                else:
                    failed_msg="Show-stat failed"
            elif option[0] == 'Show-person-route':
                list_of_sites = self.show_person_route(option[1:])
                if list_of_sites:
                    self.view.show_person_route(list_of_sites)
                else:
                    failed_msg="Show-person-route failed"
            elif option[0] == 'Show-sick':
                list_of_sick = self.show_sick()
                if list_of_sick:
                    self.view.show_sick(list_of_sick)
                else:
                    failed_msg="Show-sick failed"
            elif option[0] == 'Show-isolated':
                list_of_isolated = self.show_isolated()
                if list_of_isolated:
                    self.view.show_isolated(list_of_isolated)
                else:
                    failed_msg="Show-isolated failed: no isolated people found"
            elif option[0] == 'Show-help':
                self.view.show_help()
            else:
                failed_msg="UNKNOWN COMMAND:: "+option[0]

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
        isolation_date = datetime.datetime.now()
        pereson_created= self.container.create_patient(phone,firstname,lastname,id,birthdate,mail,city,street,house_num,aptmnt,house_res,sick=True, isolation_begin_date=isolation_date)
        self.list_of_new_patients.append(pereson_created)
        return pereson_created
         

    # args: ["id" "01/04/2020" "10:00" "sitename" optional: "city" "street" "number"]
    def add_route_site(self, args: list):
        date_time = datetime.datetime.strptime(
            args[1] + args[2], '%Y-%m-%d%H:%M')
        id=args[0]
        site_name=args[3]
        city=None
        street=None
        number=None
        if len(args) > 4: # add_route_address
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
        suspects = [x for x in self.container.read_list_of_patients() if x.id == None]
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

    def update_lab_test(self, args: list): 
        lab_id=args[0]
        test_id=args[1]
        person_id=args[2]
        result_date=datetime.datetime.strptime(args[3], '%d-%m-%Y')
        result=True if args[4]=='true' else False
        return self.container.update_test_result(test_id,lab_id,person_id,result_date,result)

    def show_new_sick(self): 
        list_to_return = []
        for sick in self.list_of_new_patients:
            string=params_to_string(sick.id,sick.firstName,sick.surName,str(sick.birthdate.date()),sick.phone,sick.mail,sick.home.city,sick.home.street,sick.home.number,\
                sick.home.apartment_number,sick.home.house_residents)
            list_to_return.append(string)
        self.list_of_new_patients.clear()
        return list_to_return

    def show_stat(self, args:list): 
        isolation_period = 14
        stats_dict = {}
        for arg in args:
            arg = arg.replace(",", "")
            if arg == "sick":
                sicks = self.show_sick()
                stats_dict["sick"] = len(sicks)
            if arg == "healed":
                not_sick = list(set(self.container.read_list_of_patients()) - set(self.container.read_list_of_sick()))
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
                sicks = self.container.read_list_of_sick()
                for sick in sicks:
                    if sick.home.city not in city_sick_dict:
                        city_sick_dict[sick.home.city] =0
                    city_sick_dict[sick.home.city] +=1
                stats_dict["sick-per-city"] = city_sick_dict
        return stats_dict

    def show_person(self, args): 
        person = self.container.get_person_by_id(args[0])
        test_list_of_person = [str(x.result_date.date()) +" "+str(x.lab.lab_id)+" "+str(x.test_id)+" "+str(x.test_result) for x in self.container.read_list_of_tests() if x.person.id == args[0]]
        person_string=params_to_string( person.id,person.firstName,person.surName,str(person.birthdate.date()),\
                                        person.phone,person.mail,person.home.city,person.home.street,person.home.number,\
                                        person.home.apartment_number,person.home.house_residents,(person.infector.firstName if hasattr(person, "infector") else "0" ))
        return person_string, test_list_of_person

    def show_person_route(self, args):
        sick_in_site = self.container.read_list_of_sick_in_site()
        list_of_sites = []
        for x in sick_in_site:
            if (x.sick.id == args[0]):
                list_of_sites.append(x.site.siteName+(' '+x.site.siteAddress.city if x.site.siteAddress else ''))
        return list_of_sites

    def show_sick(self): 
        sick_print_list=[]
        for sick in self.container.read_list_of_sick():
                        person_string = params_to_string(sick.id, sick.firstName, sick.surName,
                                                         str(sick.birthdate.date()), sick.phone, sick.mail,
                                                         sick.home.city, sick.home.street, sick.home.number,
                                                         sick.home.apartment_number, sick.home.house_residents, (
                                                         sick.infector.firstName if hasattr(sick,"infector") else "0"))
                        sick_print_list.append(person_string)
        return sick_print_list

    def show_isolated(self): 
        time_now = datetime.datetime.now()
        isolated = []
        for sick in self.container.read_list_of_patients():

            if sick.isolation_begin_date and (time_now - sick.isolation_begin_date).days < isolation_period:
                id= (str(sick.id) if sick.id else 'NO-ID')
                bday=str(sick.birthdate.date()) if sick.birthdate else ''
                if sick.mail: # if was 'interviewd' and details were updated by a nurse
                    person_string=params_to_string(id,sick.firstName,sick.surName,bday,sick.phone,sick.mail,sick.home.city,sick.home.street,sick.home.number,sick.home.apartment_number,str(sick.home.house_residents))
                else:
                    person_string=params_to_string(id,sick.firstName,sick.surName,bday,sick.phone)
                isolated.append(person_string) # seperate by space
        return isolated

def params_to_string(id,first_name,sur_name,birthdate,phone,mail='',city='',street='',house_number='',apt_num='',house_residents='',source_sick=''):
    string_list=[str(id),first_name,sur_name,birthdate,phone,mail,city,street,str(house_number),str(apt_num),str(house_residents),source_sick]
    return " ".join(string_list) # return a string seperated by spaces