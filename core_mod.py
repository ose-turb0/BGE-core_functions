#This module is meant to be accessed by python code
#you can try to use this with logic bricks, i haven't yet xD
#remenants are old functionality/unfinished ideas
#enable if you dare...

import bge
from bge import constraints
from mathutils import Vector
import math
#Global Variables in Module
ptag_len = 5
ttag_len = 4

scene = bge.logic.getCurrentScene()



def dice(in_obj):
    
    infin_life = 0
    life = 0
    
    m_v = [0.0,0.0,0.0]
    
    s = []
    s.clear()
        
    #own.suspendDynamics()
    #find the axis with highest value 
    own = in_obj #save my ass some time xD
    for n in own.localScale:
        s.append(n)
            
    m = max(s)
    mdx = s.index(m)
    s.clear()
          
        #to frac or not
    if own.localScale[mdx] > 0.1:
            
            
        if own.localScale[mdx] <= 0.4:
                
            if own.localScale[0] == own.localScale[1] and own.localScale[0] == own.localScale[2]:
                #if small cube despawn after a bit
                #resize - dupe - rescale - rescale - rescale - move
                own.localScale[mdx] = own.localScale[mdx]/2
                copy1 = scene.addObject(own.name,own,life)
                copy2 = scene.addObject(own.name,own,life)
                copy1.localScale = own.localScale
                copy2.localScale = own.localScale
                
                m_v[mdx] = copy1.localScale[mdx]/2
                copy1.applyMovement(m_v,True)
                    
                m_v[mdx] = -copy2.localScale[mdx]/2
                copy2.applyMovement(m_v,True)
                    
                   
                copy1.restoreDynamics()
                copy2.restoreDynamics()
                    
                    #copy1.setLinearVelocity((0,0,0),0)
                    #copy2.setLinearVelocity((0,0,0),0)
                   
                m_v[mdx] = 0.0
                
                           
        else:
        
        
            own.localScale[mdx] = own.localScale[mdx]/2
         
            copy1 = scene.addObject(own.name,own,infin_life)
            copy2 = scene.addObject(own.name,own,infin_life)
                
            copy1.localScale = own.localScale
            copy2.localScale = own.localScale
                
            m_v[mdx] = copy1.localScale[mdx]/2
            copy1.applyMovement(m_v,True)
                
            m_v[mdx] = -copy2.localScale[mdx]/2
            copy2.applyMovement(m_v,True)
                
                
            copy1.suspendDynamics()
            copy2.suspendDynamics()
                
                
                #copy1.setLinearVelocity((0,0,0),0)
                #copy2.setLinearVelocity((0,0,0),0)
                
            m_v[mdx] = 0.0
            
            
        own.endObject()



#credit to that dude that wrote this, even though i dont use it xD
def getDimensions(in_obj):
    
    
    obj = in_obj
    mesh = obj.meshes[0]

    n_verts = mesh.getVertexArrayLength(0)


    def retrieveExtremalValues(mesh, n_verts):
    
        x1, y1, z1 = mesh.getVertex(0, 0).XYZ
        x2, y2, z2 = mesh.getVertex(0, 1).XYZ

    
        mins = [min(x1, x2), min(y1, y2), min(z1, z2)]
        maxs = [max(x1, x2), max(y1, y2), max(z1, z2)]

        for n in range(n_verts - 2):
    
            xyz = mesh.getVertex(0, n+2).XYZ

            for i in range(3):
                mins[i] = min(mins[i], xyz[i])
                maxs[i] = max(maxs[i], xyz[i])


        return mins + maxs

    if n_verts < 2:
        dimensions = [0, 0, 0]

    else:
    
        xm, ym, zm, xM, yM, zM = retrieveExtremalValues(mesh, n_verts)

        dimensions = [xM-xm, yM-ym, zM-zm]
        
        return dimensions


def make_joint(in_joint):
    
#def make_joint(in_joint,in_j_child,in_j_object):
    
    major = scene.objects[in_joint["major_b"]]
    minor = scene.objects[in_joint["minor_b"]]
     
    
    xlim1 = math.radians(in_joint["xlim1"])
    xlim2 = math.radians(in_joint["xlim2"])
    ylim1 = math.radians(in_joint["ylim1"])
    ylim2 = math.radians(in_joint["ylim2"])
    zlim1 = math.radians(in_joint["zlim1"])
    zlim2 = math.radians(in_joint["zlim2"])
    
    xangle = math.radians(in_joint["x_rot"])
    yangle = math.radians(in_joint["y_rot"])
    zangle = math.radians(in_joint["z_rot"])
    
    #print("angle: ",math.degrees(zangle))
    
    
    
    
    
    
    
    xoff = -(major.worldPosition.x - in_joint.worldPosition.x)
    yoff = -(major.worldPosition.y - in_joint.worldPosition.y)
    zoff = -(major.worldPosition.z - in_joint.worldPosition.z)
    
    #print("x offset = ",xoff)
    #print("y offset = ",yoff)
    #print("z offset = ",zoff)
    
    
    #Type 
    constraintType = bge.constraints.GENERIC_6DOF_CONSTRAINT
    
    #ID
    minor_id = minor.getPhysicsId()
    major_id = major.getPhysicsId()
    
    
    out_cont = constraints.createConstraint(
                            major_id, #obj 1 physics Id
                            minor_id, #obj 2 physics Id
                            constraintType, #constraint type 12 = 6DOF
                            xoff,     #pos x
                            yoff,     #pos y
                            zoff,     #pos z
                            xangle,     #piv axis x
                            yangle,     #piv axis y
                            zangle,     #piv axis z
                            128)     #flag
                            
    out_cont.setParam(3,xlim1,xlim2)
    out_cont.setParam(4,ylim1,ylim2)
    out_cont.setParam(5,zlim1,zlim2)
    
    
    return out_cont

