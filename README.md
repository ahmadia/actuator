# Sample actuator response code

The Python script, `actuator.py`, when properly calibrated,
detects micro-pressure readings by processing image frames
from a camera aimed at a manometer.  The time is parsed from
image EXIF data and stored as well.

Cropped images and a reference frame are also saved for experimental
reproducibility.

[Some example data](https://dl.dropbox.com/u/65439/micro-filter/input.tar.gz)

## Example Data
Here is a sample reference frame:

![sample_reference](https://dl.dropbox.com/u/65439/micro-filter/reference_DSC_1348.JPG)

The cropped frame:

![sample_crop](https://dl.dropbox.com/u/65439/micro-filter/cropped_DSC_1348.JPG)

The script detects this as a measurement of 1.8 cm

## Example Plot
Here's an example plot from a complete run of pressure vs. time.

![sample_plot](https://dl.dropbox.com/u/65439/micro-filter/pressure.png)
