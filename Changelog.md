# Changelog

## 2026-09-22 - V[1.10]
### New Features: 
* Diodes can be created with random specifications using Create.Diode("random") or Create.Diode("rand").
* The voltage and electric field sweeps of separate Diode instances can be visually compared on the same graph via CMP_VoltageSweepAtEquilibrium() or CMP_ElectricFieldSweepAtEquilibrium()
* Diodes can now be named on initialisation

## 2026-09-25 - v[1.2]
### New Features:
* Implemented the Tridiagonal Matrix Algorithm to drastically decrease time spent on an iteration by 98.53%
