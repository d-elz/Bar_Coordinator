
#Our imports
from security_staff import signature
from common import  funcs , db
from common.db import Bardb

from Crypto import Random
import random
import time

class baseCoordinator(object):
    """
    This class is the main class of the Coordinator
    operations.
    @func
    """
    def __init__(self):
        pass

class Coordinator(baseCoordinator):
    """
    This class is the main class of the Coordinator
    operations.
    @func coordinator_operation : is the main function of the coordinator.
    @func logs : keep updating a time stamp file with all the client requests
    """
    def __init__(self):
        pass

    def coordinator_operation(self,data):
        """
        Here is the func for every coordinator
        """
        pass

    def logs(Filename):
        self.fp = open(Filename, 'a')
        log = "Bar[" + time.asctime(time.localtime()) + "] from "+ str(peer) + " with method: " + "\r"
        self.fp.write(log)

class DatabaseOperationCoordinator(Coordinator):

    """
    All the function that coordinator wants for the services he grants
    @func checking_pseudonym : checking if the given pseudonym is in the PublicList table
    @func insert_public_list : publishing in the bulletin board(PublicList) the nym,pk,sign
    @func insert_active_list : publishing in the bulletin board(ActiveList) the id,IP,bridge_pk , when a user log in
    @func delete_active_list : log out a user (deleting an entry)
    @func check_ip : checking if another user has the same ip. If so ,we not procced
    @func check_id : checking if another user has the same id. If so ,we not procced
    @func insert_exchange_key_list : publish the exchange key to the exchangeKeylist
    @func select_exchange_list :
    @func check_update_exchange_list :

    """
    def __init__(self):
        pass

    def checking_pseudonym(self,pseudonym):
        get_where_dict = { "nym" : pseudonym ,}
        db = Bardb()
        check = db.select_entries("PublicList", get_where_dict)
        if check :
            print "There is a user with the same pseudonym"
            return False
        else:
            print "Nobody has the same name .You can proceed!"
            return True

    def insert_public_list(self,nym,pk,sign):
        get_where_dict = { "nym" : nym ,
                            "pk" : pk ,
                            "signature" : sign ,}
        db = Bardb()
        row_public_list = db.insert_entry("PublicList", get_where_dict)
        print "The data was successfully added to database "
        #self.logs("logs")
        return row_public_list

    def insert_active_list(self,special_id,IP,bridge_pk,bar_server):
        get_where_dict = { "special_id" : special_id ,
                            "ip" : IP ,
                            "bridge_pk" : bridge_pk ,
                            "bar_server" : bar_server ,}
        db = Bardb()
        row_active_list = db.insert_entry("ActiveList", get_where_dict)
        return row_active_list

    def delete_active_list(self,IP):#maybe if the user ISP change IP we have problem
        get_where_dict = { "ip" : IP ,}
        db = Bardb()
        row_active_list = db.delete_entries("ActiveList", get_where_dict)
        return row_active_list

    def check_ip(self,IP):
        get_where_dict = { "ip" : IP ,}
        db = Bardb()
        check = db.select_entries("ActiveList", get_where_dict)
        if check :
            print "There is an other user with same IP"
            return False
        else:
            return True



    def check_id(self,special_id):
        get_where_dict = { "special_id" : special_id ,}
        db = Bardb()
        check = db.select_entries("ActiveList", get_where_dict)
        if check :
            print "There is an other user with the same id"
            return False
        else:
            return True

    # ExchangeKeyList methods

    def insert_exchange_key_list(self,nym,cij):
        get_where_dict = { "nym" : nym ,
                            "cij" : cij ,}
        db = Bardb()
        row_exchange_key_list = db.insert_entry("ExchangeKeyList", get_where_dict)
        return row_exchange_key_list

    def select_exchange_list(self,nym):
        get_where_dict = { "nym" : nym ,}
        db = Bardb()
        exchange = db.select_entries("ExchangeKeyList", get_where_dict)
        print exchange[0]['cij']
        return exchange[0]['cij']

    def check_update_exchange_list(self, nym, cij):
        get_where_dict = { "nym" : nym ,}
        set_where_dict = { "cij" : cij ,
                            }

        db = Bardb()
        check = db.select_entries("ExchangeKeyList", get_where_dict)
        if check :
            print "There is a user with the same pseudonym.We update the key"
            #return False
            row_list = db.update_entries("ExchangeKeyList", get_where_dict , set_where_dict)
        else:
            print "First time excganging keys thse users!"
            self.insert_exchange_key_list(nym,cij)
            #return True

    #Bar Server methods
    def insert_bar_server_list(self,IP,description,name):
        get_where_dict = { "ip" : IP ,
                            "description" : description ,
                            "name" : name ,}
        db = Bardb()
        row_bar_server_list = db.insert_entry("ActiveBarServers", get_where_dict)
        return row_bar_server_list

    def delete_bar_server_list(self,name):#maybe if the user ISP change IP we have problem
        get_where_dict = { "name" : name ,}
        db = Bardb()
        row_bar_server_list = db.delete_entries("ActiveBarServers", get_where_dict)
        return row_bar_server_list

    def get_bar_server_IP(self,name):
        get_where_dict = { "name" : name ,}
        db = Bardb()
        bar_server = db.select_entries("ActiveBarServers", get_where_dict)
        return bar_server[0]['ip']

