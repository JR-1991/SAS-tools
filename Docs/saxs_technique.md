## 1D SAXS Technique Layer Concept

## Sample role blueprints

### In here go the different sample types like "blank, solvent, normalisation, etc.

- Sample (Category)
  - Sample name (Parameter)
  - Descriptive name (Parameter)
  - Sample ID (Parameter)
  - LLC/hybrid material/silica material
- Date (Category)
  - Year (Parameter)
  - Month (Parameter)
  - Day (Parameter)


## Experimental data role blueprints

### In here goes the type of spectra that can be collected.

- SAXS Diffractogram (Series)
  - Scattering vector q (Quantity)
  - intensity (Quantity)


## Method blueprint

### In here goes the description of the experimental method applied with all the different parameters of the spectrometer and program.

- Device setup (Category)
  - Diffractometer
      - model
      - manufacturer
  - x-ray source
    - source material
    - generator
    - acceleration voltage
    - current
  - focussing optics
  - detector + distance

- Sample holder (Category)
  - temperature control unit
  - sample holder/borehole
  - rotation
  - Capillary
    - diameter (Quantity)
    - wall thickness (Quantity)
    - glass type

- Measurement program
  - exposure time
  - captures per something
  - temperature/ temperature control
  - single measurement/measurement series

- Measurement values
  - scattering vector q
  - intensity
  - standard error

- Data analysis
  - plot
  - Lorentz-fit

- Evaluation
  - desmearing (y/n)
  - background correction
  - calibration
  - lattice planes d
  - peak ratios
  - LLC phase
  - lattice parameter a


## Result blueprint

### Everything that is measured or can be measured goes in here.

- Diffractogram
  - scattering vector q
  - intensity
- Temperature