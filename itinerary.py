# importing necessary libraries
from collections import OrderedDict
from flask import jsonify
from abc import abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flights import *
from location import *
import json

# Adding the Heroku URL
DB_URL = 'postgres://ugcuvkvpcdaixu:b624b6193c9e248af602f7239c6ddca6848239242adbcb31a9fd4685ac75aabf@ec2-204-236-228-169.compute-1.amazonaws.com:5432/d93me5889f2sp1'
# Building a connection to the database
engine = create_engine(DB_URL)
connection = engine.connect()


# Itinerary class to connect frontend to DB
class Itinerary( ) :

    # the constructor having the input ownerId and the list of tasks
    def __init__( self , ownerId = -1 , tasks = [ ] ) :
        self.ownerId = ownerId
        # self.tasks = processTasks( tasks )
        self.tasks = tasks
    #in the case where we are constructing the Itinerary object from the DB to pass to the frontend, a blank one will be instantiated
    #then initFromDB will be called to populate the member variables

    # adding a task to a preexisting list of tasks
    def appendTask( self , task ) :
        self.tasks += task ,

    # returning the list of tasks
    def getTasks( self ) :
        return self.tasks

    # checking whether the id of the task is valid if it can be returned
    # else returning invalid statement.
    def getTask( self , idx ) :
        if id > len( self.tasks ) :
            return self.tasks[ idx ]
        else :
            return "Invalid Task"

    # checking whether the id of the task is valid if it can be removed
    # else printing error statement
    def removeTask( self , idx ) :
        if id > len( self.tasks ) :
            self.tasks.pop( idx )
        else :
            print( "Invalid Task" )

    # returning the index of the task if that exists else printing error statement
    def getIndex( self , task ) :
        if task in self.tasks :
            return self.tasks.index( task )
        return "Invalid Task"

    # returning the task from the list if that exists else printing error statement
    def removeTask( self , task ) :
        if task in self.tasks :
            self.tasks.remove( task )
        else :
            print( "Invalid Task" )

    def processTasks( self , tasks ) :
        if( tasks ) :
            tasks = tasks[ 1 : -1 ].replace( '"' , '' ).split( ',' )
        return tasks

    # the itinerary comprising of all the tasks for a respective user id
    def saveItinerary( self ) :
        tasksAsSQLArray = ''
        for task in self.tasks:
            tasksAsSQLArray += (',\"' + task + '\"')
        tasksAsSQLArray = '{' + tasksAsSQLArray[1:] + '}'
        connection.execute( "INSERT INTO itinerary values ({}, (\'{}\'));".format( self.ownerId , tasksAsSQLArray ) )

    # # assuming the itinerary to handle string to list manipulation
    def initFromDB( self ) :
        summary = connection.execute( "SELECT * FROM itinerary WHERE owner_id={}".format( self.ownerId ) ).fetchall( )
        print( summary )
        self.tasks = summary[ 1 ]

    #For use when ownerID is not yet in the object
    # def initFromDB( self , newOwnerId ) :
    #     summary = connection.execute( "SELECT * FROM itinerary WHERE owner_id={}".format( newOwnerId ) ).fetchall( )
    #     self.tasks = summary[ 1 ]

    # returning json object of the list of tasks
    def productJson( self ) :
        return json.dumps( { "tasks" : self.tasks } )