class SecurityOperationCoordinator(Coordinator):

    """
    Here us the security functions of the Coordinator  . We have only one at this time
    @func coordinator_signature : uses the signature file method and signs nym and pk with the private key of the cooordinator
    """

    def __init__(self):
        pass

    def coordinator_signature(self,nym_pk):
        sign= signature.sign(nym_pk , funcs.dirc(__file__,'../keys',"/private_key"))
        return sign

    def coordinator_verification():
        pass

    def coordinator_encrypt():
        pass

    def coordinator_decrypt():
        pass

class RegisterCoordinator(Coordinator):

    """
    $Register Service
    The main service of the register is coordinator operation.
    Go to the paper to see the exact implemetation of the register Service
    @func coordinator_operation :

    """

    def __init__(self):
        pass

    def coordinator_operation(self,data):
        #Testing threads
        #time.sleep(10)

        #Objects
        database_coor = DatabaseOperationCoordinator()
        security_coor = SecurityOperationCoordinator()

        #Spliting data
        nym = data.split('||||')[1]
        pk = data.split('||||')[2]
        nym_pk = data.split('||||')[1] + data.split('||||')[2]

        ##### 1.Cheking the UserList [nym , pk , sign] if nym exist!
        #check_nym_exist = database_coor.checking_pseudonym(nym)
        ##### This step is in register_service.py . It s better use it there because helping us send message back to the client

        #### 2.Compute s = sign(nym||||pk)
        sign= security_coor.coordinator_signature(nym_pk)

        #### 3.Add [nym , pk , s = sign] to the UserList
        #if check_nym_exist:
        database_coor.insert_public_list(nym, pk ,sign )

class LogInOutCoordinator(Coordinator):
    """
    This class is the main class of the Coordinator
    operations.
    @param Nmin :
    @param Nmax :
    @param M :
    @param m :
    """
    ##Cluster Params (not in use yet)
    M = 10
    m = 20
    #----------
    Nmin = 200
    Nmax = 500

    def __init__(self):
        pass

    def login(self,data):
        #time.sleep(2)
        #objects
        database_coor = DatabaseOperationCoordinator()

        #Spliting data
        nym = data.split('||||')[1]
        bridge_key = data.split('||||')[3]
        IP = data.split('||||')[4]
        cluster = data.split('||||')[5]

        #getNmax
        Nmax = 10000

        #(a) Choose a random idi BARi, not in use.
            #Generate random numbers
        #rpool =  Random.new()
        #Random.atfork()
        #special_id = rpool.read(16).encode("hex")
        bar_server = "Bar"
        if cluster == "Bar1":
            find_id=True
            while find_id: #if we eant to make abstract this code we must fix the checking mechanism first
                special_id = random.randrange(1, 1000, 1)
                check_id = database_coor.check_id(special_id)
                if check_id: find_id = False
            bar_server = database_coor.get_bar_server_IP("Bar1")
        elif cluster == "Bar2":
            find_id=True
            while find_id:
                special_id = random.randrange(1000, 2000, 1)
                check_id = database_coor.check_id(special_id)
                if check_id: find_id = False
            bar_server = database_coor.get_bar_server_IP("Bar2")
        else :
            print "Something wrong at clusters"
        print "LogIn Info: "+nym+" from "+IP+" in bar server "+cluster

        #Checks if someone have the same IP:port combination
        check_ip = database_coor.check_ip(IP)
        if check_ip:
            database_coor.insert_active_list(special_id, IP ,bridge_key,cluster )
            return True , bar_server
        else:
            return False , bar_server

    def logout(self,data):
        #time.sleep(2)
        #objects
        database_coor = DatabaseOperationCoordinator()

        #Spliting data
        IP = data.split('||||')[1]

        #Delete the row in Active List
        database_coor.delete_active_list(IP)


class ExchangeKeyCoordinator(Coordinator):
    def __init__(self):
        pass

    def coordinator_operation(self,data):
        #Testing threads
        #time.sleep(10)

        #Objects
        database_coor = DatabaseOperationCoordinator()

        #Spliting data
        nym = data.split('||||')[1]
        cij = data.split('||||')[2]
        print nym
        print cij
        ##### 1.Maintain a public bulleting board

        ##### 2.Publish on the bulletin board each [nym,cij] that is received
        database_coor.check_update_exchange_list( nym, cij)

class BarServerCoordinator(Coordinator):
    def __init__(self):
        pass

    def coordinator_operation(self,data):
        #Testing threads
        #time.sleep(10)

        #Objects
        database_coor = DatabaseOperationCoordinator()
        #Spliting data
        description = data.split('||||')[1]
        BarServerIP_port = data.split('||||')[2]
        BarServerIP = data.split(':')[0]
        BarServer_port = data.split(':')[1]
        name = data.split('||||')[3]
        ##### 1.Maintain a public bulleting board

        ##### 2.Publish on the bulletin board each [nym,cij] that is received
        database_coor.insert_bar_server_list( BarServerIP_port, description,name)

    def bar_server_logout(self,unique_name):
        #time.sleep(2)
        #objects
        database_coor = DatabaseOperationCoordinator()

        #Delete the row in Active List
        database_coor.delete_bar_server_list(unique_name)

class BCPCoordinator(Coordinator):
    def __init__(self):
        pass


if __name__ == '__main__':
    coordinator_service("manoliso")
