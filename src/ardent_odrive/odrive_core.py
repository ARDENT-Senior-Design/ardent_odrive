#!/usr/bin/env python
from __future__ import print_function

#import roslib; roslib.load_manifest('BINCADDY')
import rospy
import tf.transformations
import tf_conversions
import tf2_ros

from std_msgs.msg import Float64, Int32
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
import std_srvs.srv

import time
import math
import traceback
import Queue

from odrive_interface import ODriveInterfaceAPI, ODriveFailure

class ROSLogger(object):
    """Imitate a standard Python logger, but pass the messages to rospy logging.
    """
    def debug(self, msg):    rospy.logdebug(msg)  #  print(msg) #
    def info(self, msg):     rospy.loginfo(msg)   #  print(msg) #
    def warn(self, msg):     rospy.logwarn(msg)   #  print(msg) #
    def error(self, msg):    rospy.logerr(msg)    #  print(msg) #
    def critical(self, msg): rospy.logfatal(msg)  #  print(msg) #
    
    # use_index = False (bool)
    # offset_float = 0.590887010098 (float)
    # calib_range = 0.019999999553 (float)
    # mode = 0 (int)
    # offset = 1809 (int)
    # cpr = 4096 (int)
    # idx_search_speed = 10.0 (float)
    # pre_calibrated = False (bool)

#m_s_to_rpm = 60.0/tyre_circumference
#m_s_to_erpm = 10 * m_s_to_rpm 

# 4096 counts / rev, so 4096 == 1 rev/s


# 1 m/s = 3.6 km/hr