def debug_vis(input_obj):
    scene = bge.logic.getCurrentScene()
    dbg = scene.objects["db_ico_g"]
    scene.addObject("db_ico_g",input_obj,0)
    dbg.setParent(input_obj,0,1)
    dbg.localOrientation = input_obj.localOrientation
    

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
    
    #remenants
    #bge.render.drawLine(obj.worldPosition,obj.worldPosition + Vector((5.0, 0.0, 0.0)),(.1,1,0))
    #obj_xyz = obj.localOrientation.to_euler()
    #tgt_xyz = obj.localOrientation.to_euler()
    #rotz = math.degrees(xyz[2])
    #xyz[2] = math.radians(45)
    obj.localOrientation = tgt.localOrientation
    #print(rotz)
    
    
    
    
def attach(input_obj):
    obj = input_obj
    scene = bge.logic.getCurrentScene()
    objects = scene.objects
    length = len(obj.name)
                      #more string magic :D
    
    master  = obj.name[:length-ptag_len]
    tgt = objects[master+'.tgt']
    
    #bge.render.drawLine(obj.worldPosition,tgt.worldPosition,(.1,1,0))
    
    obj.worldPosition = tgt.worldPosition
    obj.setParent(tgt,0,0)
    obj["active"] = True
    
    #print(obj.name)




def drop(input_obj):
    obj = input_obj
    obj.removeParent()
    obj["active"] = False
    
    
def attract(input_obj):
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
    
    xvect = tgt.getAxisVect([1.0,0.0,0.0])
    yvect = tgt.getAxisVect([0.0,1.0,0.0])
    zvect = tgt.getAxisVect([0.0,0.0,0.1])
    
    #freeze
    if obj["active"] == False:
        #speed = 0.3 / distance
        bge.render.drawLine(obj.worldPosition,tgt.worldPosition,(.1,1,0))
        #bge.render.drawLine(obj.worldPosition,tgt.worldPosition,(.1,0,1))
        obj.linVelocityMax = 2.0
        #obj.applyImpulse(obj.worldPosition-tgt.worldPosition,-pulse)
        obj.setAngularVelocity((0,0,0),0)
        obj.setLinearVelocity((0,0,0),0)
        
        obj.alignAxisToVect(xvect,0,0.2)
        obj.alignAxisToVect(yvect,1,0.2)
        obj.alignAxisToVect(zvect,2,0.2)
        
        obj.applyForce((0,0,obj.mass*9.8),0)
        #obj.applyImpulse(obj.worldPosition-tgt.worldPosition,-pulse)
        force = 300 * float(obj.mass)
        #obj.applyForce((distance)*(float(force))*(-obj.worldPosition+tgt.worldPosition),0)
        becter = (-obj.worldPosition+tgt.worldPosition)
        obj.applyForce((float(force))*((becter)*2),0)
    
        if distance <= min_snap:
            obj.applyForce((0,0,obj.mass*9.8),0)
            obj.alignAxisToVect(xvect,0,1.0) #orientation fix
            obj.alignAxisToVect(yvect,1,1.0) #orientation fix
            obj.alignAxisToVect(zvect,2,1.0) #orientation fix
            #obj.applyForce((float(force*2))*((becter)*2),0) #unused
            obj.worldPosition = tgt.worldPosition
            #obj.localOrientation = tgt.localOrientation #fix this later...
            obj.setParent(tgt,0,0)
            obj["active"] = True


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
        force = 300.0 * float(obj.mass)
        #obj.applyForce((distance)*(float(force))*(-obj.worldPosition+tgt.worldPosition),0)
        becter = (-obj.worldPosition+tgt.worldPosition)
        obj.applyForce((float(force))*((becter)*2),0)
    
        #if distance <= min_snap:
            #activate spring
        #    obj.applyImpulse(obj.worldPosition-tgt.worldPosition,-pulse)
            
        #    obj["active"] = True



#return 0;


   
