import sqlite3,datetime

conn=sqlite3.connect('ParkingLotDatabase.db')


curs=conn.cursor()


#These are the tables that I use to store info


#create table ParkingLot
#(name varchar(20),
#constraint pk_pkl_name primary key(name))

#create table ParkingFloor
#(inParkingLot varchar(20),floornumber smallint unsigned,
#constraint pk_pkf_floornum primary key(floornumber),
#constraint fk_pkf_inpkl foreign key(inParkingLot)
#references ParkingLot(name))

#create table Ticket
#(ticketnumber varchar(20), issueplace varchar(20), arrivetime datetime, departtime datetime, fee float,
#constraint pk_ticket_num primary key(ticketnumber),
#constraint fk_ticket_place foreign key(issueplace)
#references ParkingLot(name))

#create table Vehicle
#(license varchar(20), type varchar(12), ticketnumber varchar(20),inParkingLot varchar(20), inParkingFloor varchar(20),
#constraint pk_v_license primary key(license),
#constraint fk_v_ticketnumber foreign key(ticketnumber)
#references Ticket(ticketnumber),
#constraint fk_v_pkl foreign key(inParkingLot)
#references ParkingLot(name),
#constraint fk_v_pkf foreign key(inParkingFloor)
#references ParkingFloor(floornumber))

#create table ParkingSpot
#(spotnumber smallint unsigned,inParkingLot varchar(20), inParkingFloor smallint unsigned,status varchar(10), type varchar(12), vehicle_in_license varchar(20),
#constraint pk_ps_license primary key(vehicle_in_license),
#constraint fk_ps_inpkl foreign key(inParkingLot)
#references ParkingLot(name)
#constraint fk_ps_inpkf foreign key(inParkingLot)
#references ParkingFloor(floornumber)
#constraint fk_ps_vil foreign key(vehicle_in_license)
#references Vehicle(license))

#create table Panel
#(type varchar(12), id integer, inParkingLot,
#constraint fk_panel_inpkl foreign key(inParkingLot)
#references ParkingLot(name))

#create table Account
#(username varchar(20), password varchar(20), type varchar(12),
#constraint pk_acc_username primary key(username))




def addParkingLot(name):
    with conn:
        try:
            curs.execute("insert into ParkingLot values(:name)", {'name': name})
        except Exception:
            pass

def addParkingFloor(parkinglot):
    with conn:
        curs.execute("""
        select max(pkf.floornumber)
        from ParkingFloor pkf inner join ParkingLot pkl
        on pkf.inParkingLot=pkl.name
        where pkf.inParkingLot=:parkinglot
        """,{"parkinglot":parkinglot})
        floornumber,=curs.fetchone()
        if floornumber==None: floornumber=0
        curs.execute("insert into ParkingFloor values(:inParkingLot,:floornumber)",{"inParkingLot":parkinglot,"floornumber":floornumber+1})

def getParkingFloorNumber(parkinglot):
    with conn:
        curs.execute("select max(floornumber) from ParkingFloor where inParkingLot=:parkinglot",{"parkinglot":parkinglot})
        ret,=curs.fetchone()
        return ret



def addEntrancePanel(parkinglot):
    with conn:
        curs.execute("select max(id) from Panel where type=:type and inParkingLot=:parkinglot",{"type":"Entrance","parkinglot":parkinglot})
        maxid,=curs.fetchone()
        if not maxid: maxid=1000
        curs.execute("insert into Panel values(:type,:id,:inParkingLot)",{"type":'Entrance',"id":maxid+1,"inParkingLot":parkinglot})

def addExitPanel(parkinglot):
    with conn:
        curs.execute("select max(id) from Panel where type=:type and inParkingLot=:parkinglot",{"type":'Exit',"parkinglot":parkinglot})
        maxid,=curs.fetchone()
        if not maxid: maxid=2000
        curs.execute("insert into Panel values(:type,:id,:inParkingLot)",{"type":'Exit',"id":maxid+1,"inParkingLot":parkinglot})

def VehicleInit(licenseNumber,type):
    with conn:
        try:
            curs.execute("insert into Vehicle values(:license,:type,:ticketnumber,:inParkingLot,:inParkingFloor)",
                         {"license":licenseNumber,"type":type,"ticketnumber":None,"inParkingLot":None,"inParkingFloor":None})
        except Exception:
            pass


def ParkingSpotInit(type,parkingfloor,parkinglot):
    with conn:
        curs.execute("select max(spotnumber) from ParkingSpot where inParkingFloor=:parkingfloor and inParkingLot=:parkinglot",
                     {"parkingfloor":parkingfloor,"parkinglot":parkinglot})
        maxspotnum,=curs.fetchone()
        if not maxspotnum: maxspotnum=0
        curs.execute("insert into ParkingSpot values(:spotnumber,:inParkingLot,:inParkingFloor,:status,:type,:vehicle_in_license)",
                     {"spotnumber":maxspotnum+1,"inParkingLot":parkinglot,"inParkingFloor":parkingfloor,"status":"avail","type":type,"vehicle_in_license":None})


