---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: robotics
description: Robotics development with ROS 2, embedded control and simulation. Use when building robot software, ROS 2 nodes/packages, teleop, motor control, sensor fusion, path planning, microcontrollers in robots, or when users mention ROS, robotics, odometry, lidar, servo, motor, kinematics or gazebo simulation.
category: robotics
version: 0.1.0
author: devtiagoabreu
tags: [robotics, ros2, control, sensors, kinematics, simulation, motors]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - ROS 2 (Humble/Iron/Jazzy) installed on Ubuntu or a robotics container
  - A robot platform or simulator (Gazebo) for testing
  - Basic electronics for hardware: motors, encoders, sensor wiring
provides:
  - ROS 2 workspace and package setup
  - Node/publisher/subscriber patterns
  - Motor and servo control patterns
  - Odometry and sensor fusion approaches
  - Teleop and basic navigation
  - Simulation-first development workflow
difficulty: advanced
frameworks: [ros2, gazebo, micro-ros]
languages: [python, cpp]
---

# Robotics

## Overview

Robotics software is **event-driven** and **hardware-coupled**: code must be
testable without the robot. Develop in simulation, keep hardware drivers
behind clean interfaces, and always verify safety behavior (limits, e-stop)
before anything else.

## Prerequisites

- ROS 2 (Humble/Iron/Jazzy) installed on Ubuntu or a robotics container
- A robot platform or simulator (Gazebo) for testing
- Basic electronics for hardware: motors, encoders, sensor wiring

## 1. Architecture

```
Hardware (motors, lidar, camera, IMU)
   ↓ drivers (sensors publish)
ROS 2 Graph (nodes publish/subscribe on topics, services, actions)
   ↓
Behavior (perception → planning → control)
   ↓
Actuation (cmd_vel, joint commands)
```

Rules:
- **Simulation first:** develop in Gazebo/Webots; the same code must run on hardware.
- **Interfaces over nodes:** define message/interface packages (`my_robot_interfaces`) so nodes don't couple directly.
- **Never block the callback:** sensor callbacks must return fast; heavy logic in worker threads/timers.
- **Time is relative:** use `this->get_clock()->now()` / `rclpy` time, never `time()` wall for timestamps.

## 2. ROS 2 Workspace Setup

```bash
# ~/ros2_ws/src
source /opt/ros/humble/setup.bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws
ros2 pkg create --build-type ament_python my_bot
colcon build --symlink-install
source install/setup.bash
```

Check everything with `ros2 node list`, `ros2 topic list`, `ros2 topic echo /cmd_vel`.

## 3. Publisher/Subscriber Patterns

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Controller(Node):
    def __init__(self):
        super().__init__("controller")
        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.sub = self.create_subscription(LaserScan, "/scan", self.on_scan, 10)
        self.timer = self.create_timer(0.1, self.control_loop)

    def on_scan(self, scan: LaserScan):
        self.min_distance = min(scan.ranges) if scan.ranges else float("inf")

    def control_loop(self):
        cmd = Twist()
        cmd.linear.x = 0.1 if getattr(self, "min_distance", 9) > 0.5 else 0.0
        cmd.angular.z = 0.0
        self.pub.publish(cmd)

def main():
    rclpy.init()
    rclpy.spin(Controller())
    rclpy.shutdown()
```

### Safety callback pattern (drivers)

- Monitor motor currents and limit switches.
- On anomaly: publish zero velocity immediately (e-stop), log, and enter a safe state.
- Rate-limit re-enable: require explicit command to resume.

## 4. Motor and Servo Control

### DC motors + H-bridge (e.g. L298N, TB6612) via PWM

```cpp
// Arduino/ESP32 style (platform-specific API shown as reference)
const int ENA = 9, IN1 = 8, IN2 = 7;
void setMotor(int speed, bool forward) {
  analogWrite(ENA, abs(speed));          // 0..255
  digitalWrite(IN1, forward ? HIGH : LOW);
  digitalWrite(IN2, forward ? LOW : HIGH);
}
```

- Always enable PWM **soft start/stop** (ramp) to avoid current spikes.
- Drive both channels with the same reference for straight-line motion; add encoder feedback for reliable distance.

### Servo

```cpp
servo.write(90);   // 0..180°, sweep slowly; never slam to hard limits
```

- Power servos from a separate supply; a stalled servo on the MCU 5V rail resets the board.

### Odometry from encoders

```python
# ticks → meters: distance = (ticks / ticks_per_rev) * wheel_circumference
# per wheel; robot pose update via differential drive model
linear = (right + left) / 2
angular = (right - left) / track_width
x += linear * cos(theta); y += linear * sin(theta); theta += angular
```

## 5. Sensor Fusion

- **IMU:** gyro yaw drifts; high-rate, good for short-term orientation.
- **Encoders:** good linear/angular speed, drifts over distance.
- **Lidar:** excellent for localization/mapping (SLAM) — fuse with odometry via EKF (`robot_localization` package).
- Rule: trust **velocity-level** fusion (EKF on twist) over raw position averages.

## 6. Teleop and Navigation

- `ros2 run teleop_twist_keyboard teleop_twist_keyboard` for manual test.
- Nav2 for autonomous navigation: map via `slam_toolbox`/`cartographer`, plan with Nav2, localize with AMCL.
- Start with a **fixed map + AMCL**, then add SLAM; never deploy navigation without a recovery behavior (e-stop → replan).

## 7. Development Workflow (robot-safe)

1. Simulate the task in Gazebo (world → robot model → sensor).
2. Implement and tune in simulation with `ros2 launch`.
3. Log everything (`ros2 bag record -a`) for replay/debug.
4. Bench-test hardware with manual teleop first.
5. Only then run the autonomous behavior — with an e-stop reachable.

## Examples

### Example 1: Minimal ROS 2 package (ament_python)

```
my_bot/
├── package.xml
├── setup.py
├── resource/my_bot
└── my_bot/
    └── talker.py
```

```python
# talker.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__("talker")
        self.pub = self.create_publisher(String, "chatter", 10)
        self.timer = self.create_timer(1.0, self.tick)
        self.n = 0
    def tick(self):
        self.pub.publish(String(data=f"hello {self.n}")); self.n += 1
```

### Example 2: PID for line/angular control

```python
class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.err_sum = 0.0
        self.prev_err = 0.0
    def step(self, err, dt):
        self.err_sum = max(-5, min(5, self.err_sum + err * dt))
        d = (err - self.prev_err) / dt if dt > 0 else 0
        self.prev_err = err
        return self.kp * err + self.ki * self.err_sum + self.kd * d
```

## Notes

- Simulation-first: never debug on the physical robot what you can debug in Gazebo.
- Safety is a software requirement: e-stop, limits, current monitoring are features.
- Pin versions (ROS distro + packages) — the workspace is reproducible or it isn't.
- For MCU-only robots see `arduino-development`, `esp32-development`, `esp8266-development`.

## References

- [ROS 2 Documentation](https://docs.ros.org/en/rolling/index.html)
- [Nav2](https://docs.nav2.org/)
- [robot_localization](https://github.com/cra-ros-pkg/robot_localization)
- [Gazebo](https://gazebosim.org/)
