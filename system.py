import datetime,secrets
import random
import sqlite_demo
class ParkingLot:
    def __init__(self,name):
        self.name=name
        sqlite_demo.addParkingLot(name)
    def __addParkingFloor(self):
        temp=ParkingFloor(self)
        return temp
    def adminOnly(self):
        return self.__addParkingFloor()
    def addEntrancePanel(self):
        sqlite_demo.addEntrancePanel(self.name)
    def addExitPanel(self):
        sqlite_demo.addExitPanel(self.name)


class EntrancePanel:
    def __init__(self,inParkingLot):
        self.inParkingLot=inParkingLot
        sqlite_demo.addEntrancePanel(inParkingLot)
    def printTicket(self,vehicleObject):
        vehicleObject.assignTicket(self.inParkingLot)


class ExitPanel:
    def __init__(self,inParkingLot):
        self.inParkingLot=inParkingLot
        sqlite_demo.addExitPanel(inParkingLot)
    def scanTicket(self,parkingticket,vehicleObject):
        sqlite_demo.ScanTicket(parkingticket.ticketNumber)
    def ProcessPayment(self,parkingticket,payingMethod):
        sqlite_demo.ProcessTicket(parkingticket.ticketNumber)


class ParkingTicket:
    def __init__(self,vehicleObject,parkinglotobject,EntrancePanelId):
        sqlite_demo.ParkingTicketInit(secrets.token_hex(16),parkinglotobject.name,vehicleObject.licenseNumber,EntrancePanelId)
        self.ticketNumber=sqlite_demo.GetTicketNumber(vehicleObject.licenseNumber)

class Payment:
    def __init__(self,parkingTicketobject):
        self.creationDate=parkingTicketobject.issuedAt
        self.amount=parkingTicketobject.payedAmount
        self.status=False
        self.ticket=parkingTicketobject
    def initiateTransaction(self,typeofTrans):
        if typeofTrans=='Credit Card':
            CreditCardTransaction(self.ticket.ticketInfo.licenseNumber).Transaction(self.ticket.payedAmount)
        else:
            CashTransaction(self.ticket.licenseNumber).Transaction(self.ticket.payedAmount)

class CreditCardTransaction:
    def __init__(self,name):
        self.nameOnCard=name
    def Transaction(self,amount):
        print('Successfully payed {}$ by credit card'.format(amount))


class CashTransaction:
    def __init__(self,name):
        self.cashTenderer=name
    def Transaction(self,amount):
        print('Successfully payed {}$ by cash'.format(amount))


class ParkingFloor:
    def __init__(self,parkinglot):
        sqlite_demo.addParkingFloor(parkinglot.name)
        self.name = sqlite_demo.getParkingFloorNumber(parkinglot.name)
        self.inParkingLot=parkinglot
    def addParkingSpot(self,parkingSpotobject):
        temp=parkingSpotobject(self,self.inParkingLot)
        return temp


class ParkingDisplayBoard:
    def __init__(self,parkingfloor,parkinglot):
        #['Handicapped','Compact','Large','Motorbike','Electric']:
        self.handicappedFreeSpot=sqlite_demo.displayBoardInit('Handicapped',parkingfloor,parkinglot)
        self.compactFreeSpot=sqlite_demo.displayBoardInit('Compact',parkingfloor,parkinglot)
        self.largeFreeSpot=sqlite_demo.displayBoardInit('Large',parkingfloor,parkinglot)
        self.motorbikerFreeSpot=sqlite_demo.displayBoardInit('Motorbike',parkingfloor,parkinglot)
        self.electricFreeSpot=sqlite_demo.displayBoardInit('Electric',parkingfloor,parkinglot)
        self.floor=parkingfloor
    def show(self):
        string="""
        Free spots left in floor {}
        
        Handicapped: {} spot(s) left
        Compact:     {} spot(s) left
        Large:       {} spot(s) left
        Motorbike:   {} spot(s) left
        Electric:    {} spot(s) left
        """.format(self.floor,
                   self.handicappedFreeSpot,
                   self.compactFreeSpot,
                   self.largeFreeSpot,
                   self.motorbikerFreeSpot,
                   self.electricFreeSpot)
        print(string)


