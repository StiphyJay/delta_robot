#! /usr/bin/env python
import roslib; roslib.load_manifest('delta_robot')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point
from std_msgs.msg import Float64
import rospy
from math import *
from delta_construct import create_delta_simulation, set_initial_delta_pose, move_simulation_to_point
from delta_kinematics import *
from transformations import *
import numpy as np
import random

global pub1
pub1 = rospy.Publisher('/motor1/command', Float64)
global pub2
pub2 = rospy.Publisher('/motor2/command', Float64)
global pub3
pub3 = rospy.Publisher('/motor3/command', Float64)


def move_dynamixels(alpha, beta, theta):
    global pub1
    pub1.publish(Float64(math.radians(alpha)))
    global pub2
    pub2.publish(Float64(math.radians(beta)))
    global pub3
    pub3.publish(Float64(math.radians(theta)))

#def move_simulation_to_point(x, y, z, simulationMarkerArray):
#    endpoint = Point(x, y, z)
#    angles = delta_calcInverse(x, y, z)
#    print angles
#
#
#
#    for m in simulationMarkerArray.markers:
#        if m.id == 4: # from dyn1 to elbow1
#            # For dyn1:
#            pbase = (0.0, - 0.06 * sqrt(2), 0)
#            pfinal = (0.0, - 0.06 * sqrt(2) - 0.08, 0.0)
#            vecarrow = (pfinal[0] - pbase[0], pfinal[1] - pbase[1], pfinal[2] - pbase[2])
#
#            #rotate de the vector over an axis by some angle.
#            e1 = (1,0,0) # over X axis as dyn1 is over Y axis
#            # rotation_matrix( angle, reference axis, point=(optional))
#            M = rotation_matrix(np.radians(angles[1]*-1), e1)
#            rotvecarrow = numpy.dot(vecarrow, M[:3,:3].T)
#            newendpoint = pbase + rotvecarrow
#            # We got the new point
#            m.points[1] = Point( newendpoint[0], newendpoint[1], newendpoint[2])
#            
#        elif m.id == 5: # from dyn2 to elbow2
#            # For dyn2:
#            pbase = (0.06, 0.06, 0.0)
#            pfinal = (0.06 + 0.056568542, 0.06 + 0.056568542, 0.0)
#            vecarrow = (pfinal[0] - pbase[0], pfinal[1] - pbase[1], pfinal[2] - pbase[2])
#            #rotate de the vector over an axis by some angle.
#            e1 = (-1,1,0) # over its needed axis
#            # rotation_matrix( angle, reference axis, point=(optional))
#            M = rotation_matrix(np.radians(angles[2]*-1), e1)
#            rotvecarrow = numpy.dot(vecarrow, M[:3,:3].T)
#            newendpoint = pbase + rotvecarrow
#            # We got the new point
#            m.points[1] = Point( newendpoint[0], newendpoint[1], newendpoint[2])
#            
#
#        elif m.id == 6: # from dyn3 to elbow3
#            # For dyn3:
#            pbase = (- 0.06 , 0.06, 0.0)
#            pfinal = (-0.06 - 0.056568542, 0.06 + 0.056568542, 0.0)
#            vecarrow = (pfinal[0] - pbase[0], pfinal[1] - pbase[1], pfinal[2] - pbase[2])
#            #rotate de the vector over an axis by some angle.
#            e1 = (1,1,0) 
#            # rotation_matrix( angle, reference axis, point=(optional))
#            M = rotation_matrix(np.radians(angles[3]), e1)
#            rotvecarrow = numpy.dot(vecarrow, M[:3,:3].T)
#            newendpoint = pbase + rotvecarrow
#            # We got the new point
#            m.points[1] = Point( newendpoint[0], newendpoint[1], newendpoint[2])
#        elif m.id == 7: # from elbow1 to end
#             m.points[0] = simulationMarkerArray.markers[3].points[1] # index is number -1
#             m.points[1] = endpoint
#        elif m.id == 8: # from elbow2 to end
#             m.points[0] = simulationMarkerArray.markers[4].points[1]
#             m.points[1] = endpoint
#        elif m.id == 9: # from elbow3 to end
#             m.points[0] = simulationMarkerArray.markers[5].points[1]
#             m.points[1] = endpoint
#
#    return simulationMarkerArray

