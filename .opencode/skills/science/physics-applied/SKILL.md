---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: physics-applied
description: Force, energy, work and power with practical worked examples
category: science
version: 0.1.0
author: devtiagoabreu
tags: [physics, mechanics, force, energy, power, examples]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic algebra and unit handling
  - Understanding of vectors and coordinates at a basic level
provides:
  - Newton's laws with worked numerical problems
  - Kinetic, potential, and elastic energy calculations
  - Power, efficiency, and work examples
---

# Physics Applied

## Overview

This skill teaches the core mechanics used in engineering and everyday
technology: forces and Newton's laws, work and energy, and power with
efficiency. Each concept is introduced with the relevant equation and a fully
worked numerical example so you can reproduce the reasoning on your own
problems.

Special attention goes to units and to the sign conventions (direction matters
for forces and vectors). Most examples use the metric system: newtons (N),
joules (J), and watts (W).

## Prerequisites

- Comfort with basic algebra (solving for one variable)
- Knowledge of the SI units: m, kg, s, N, J, W
- Understanding of the difference between scalar and vector quantities

## Usage Instructions

### 1. Forces and Newton's Laws

The second law states that the net force on an object equals mass times
acceleration (F = ma). Weight is a force: w = mg, with g = 9.81 m/s² on Earth.

```text
Example 1 - Accelerating a cart:
  m = 20 kg, a = 3.0 m/s²
  F = m x a = 20 x 3.0 = 60 N
  (horizontal, ignoring friction)

Example 2 - Weight:
  w = m x g = 20 x 9.81 = 196.2 N

Example 3 - Crate on an incline (angle 30°, m = 10 kg, no friction):
  Component of weight along the slope: mg sin(30°) = 10 x 9.81 x 0.5
    = 49.05 N pulling down the slope
  Force needed to hold the crate: F = 49.05 N up the slope
  To move at constant speed: same magnitude, net force zero.

Example 4 - Friction:
  Normal force on a flat surface: N = w = 10 x 9.81 = 98.1 N
  Kinetic friction: f = mu x N = 0.30 x 98.1 = 29.43 N
  Net force to slide at constant velocity: 29.43 N
```

### 2. Work and Energy

Work is the force times the displacement along the direction of the force:
W = F d cos(theta). Kinetic energy is KE = (1/2) m v², and gravitational
potential energy is PE = m g h. The work-energy theorem links them.

```text
Work:
  F = 50 N, d = 4 m, same direction: W = 50 x 4 = 200 J
  F = 50 N, d = 4 m, angle 60°: W = 50 x 4 x cos(60) = 50 x 4 x 0.5 = 100 J
  Vertical lift: W = m g h = 10 x 9.81 x 3 = 294.3 J

Kinetic energy:
  m = 800 kg, v = 25 m/s: KE = 0.5 x 800 x 625 = 250,000 J
  Same mass at v = 50 m/s: KE = 0.5 x 800 x 2500 = 1,000,000 J
  -> doubling speed quadruples kinetic energy

Potential energy:
  m = 2 kg at h = 10 m: PE = 2 x 9.81 x 10 = 196.2 J

Work-energy theorem:
  Braking a 800 kg car from 25 m/s to rest:
  W = 0 - 250,000 = -250,000 J (work done by brakes)
  Stopping distance d with braking force F = 12,500 N:
  d = 250,000 / 12,500 = 20 m
```

### 3. Power and Efficiency

Power is the rate of doing work: P = W/t. For a force at constant velocity,
P = F v. Efficiency is useful output power divided by input power.

```text
Power examples:
  Lifting 10 kg a height of 3 m in 5 s:
    W = 10 x 9.81 x 3 = 294.3 J
    P = 294.3 / 5 = 58.9 W

  Motor pulling a load at 2.0 m/s with force 1,200 N:
    P = F x v = 1,200 x 2.0 = 2,400 W = 2.4 kW

Efficiency:
  Electric motor: input 2,800 W, output 2,400 W
  Efficiency = 2400 / 2800 = 0.857 (85.7%)
  Losses = 2800 - 2400 = 400 W (heat, friction)

Energy cost example:
  A 60 W bulb on for 8 hours:
    Energy = 60 x 8 = 480 Wh = 0.48 kWh
    At R$ 0.90/kWh: cost = 0.48 x 0.90 = R$ 0.43
```

## Examples

### Example 1: Free Fall and Conservation of Energy

```text
Ball dropped from h = 20 m, m = 0.5 kg, from rest.

At the top: PE = 0.5 x 9.81 x 20 = 98.1 J, KE = 0
At the ground (no air resistance): PE = 0, KE = 98.1 J
Speed at impact: v = sqrt(2 x 98.1 / 0.5) = sqrt(392.4) = 19.8 m/s
(Check by kinematics: v² = 2 g h -> v = sqrt(2 x 9.81 x 20) = 19.8 m/s)

Impact force if stopped over d = 0.5 m:
  Work of stopping = KE -> F x 0.5 = 98.1 -> F = 196.2 N
```

### Example 2: Projectile Range

```text
Launch speed v = 30 m/s at angle 45°, g = 9.81 m/s²

Range: R = (v² sin(2θ)) / g = (900 x sin(90°)) / 9.81 = 900 / 9.81 = 91.7 m

Time of flight: t = (2 v sin θ) / g = (2 x 30 x 0.7071) / 9.81
  = 42.43 / 9.81 = 4.33 s

Max height: h = (v² sin²θ) / (2 g) = (900 x 0.5) / (2 x 9.81)
  = 450 / 19.62 = 22.94 m
```

### Example 3: Simple Machine - Pulley

```text
Single fixed pulley: IMA = 1 (force equal to load)
Ideal mechanical advantage = d_in / d_out
Real pulley: lift 100 kg (981 N) pulling 1,100 N over 2 m
  Input work = 1,100 x 2 = 2,200 J
  Output work = 981 x 1.8 = 1,765.8 J  (actual lift 1.8 m)
  Efficiency = 1765.8 / 2200 = 0.803 (80.3%)
```

## Best Practices

- Use SI units throughout and convert before calculating
- Draw a free-body diagram before applying F = ma
- Check direction: signs distinguish acceleration from deceleration
- Apply the work-energy theorem for speed problems, kinematics for time
- Always state friction/air resistance assumptions explicitly
- Verify results with energy conservation when possible

## Pitfalls / Common Mistakes

- Writing F = m g for horizontal acceleration problems
- Confusing mass (kg) with weight (N)
- Using the vertical height instead of the displacement along the slope
- Forgetting cos(theta) when force is not aligned with motion
- Reporting J for energy and W for power interchangeably
- Using PE = mgh without defining the reference level

## References

- [The Physics Classroom - Newton's Laws](https://www.physicsclassroom.com/class/newtlaws)
- [The Physics Classroom - Work, Energy, and Power](https://www.physicsclassroom.com/class/energy)
- [Khan Academy - Physics (AP Mechanics)](https://www.khanacademy.org/science/physics)
- [MIT OpenCourseWare - Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/)
- [NIST Guide to SI Units](https://physics.nist.gov/cuu/Units/)

## Notes

- g varies by location (9.78 at equator, 9.83 at poles); use 9.81 for problems
- Rotational motion has analogous equations (torque, angular momentum)
- Real machines always have losses; efficiency < 100%