class ParkingSpot:
    def __init__(self,type,parkingfloor,parkinglotobject):
        self.ParkingLot=parkinglotobject
        self.ParkingFloor=parkingfloor
        self.type=type
        sqlite_demo.ParkingSpotInit(self.type,parkingfloor,parkinglotobject.name)
    def addVehicle(self,vehicleObject,SpotNumber):
        sqlite_demo.addVehicle(vehicleObject.licenseNumber,self.ParkingLot.name,self.ParkingFloor.name,SpotNumber)


class HandicappedSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Handicapped',parkingfloor,parkinglot)

class CompactSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Compact',parkingfloor,parkinglot)

class LargeSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Large',parkingfloor,parkinglot)

class MotorbikeSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Motorbike',parkingfloor,parkinglot)

class ElectricSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Electric',parkingfloor,parkinglot)


class Vehicle:
    def __init__(self,licenseNumber,type):
        self.licenseNumber=licenseNumber
        self.type=type
        sqlite_demo.VehicleInit(self.licenseNumber,self.type)
    def assignTicket(self,parkinglotobject,EntrancePanelId):
        self.ticket=ParkingTicket(self,parkinglotobject,EntrancePanelId)


class Car(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Car')

class Truck(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Truck')

class Electric(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Electric')

class Van(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Van')

class Motorbike(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Motorbike')



class Account:
    def __init__(self,username,password,type):
        self.username=username
        self.password=password
        sqlite_demo.AccountInit(self.username,self.password,type)

class Admin(Account):
    def __init__(self,username,password):
        Account.__init__(self,username,password,self.__class__.__name__)
    def setupParkingLot(self,name,Numberoffloor,enPanelNumber,exPanelNumber):
        pkl = ParkingLot(name)
        for index in range(Numberoffloor):
            pkl.adminOnly()
        for index in range(enPanelNumber):
            pkl.addEntrancePanel()
        for index in range(exPanelNumber):
            pkl.addExitPanel()
        return pkl
    def setupParkingFloor(self,floorNumber,ParkingLot,HandicappedNum,CompactNum,LargeNum,MotorbikeNum,ElectricNum):
        for index in range(HandicappedNum):
            spot = HandicappedSpot(floorNumber, ParkingLot)
        for index in range(CompactNum):
            spot = CompactSpot(floorNumber, ParkingLot)
        for index in range(LargeNum):
            spot = LargeSpot(floorNumber, ParkingLot)
        for index in range(MotorbikeNum):
            spot = MotorbikeSpot(floorNumber, ParkingLot)
        for index in range(ElectricNum):
            spot = ElectricSpot(floorNumber, ParkingLot)

#--------------------------------------------------------------------------------------------
#below are functional functions!







def assignTicketandGetintoSpot(floorNumber,ParkingLotObject,spotNumber,entrancePanelId,VehicleObject):
    VehicleObject.assignTicket(ParkingLotObject,entrancePanelId)
    sqlite_demo.addVehicle(VehicleObject.licenseNumber,ParkingLotObject.name,floorNumber,spotNumber)

def ScanTicketandProcessPayment(ticketNumber):
    try:
        sqlite_demo.ScanTicket(ticketNumber)
        print(sqlite_demo.ProcessTicket(ticketNumber))
    except TypeError:
        print("Ticket not exist!")




#This is a way to use the system(everything would be nicer if I design a GUI but I'm lazy)

if __name__=='__main__':
    admin=Admin("louisdo","lamthon1511")
    pkl=ParkingLot("The Sparks")
    moto=Motorbike("31-297-T9")
    car=Car("30-T4-1975")
    assignTicketandGetintoSpot(1,pkl,151,1001,moto)
    assignTicketandGetintoSpot(2,pkl,51,1001,car)
    ScanTicketandProcessPayment(moto.ticket.ticketNumber)
    board1=ParkingDisplayBoard(1,pkl)
    board2=ParkingDisplayBoard(2,pkl)
    board1.show()
    board2.show()
    sqlite_demo.show()