topic = 'delta_simulation'
publisher = rospy.Publisher(topic, MarkerArray)

rospy.init_node('delta_robot')

markerArray = create_delta_simulation()
initializedMarkerArray = set_initial_delta_pose(markerArray)


try:
    f = open('valid_points.txt', 'a')
    onlyone = True
    while not rospy.is_shutdown():
        theta = 1
        idcount = 15
        testpointscale = 0.002
        while  theta < 90 and onlyone:
            print "Setting all dynamixel to " + str(theta)
            print "Forward kinematics give us: "
            posefinal = delta_calcForward(theta, theta, theta)
            print posefinal
            print "\n"
            theta += 1
    
            
            testpoint = Marker()
            testpoint.header.frame_id = "/map"
            testpoint.type = testpoint.SPHERE
            testpoint.action = testpoint.ADD
            testpoint.scale.x = testpointscale
            testpoint.scale.y = testpointscale
            testpoint.scale.z = testpointscale
            testpoint.color.a = 1.0
            testpoint.color.r = 1.0
            testpoint.color.g = 1.0
            testpoint.color.b = 1.0
            testpoint.pose.orientation.w = 1.0
            testpoint.pose.position.x = posefinal[1] 
            testpoint.pose.position.y = posefinal[2] 
            testpoint.pose.position.z = posefinal[3]
            print "Testpoint position:\n" + str(testpoint.pose.position)
            print "\n"
            testpoint.id = idcount
            idcount += 1
   
            # Llamar a funcion que mueve los motores move_dynamixels( alpha, beta, theta)
            move_dynamixels(theta, theta, theta)
            initializedMarkerArray = move_simulation_to_point(posefinal[1], posefinal[2], posefinal[3], initializedMarkerArray)
                
            
            print "Inverse for this point"
            angles = delta_calcInverse(posefinal[1], posefinal[2], posefinal[3])
            print str(angles[1]) + ", "+ str(angles[2]) + ", "+ str(angles[3])
            #print str(math.degrees(angles[1])) + ", "+ str(math.degrees(angles[2])) + ", "+ str(math.degrees(angles[3]))
    
            print "\n"
            
            initializedMarkerArray.markers.append(testpoint)
             # Publish the MarkerArray
            publisher.publish(initializedMarkerArray)
            rospy.sleep(0.02)
            
            
        theta1 = 1
        while  theta1 < 90 and onlyone:
            print "Setting dynamixel1 to " + str(theta1)
            print "Forward kinematics give us: "
            posefinal = delta_calcForward(theta1, 0, 0)
            print posefinal
            print "\n"
            theta1 += 1
    
            
            testpoint = Marker()
            testpoint.header.frame_id = "/map"
            testpoint.type = testpoint.SPHERE
            testpoint.action = testpoint.ADD
            testpoint.scale.x = testpointscale
            testpoint.scale.y = testpointscale
            testpoint.scale.z = testpointscale
            testpoint.color.a = 1.0
            testpoint.color.r = 1.0
            testpoint.color.g = 1.0
            testpoint.color.b = 1.0
            testpoint.pose.orientation.w = 1.0
            testpoint.pose.position.x = posefinal[1] 
            testpoint.pose.position.y = posefinal[2] 
            testpoint.pose.position.z = posefinal[3]
    
            testpoint.id = idcount
            idcount += 1
         
            move_dynamixels(theta1, 0, 0)   
            initializedMarkerArray = move_simulation_to_point(posefinal[1], posefinal[2], posefinal[3], initializedMarkerArray)
                
            
            print "Inverse for this point"
            angles = delta_calcInverse(posefinal[1], posefinal[2], posefinal[3])
            print str(angles[1]) + ", "+ str(angles[2]) + ", "+ str(angles[3])
            #print str(math.degrees(angles[1])) + ", "+ str(math.degrees(angles[2])) + ", "+ str(math.degrees(angles[3]))
    
            print "\n"
            
            initializedMarkerArray.markers.append(testpoint)
             # Publish the MarkerArray
            publisher.publish(initializedMarkerArray)
            rospy.sleep(0.02)
            
        theta2 = 1
        while  theta2 < 90 and onlyone:
            print "Setting  dynamixel2 to " + str(theta2)
            print "Forward kinematics give us: "
            posefinal = delta_calcForward(0, theta2, 0)
            print posefinal
            print "\n"
            theta2 += 1
    
            
            testpoint = Marker()
            testpoint.header.frame_id = "/map"
            testpoint.type = testpoint.SPHERE
            testpoint.action = testpoint.ADD
            testpoint.scale.x = testpointscale
            testpoint.scale.y = testpointscale
            testpoint.scale.z = testpointscale
            testpoint.color.a = 1.0
            testpoint.color.r = 1.0
            testpoint.color.g = 1.0
            testpoint.color.b = 1.0
            testpoint.pose.orientation.w = 1.0
            testpoint.pose.position.x = posefinal[1] 
            testpoint.pose.position.y = posefinal[2] 
            testpoint.pose.position.z = posefinal[3]
    
            testpoint.id = idcount
            idcount += 1
    
            move_dynamixels(0, theta2, 0)
            initializedMarkerArray = move_simulation_to_point(posefinal[1], posefinal[2], posefinal[3], initializedMarkerArray)
               
            
            print "Inverse for this point"
            angles = delta_calcInverse(posefinal[1], posefinal[2], posefinal[3])
            print str(angles[1]) + ", "+ str(angles[2]) + ", "+ str(angles[3])
            #print str(math.degrees(angles[1])) + ", "+ str(math.degrees(angles[2])) + ", "+ str(math.degrees(angles[3]))
    
            print "\n"
            
            initializedMarkerArray.markers.append(testpoint)
             # Publish the MarkerArray
            publisher.publish(initializedMarkerArray)
            rospy.sleep(0.02)
