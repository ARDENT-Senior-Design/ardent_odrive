#!/usr/bin/env python
from __future__ import print_function

import rospy
import odrive_core

if __name__ == '__main__':
    try:
        print("Running Odrive")
        odrive_core.start_odrive()
    except rospy.ROSInterruptException:
        pass