class ODriveNode(object):
    # last_speed = 0.0
    # driver = None
    # prerolling = False
    
    # # Robot wheel_track params for velocity -> motor speed conversion
    # wheel_track = None
    # tyre_circumference = None
    # encoder_counts_per_rev = None
    # m_s_to_value = 1.0
    # axis_for_right = 0
    # encoder_cpr = 4096
    
    # # Startup parameters
    # connect_on_startup = False
    # calibrate_on_startup = False
    # engage_on_startup = False

    
    def __init__(self):
        
        self.index = float(rospy.get_param('~odrive_index',0))
        self.connect_on_startup   = rospy.get_param('~connect_on_startup', False)
        self.calibrate_on_startup = rospy.get_param('~calibrate_on_startup', False)
        self.engage_on_startup    = rospy.get_param('~engage_on_startup', False)
        
        self.has_preroll     = rospy.get_param('~use_preroll', True)
                
        self.publish_current = rospy.get_param('~publish_current', True)
        self.publish_odom = rospy.get_param('~publish_odom', True)
        
        self.publish_tf      = rospy.get_param('~publish_odom_tf', False)
        self.odom_topic      = rospy.get_param('~odom_topic', "odom")
        self.odom_frame      = rospy.get_param('~odom_frame', "odom")
        self.base_frame      = rospy.get_param('~base_frame', "base_link")
        self.odom_calc_hz    = rospy.get_param('~odom_calc_hz', 25)
        
        rospy.on_shutdown(self.terminate)

        rospy.Service('connect_driver',    std_srvs.srv.Trigger, self.connect_driver)
        rospy.Service('disconnect_driver', std_srvs.srv.Trigger, self.disconnect_driver)
    
        rospy.Service('calibrate_motors',  std_srvs.srv.Trigger, self.calibrate_motor)
        rospy.Service('engage_motors',     std_srvs.srv.Trigger, self.engage_motor)
        rospy.Service('release_motors',    std_srvs.srv.Trigger, self.release_motor)
        
        self.command_queue = Queue.Queue(maxsize=5)
        self.vel_subscribe = rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback, queue_size=2)
        self.torque_subscribe = rospy.Subscriber("/cmd_torque", Twist, self.cmd_torque_callback, queue_size=2)
        
        if self.publish_current:
            self.current_loop_count = 0
            self.current_accumulator_1  = 0.0
            self.current_accumulator_0 = 0.0
            self.current_publisher_1  = rospy.Publisher('odrive/current_1', Float64, queue_size=2)
            self.current_publisher_0 = rospy.Publisher('odrive/current_0', Float64, queue_size=2)
            rospy.loginfo("ODrive will publish motor currents.")
        
        self.last_cmd_vel_time = rospy.Time.now()
        
        if self.publish_odom:
            self.raw_odom_publisher_encoder_1  = rospy.Publisher('odrive/raw_odom/encoder_1',   Int32, queue_size=2) if self.publish_odom else None
            self.raw_odom_publisher_encoder_0 = rospy.Publisher('odrive/raw_odom/encoder_0',  Int32, queue_size=2) if self.publish_odom else None
            self.raw_odom_publisher_vel_1      = rospy.Publisher('odrive/raw_odom/velocity_1',  Float64, queue_size=2) if self.publish_odom else None
            self.raw_odom_publisher_vel_0     = rospy.Publisher('odrive/raw_odom/velocity_0', Float64, queue_size=2) if self.publish_odom else None
            rospy.loginfo("ODrive will publish encoder position and velocity.")
                            

    def fast_timer(self, timer_event):
            time_now = rospy.Time.now()
            # in case of failure, assume some values are zero
            self.vel_1 = 0
            self.vel_0 = 0
            self.pos_1 = 0
            self.pos_0 = 0
            self.current_1 = 0
            self.current_0 = 0
            
            # Handle reading from Odrive and sending odometry
            if self.fast_timer_comms_active:
                try:
                    # read all required values from ODrive for odometry
                    self.encoder_cpr = self.driver.encoder_cpr
                    
                    self.vel_1 = self.driver.axis_1.encoder.vel_estimate  # units: encoder counts/s
                    self.vel_0 = self.driver.axis_0.encoder.vel_estimate # neg is forward for right
                    self.pos_1 = self.driver.axis_1.encoder.pos_cpr    # units: encoder counts
                    self.pos_0 = self.driver.axis_0.encoder.pos_cpr  # sign!
                    
                    # for currents
                    self.current_1 = self.driver.axis_1.motor.current_control.Ibus
                    self.current_0 = self.driver.axis_0.motor.current_control.Ibus
                    
                except:
                    rospy.logerr("Fast timer exception reading:" + traceback.format_exc())
                    self.fast_timer_comms_active = False
                    
            # odometry is published regardless of ODrive connection or failure (but assumed zero for those)
            # as required by SLAM
            if self.publish_odom:
                self.publish_odometry(time_now)
            if self.publish_current:
                self.pub_current()
                
            # check and stop motor if no vel command has been received in > 1s
            try:
                if self.fast_timer_comms_active and \
                        (time_now - self.last_cmd_vel_time).to_sec() > 2.0 and \
                        self.driver.engaged(): #(self.last_speed > 0):
                    #rospy.logdebug("No /cmd_vel received in > 1s, stopping.")
                
                    self.driver.drive(0,0)
                    self.last_speed = 0
                    self.last_cmd_vel_time = time_now
                    self.driver.release() # and release
            except:
                rospy.logerr("Fast timer exception on cmd_vel timeout:" + traceback.format_exc())
                self.fast_timer_comms_active = False
            
            # handle sending drive commands.
            # from here, any errors return to get out
            if self.fast_timer_comms_active and not self.command_queue.empty():
                # check to see if we're initialised and engaged motor
                try:
                    if not self.driver.prerolled():
                        self.driver.preroll()
                        return
                except:
                    rospy.logerr("Fast timer exception on preroll:" + traceback.format_exc())
                    self.fast_timer_comms_active = False                
                
                try:
                    motor_command = self.command_queue.get_nowait()
                except Queue.Empty:
                    rospy.logerr("Queue was empty??" + traceback.format_exc())
                    return
                
                if motor_command[0] == 'drive':
                    try:
                        if not self.driver.engaged():
                            self.driver.engage()
                            
                        linear_val_1, linear_val_0 = motor_command[1]
                        self.driver.drive(linear_val_1, linear_val_0)
                        self.last_speed = max(abs(linear_val_1), abs(linear_val_0))
                        self.last_cmd_vel_time = time_now
                    except:
                        rospy.logerr("Fast timer exception on drive cmd:" + traceback.format_exc())
                        self.fast_timer_comms_active = False
                elif motor_command[0] == 'release':
                    pass
                # ?
                else:
                    pass
        
    def main_loop(self):
        # Main control, handle startup and error handling
        # while a ROS timer will handle the high-rate (~50Hz) comms + odometry calcs
        main_rate = rospy.Rate(1) # hz
        # Start timer to run high-rate comms
        self.fast_timer = rospy.Timer(rospy.Duration(1/float(self.odom_calc_hz)), self.fast_timer)
        
        self.fast_timer_comms_active = False
        
        while not rospy.is_shutdown():
            try:
                main_rate.sleep()
            except rospy.ROSInterruptException: # shutdown / stop ODrive??
                break
            
            # fast timer running, so do nothing and wait for any errors
            if self.fast_timer_comms_active:
                continue
            
            # check for errors
            if self.driver:
                try:
                    # driver connected, but fast_comms not active -> must be an error?
                    if self.driver.get_errors(clear=True):
                        rospy.logerr("Had errors, disconnecting and retrying connection.")
                        self.driver.disconnect()
                        self.driver = None
                    else:
                        # must have called connect service from another node
                        self.fast_timer_comms_active = True
                except:
                    rospy.logerr("Errors accessing ODrive:" + traceback.format_exc())
                    self.driver = None
            
            if not self.driver:
                if not self.connect_on_startup:
                    #rospy.loginfo("ODrive node started, but not connected.")
                    continue
                
                if not self.connect_driver(None)[0]:
                    rospy.logerr("Failed to connect.") # TODO: can we check for timeout here?
                    continue
            
            else:
                pass # loop around and try again
        
    def terminate(self):
        self.fast_timer.shutdown()
        if self.driver:
            self.driver.release()

    

    # ROS services
    def connect_driver(self, request):
        if self.driver:
            return (False, "Already connected.")
        
        self.driver = ODriveInterfaceAPI(logger=ROSLogger())
        rospy.loginfo("Connecting to ODrive...")
        
        if self.publish_odom:
            self.old_pos_1 = self.driver.axis_1.encoder.pos_cpr
            self.old_pos_0 = self.driver.axis_0.encoder.pos_cpr
        
        self.fast_timer_comms_active = True
        
        return (True, "ODrive connected successfully")
    
    def disconnect_driver(self, request):
        if not self.driver:
            rospy.logerr("Not connected.")
            return (False, "Not connected.")
        try:
            if not self.driver.disconnect():
                return (False, "Failed disconnection, but try reconnecting.")
        except:
            rospy.logerr('Error while disconnecting: {}'.format(traceback.format_exc()))
        finally:
            self.driver = None
        return (True, "Disconnection success.")
    
    def calibrate_motor(self, request):
        if not self.driver:
            rospy.logerr("Not connected.")
            return (False, "Not connected.")
            
        if self.has_preroll:
            if not self.driver.preroll():
                return (False, "Failed preroll.")        
        else:
            if not self.driver.calibrate():
                return (False, "Failed calibration.")
                
        return (True, "Calibration success.")
                    
    def engage_motor(self, request):
        if not self.driver:
            rospy.logerr("Not connected.")
            return (False, "Not connected.")
        if not self.driver.engage():
            return (False, "Failed to engage motor.")
        return (True, "Engage motor success.")
    
    def release_motor(self, request):
        if not self.driver:
            rospy.logerr("Not connected.")
            return (False, "Not connected.")
        if not self.driver.release():
            return (False, "Failed to release motor.")
        return (True, "Release motor success.")
    
    def reset_odometry(self, request):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        return(True, "Odometry reset.")

    def cmd_pos_callback(self, msg):
        trg_pos = 1

    def cmd_vel_callback(self, msg):
        linear_val_0 = 1
        linear_val_1 = 1
        try:
            # TODO: rename drive_command to velo_command and add a pos_command
            drive_command = ('drive', (linear_val_1, linear_val_0)) 
            self.command_queue.put_nowait(drive_command)
        except Queue.Full:
            pass
            
        self.last_cmd_vel_time = rospy.Time.now()

    def cmd_torque_callback(self, msg):
        torque_val_0 = 1
        torque_val_1 = 1
        # convert torque to current based on calculated torque constant
        # try:
        #     # effort_command = 
        # except Queue.Full:
        #     pass
    
    def publish_odometry(self, time_now):
        now = time_now
        # self.odom_msg.header.stamp = now
        # self.tf_msg.header.stamp = now

        if self.publish_odom:
            self.raw_odom_publisher_encoder_1.publish(self.pos_1)
            self.raw_odom_publisher_encoder_0.publish(self.pos_0)
            self.raw_odom_publisher_vel_1.publish(self.vel_1)
            self.raw_odom_publisher_vel_0.publish(self.vel_0)
        
        # ... If anything weird regarding higher level odometry (like tracking a wheeled robot) put it here
        # ... 
        # self.odom_publisher.publish(self.odom_msg)

    def pub_current(self):
        current_quantizer = 5
        
        self.current_accumulator_1 += self.current_1
        self.current_accumulator_0 += self.current_0
    
        self.current_loop_count += 1
        if self.current_loop_count >= current_quantizer:
            self.current_publisher_1.publish(float(self.current_accumulator_1) / current_quantizer)
            self.current_publisher_0.publish(float(self.current_accumulator_0) / current_quantizer)
    
            self.current_loop_count = 0
            self.current_accumulator_1 = 0.0
            self.current_accumulator_0 = 0.0    

def start_odrive():
    rospy.init_node('odrive')
    odrive_node = ODriveNode()
    print("Odrive Initialized")
    odrive_node.main_loop()
    #rospy.spin() 
    
if __name__ == '__main__':
    try:
        start_odrive()
    except rospy.ROSInterruptException:
        pass