#            
        theta3 = 1
        while  theta3 < 90 and onlyone:
            print "Setting dynamixel3 to " + str(theta3)
            print "Forward kinematics give us: "
            posefinal = delta_calcForward(0, 0, theta3)
            print posefinal
            print "\n"
            theta3 += 1
    
            
            testpoint = Marker()
            testpoint.header.frame_id = "/map"
            testpoint.type = testpoint.SPHERE
            testpoint.action = testpoint.ADD
            testpoint.scale.x = testpointscale
            testpoint.scale.y = testpointscale
            testpoint.scale.z = testpointscale
            testpoint.color.a = 1.0
            testpoint.color.r = 1.0
            testpoint.color.g = 1.0
            testpoint.color.b = 1.0
            testpoint.pose.orientation.w = 1.0
            testpoint.pose.position.x = posefinal[1] 
            testpoint.pose.position.y = posefinal[2] 
            testpoint.pose.position.z = posefinal[3]
    
            testpoint.id = idcount
            idcount += 1
    
            move_dynamixels(0, 0, theta3)
            initializedMarkerArray = move_simulation_to_point(posefinal[1], posefinal[2], posefinal[3], initializedMarkerArray)
                
            
            print "Inverse for this point"
            angles = delta_calcInverse(posefinal[1], posefinal[2], posefinal[3])
            print str(angles[1]) + ", "+ str(angles[2]) + ", "+ str(angles[3])
            #print str(math.degrees(angles[1])) + ", "+ str(math.degrees(angles[2])) + ", "+ str(math.degrees(angles[3]))
    
            print "\n"
            
            initializedMarkerArray.markers.append(testpoint)
             # Publish the MarkerArray
            publisher.publish(initializedMarkerArray)
            rospy.sleep(0.02)
           
           
            
    
        
        onlyone = True
        publisher.publish(initializedMarkerArray)
    
    
        rospy.sleep(0.01)
    
except KeyboardInterrupt:
  # do nothing here
  f.close()
  pass
