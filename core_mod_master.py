# This is a collection of functions i found useful in
# the creation of my game, use share and extend as needed

import bge


from bge import logic
from mathutils import Vector
import math

#Global Variables in Module
ptag_len = 5
ttag_len = 4

# This script will attach one object to another instantly
# input: object *important* - obj name must be "object_name" + ".phys" ex) cube.phys
# there needs to be another point in the scene named "object_name" + ".tgt" ex cube.tgt
# this gives you a phys obj and a target obj
# the phys obj needs the "active" bool property so it sets it to active
#
def orient(input_obj):
    obj = input_obj
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    length = len(obj.name)
    master  = obj.name[:length-ptag_len]
    tgt = objects[master+'.tgt']
    obj.localOrientation = tgt.localOrientation

    
    
    
    
def attach(input_obj):
    obj = input_obj
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    length = len(obj.name)
    master  = obj.name[:length-ptag_len]
    tgt = objects[master+'.tgt']
    obj.worldPosition = tgt.worldPosition
    obj.setParent(tgt,0,0)
    obj["active"] = True


def drop(input_obj):
    obj = input_obj
    obj.removeParent()
    obj["active"] = False
    
    
def attract(input_obj):
    obj = input_obj
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    length = len(obj.name)                    #more string magic :D
    master  = obj.name[:length-ptag_len]
    tgt = objects[master+'.tgt']
    
    min_snap = 0.15
    distance = (obj.worldPosition - tgt.worldPosition).length

    if obj["active"] == False:
        bge.render.drawLine(obj.worldPosition,tgt.worldPosition,(.1,0,1))
        obj.linVelocityMax = 2.0
        obj.setAngularVelocity((0,0,0),0)
        obj.setLinearVelocity((0,0,0),0)
        obj.applyForce((0,0,obj.mass*9.8),0)
        force = 700.0 * float(obj.mass)
        becter = (-obj.worldPosition+tgt.worldPosition)
        obj.applyForce((float(force))*((becter)*2),0)
    
        if distance <= min_snap:
            obj.applyForce((0,0,obj.mass*9.8),0)
            obj.worldPosition = tgt.worldPosition
            obj.setParent(tgt,0,0)
            obj["active"] = True



#unfinished 
def grab(input_obj):
    #local data
    obj = input_obj
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    length = len(obj.name)
                      #more string magic :D
    master  = obj.name[:length-ptag_len]
    tgt = objects[master+'.tgt']
    
    #hooke's law Force = -(spring const*offset)
    #obj.applyImpulse(pos,force)
    offset = (obj.worldPosition - tgt.worldPosition)
    const = 500
    spring_f = const * (offset - 0.01*offset.normalized())
    pulse = spring_f/bge.logic.getLogicTicRate()
     
    #obj.applyImpulse(obj.worldPosition-tgt.worldPositon,pulse)
    ####
    
    min_snap = 0.15
    distance = (obj.worldPosition - tgt.worldPosition).length
    #speed = 0.3 / distance
    
    #freeze
    if obj["active"] == False:
        #speed = 0.3 / distance
        bge.render.drawLine(obj.worldPosition,tgt.worldPosition,(.1,0,1))
        obj.linVelocityMax = 2.0
        #obj.applyImpulse(obj.worldPosition-tgt.worldPosition,-pulse)
        obj.setAngularVelocity((0,0,0),0)
        obj.setLinearVelocity((0,0,0),0)
        obj.applyForce((0,0,obj.mass*9.8),0)
        #obj.applyImpulse(obj.worldPosition-tgt.worldPosition,-pulse)
        force = 100.0 * float(obj.mass)
        #obj.applyForce((distance)*(float(force))*(-obj.worldPosition+tgt.worldPosition),0)
        becter = (-obj.worldPosition+tgt.worldPosition)
        obj.applyForce((float(force))*((becter)*2),0)
    
        if distance <= min_snap:
            #activate spring
            obj.applyImpulse(obj.worldPosition-tgt.worldPosition,-pulse)
            
            obj["active"] = True



#return 0;


   
