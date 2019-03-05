import datetime
import random
class ParkingLot:
    def __init__(self):
        self.id='some_id'
        self.location='some where on Earth.'
        self.ParkingFloor=[]
        self.EntrancePanel=[]
        self.ExitPanel=[]
    def __addParkingFloor(self):
        self.ParkingFloor.append(ParkingFloor(len(self.ParkingFloor)+1))
    def adminOnly(self):
        self.__addParkingFloor()
    def addEntrancePanel(self):
        self.EntrancePanel.append(EntrancePanel(len(self.EntrancePanel)+1))
    def addExitPanel(self):
        self.ExitPanel.append(ExitPanel(len(self.ExitPanel)+1))
    def getNewParkingTicket(self,EPid,vehicleObject):
        self.EntrancePanel[EPid-1].printTicket(vehicleObject)


class EntrancePanel:
    def __init__(self,id):
        self.id=id
    def printTicket(self,vehicleObject):
        vehicleObject.assignTicket()
        
        
class ExitPanel:
    def __init__(self,id):
        self.id=id
    def scanTicket(self,parkingticket,vehicleObject):
        if not vehicleObject.licenseNumber==parkingticket.ticketInfo.licenseNumber:
            print('Ticket info and vehicle not matched')
            return
        parkingticket.payedAt=datetime.datetime.now()
    def ProcessPayment(self,parkingticket,payingMethod):
        hour,minute,second=str(parkingticket.payedAt-parkingticket.issuedAt).split(':')
        parkingticket.payedAmount=int(hour)+int(minute)/60+int(second)/3600
        parkingticket.payment=Payment(parkingticket)
        parkingticket.payment.initiateTransaction(payingMethod)


class ParkingTicket:
    def __init__(self,vehicleObject):
        self.ticketNumber=str(random.choice(range(100000,1000000)))
        self.issuedAt=datetime.datetime.now()
        self.payedAt=None
        self.payedAmount=0
        self.status=0
        self.ticketInfo=vehicleObject
        self.payment=None

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
    def __init__(self,name):
        self.name=name
        self.allParkingSpot=[]
    def addParkingSpot(self,parkingSpotobject):
        self.allParkingSpot.append(parkingSpotobject(len(self.allParkingSpot)+1))
    def updateDisplayBoard(self):
        for item in self.allParkingSpot:
            print(item)
        ParkingDisplayBoard(self,111).show()
    def vehicle_to_slot(self,vehicle):
        if not vehicle.ticketAssigned:
            print('Take your ticket first!!')
            return
        for item in self.allParkingSpot:
            if item.free:
                item.free=False
                vehicle.at_spot=item.number
                item.vehicle_in_place=vehicle
                print('[VehicleType: {}, LicenseNumber: {}] is now at spot number {}'.format(vehicle.type,
                                                                                           vehicle.licenseNumber,item.number))
                break
    def countFreeSpot(self,type):
        count=0
        for spot in self.allParkingSpot:
            if spot.type==type and spot.free:
                count+=1
        return count


class ParkingDisplayBoard:
    def __init__(self,parkingfloor,id):
        self.id=id
        self.handicappedFreeSpot=ParkingFloor.countFreeSpot(parkingfloor,'Handicapped')
        self.compactFreeSpot=ParkingFloor.countFreeSpot(parkingfloor,'Compact')
        self.largeFreeSpot=ParkingFloor.countFreeSpot(parkingfloor,'Large')
        self.motorbikerFreeSpot=ParkingFloor.countFreeSpot(parkingfloor,'Motorbike')
        self.electricFreeSpot=ParkingFloor.countFreeSpot(parkingfloor,'Electric')
    def show(self):
        string="""
        Handicapped: {} spot(s) left
        Compact:     {} spot(s) left
        Large:       {} spot(s) left
        Motorbike:   {} spot(s) left
        Electric:    {} spot(s) left
        """.format(self.handicappedFreeSpot,
                   self.compactFreeSpot,
                   self.largeFreeSpot,
                   self.motorbikerFreeSpot,
                   self.electricFreeSpot)
        print(string)


class ParkingSpot:
    def __init__(self,number,type):
        self.number=number
        self.free=True
        self.vehicle_in_place=Vehicle(None,None)
        self.type=type
    def __repr__(self):
        stt=lambda object: 'available' if object.free else 'unavailable'
        return '[SpotNumber: {}, Stat: {}, Type: {}, VehicleType: {}, LicenseNumber: {}]'.format(
            self.number,stt(self),self.type,self.vehicle_in_place.type,self.vehicle_in_place.licenseNumber)

class HandicappedSpot(ParkingSpot):
    def __init__(self,number):
        ParkingSpot.__init__(self,number,'Handicapped')

class CompactSpot(ParkingSpot):
    def __init__(self,number):
        ParkingSpot.__init__(self,number,'Compact')

class LargeSpot(ParkingSpot):
    def __init__(self,number):
        ParkingSpot.__init__(self,number,'Large')

class MotorbikeSpot(ParkingSpot):
    def __init__(self,number):
        ParkingSpot.__init__(self,number,'Motorbike')

class ElectricSpot(ParkingSpot):
    def __init__(self,number):
        ParkingSpot.__init__(self,number,'Electric')


class Vehicle:
    def __init__(self,licenseNumber,type):
        self.licenseNumber=licenseNumber
        self.type=type
        self.at_spot=None
        self.ticketAssigned=False
    def assignTicket(self):
        self.ticketAssigned=True
        self.ticket=ParkingTicket(self)


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
        Vehicle.__init__(self,licenseNumber,'MotorBike')



class Account:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.status='Active'

class Admin(Account):
    def __init__(self,username,password):
        Account.__init__(self,username,password)
    def addParkingFloor(self,parkinglot):
        parkinglot.adminOnly()