def addVehicle(licenseNumber,ParkingLotName,ParkingFloorNumber,SpotNumber):
    dict={"Car":"Compact","Electric":"Electric","Truck":"Large","Van":"Large","Motorbike":"Motorbike"}
    with conn:
        curs.execute("select inParkingLot,ticketnumber, type from Vehicle where license=:ln",{"ln":licenseNumber})
        test,test3,test4,=curs.fetchone()
        curs.execute("select type from ParkingSpot where spotnumber=:spotnumber",{"spotnumber":SpotNumber})
        test2,=curs.fetchone()
        if not test and test3 and dict[test4]==test2:
            curs.execute("""
            update Vehicle 
            set inParkingLot=:pklname, inParkingFloor=:pkfnumber
            where license=:ln
            """,{"pklname":ParkingLotName,"pkfnumber":"In floor {}".format(ParkingFloorNumber),"ln":licenseNumber})
            curs.execute("""
                    update ParkingSpot
                    set vehicle_in_license=:licenseNumber, status=:stt
                    where inParkingLot=:Lotname and inParkingFloor=:floornum and spotnumber=:sn
                    """, {"licenseNumber": licenseNumber, "stt": "unavail", "Lotname": ParkingLotName,
                          "floornum": ParkingFloorNumber, "sn": SpotNumber})

def ParkingTicketInit(ticketNumber,ParkingLotName,licenseNumber,EntrancePanelId):
    with conn:
        curs.execute("select ticketnumber from Vehicle where license=:licenseNumber",
                     {"licenseNumber":licenseNumber})
        test,=curs.fetchone()
        if not test:
            curs.execute("""
            update Vehicle
            set ticketnumber=:ticketNumber
            where license=:licenseNumber
            """,{"ticketNumber":ticketNumber,"licenseNumber":licenseNumber})
            curs.execute("""
            insert into Ticket
            values(:ticketNumber,:issueplace,(select datetime(current_timestamp,'localtime')),:departtime,:fee)
            """,{"ticketNumber":ticketNumber,"issueplace":ParkingLotName+' Entrance Panel id: {}'.format(EntrancePanelId),
                 "departtime":None,"fee":None})

def GetTicketNumber(license):
    with conn:
        curs.execute("select ticketnumber from Vehicle where license=:license",
                     {"license":license})
        ret,=curs.fetchone()
        return ret

def ScanTicket(TicketNumber):
    with conn:
        curs.execute("select departtime from Ticket where ticketnumber=:ticketnumber",{"ticketnumber":TicketNumber})
        tn,=curs.fetchone()
        if not tn:
            curs.execute("""
            update Ticket
            set departtime=(select datetime(current_timestamp,'localtime'))
            where ticketnumber=:ticketNumber
            """,{"ticketNumber":TicketNumber})



def ProcessTicket(ticketNumber):
    with conn:
        curs.execute("""
        select julianday(departtime)-julianday(arrivetime) from Ticket where ticketnumber=:ticketNumber
        """,{"ticketNumber":ticketNumber})
        ret,=curs.fetchone()
        curs.execute("select license from Vehicle where ticketnumber=:ticketNumber",{"ticketNumber":ticketNumber})
        license,=curs.fetchone()
        curs.execute("delete from Vehicle where ticketnumber=:ticketNumber",{"ticketNumber":ticketNumber})
        curs.execute("delete from Ticket where ticketnumber=:ticketNumber",{"ticketNumber":ticketNumber})
        curs.execute("""
        update ParkingSpot
        set status=:stt, vehicle_in_license=:license
        where vehicle_in_license=:licenseCheck
        """,{"stt":'avail',"license":None,"licenseCheck":license})
        return "Your parking fare is {}$".format(round(ret*24,2))


def AccountInit(username,password,type):
    with conn:
        try:
            curs.execute("""
            insert into Account
            values(:username,:pass,:type)
            """,{"username":username,"pass":password,"type":type})
        except Exception:
            pass

def displayBoardInit(type,floorNumber,parkinglot):
    with conn:
        curs.execute("select count(spotnumber) from ParkingSpot where type=:type and status=:stt and inParkingFloor=:floorNumber and inParkingLot=:parkinglot",
                     {"type":type,"stt":"avail","floorNumber":floorNumber,"parkinglot":parkinglot.name})
        ret,=curs.fetchone()
        return ret

def deleteAll():
    with conn:
        curs.execute("delete from ParkingLot")
        curs.execute("delete from ParkingFloor")
        curs.execute("delete from Panel")
        curs.execute("delete from Vehicle")
        curs.execute("delete from ParkingSpot")
        curs.execute("delete from Ticket")



def show():
    with conn:
        curs.execute("select * from ParkingLot order by name")
        print(curs.fetchall())
        curs.execute("select * from ParkingFloor order by floornumber")
        print(curs.fetchall())
        curs.execute("select * from Panel")
        print(curs.fetchall())
        curs.execute("select * from Vehicle")
        print(curs.fetchall())
        curs.execute("select * from ParkingSpot order by inParkingLot, inParkingFloor")
        print(curs.fetchall())
        curs.execute("select * from Ticket")
        print(curs.fetchall())
        curs.execute("select * from Account")
        print(curs.fetchall())


conn.commit()
