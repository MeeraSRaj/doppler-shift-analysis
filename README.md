# Real-Time Doppler Shift Analysis of LEO Satellite Signals Using SDR

A Python and Software Defined Radio (SDR) based project for measuring and analyzing the Doppler shift of Low Earth Orbit (LEO) satellite signals.

The project was tested using the **Meteor-M2 weather satellite** during a pass on **September 24, 2025**.

## Overview

As a satellite moves toward and away from a ground station, its received signal frequency changes due to the **Doppler effect**.

This project captures those frequency changes using an **ADALM-PLUTO SDR** and processes the measurements to:

* Measure Doppler shift in real time
* Remove noisy/outlier measurements
* Smooth the measured data
* Fit a theoretical Doppler curve
* Estimate satellite velocity
* Visualize the satellite's Doppler profile

## Hardware

* ADALM-PLUTO SDR
* 15-element Yagi antenna
* Low-noise amplifier
* 2 MHz sampling rate
* 1.622 GHz center frequency

## Software

* Python
* NumPy
* SciPy
* Matplotlib
* Pandas

## Signal Processing

The analysis pipeline uses:

```text
Raw Measurements
       ↓
Outlier Removal (IQR)
       ↓
Savitzky-Golay Filtering
       ↓
Doppler Curve Fitting
       ↓
Velocity Estimation
       ↓
Visualization
```

A hyperbolic tangent model is used to approximate the Doppler curve:

$$
f(t) = A\tanh(B(t-C))
$$

where \(C\) represents the estimated **Time of Closest Approach (TCA)**.

## Results

| Parameter                  |     Result |
| -------------------------- | ---------: |
| Measurements               |       1441 |
| Observation Time           |      720 s |
| Maximum Doppler            |   +7645 Hz |
| Minimum Doppler            |   -7672 Hz |
| Average SNR                |    52.1 dB |
| Curve Fit \(R^2\)          |     0.9987 |
| Estimated Orbital Velocity | 7431.4 m/s |

The measured Doppler curve showed the expected **S-shaped profile** of a LEO satellite pass.


## Future Work

* Automatic satellite tracking
* Real-time Doppler visualization
* Improved orbit determination
* GPS-disciplined frequency reference
* Multi-station Doppler measurements

## License

This project is intended for educational and research purposes.
