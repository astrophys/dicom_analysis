# DICOM Analysis
#### Author : Ali Snedden
#### License: MIT 
## Purpose:
In this repo I am expanding on the work from my Ph.D. thesis in
[A new multi-scale structure finding algorithm to identify cosmological structure](https://doi.org/10.1016/j.jcp.2015.07.004)
and applying my image segmentation algorithm to CT lung cancer data.

This repo provides you a set of tools that allow you to segment, visualize and explore dicom
data sets (both series and single images). You can visualize both the raw input data and
the segmented data.

## Get the Data Set :
All the data is taken from the [Cancer Imaging Archive](https://www.cancerimagingarchive.net/),
an open source of imaging data.
1. First install the [NBI Data Retriever](https://wiki.cancerimagingarchive.net/display/NBIA/Downloading+TCIA+Images)
2. Download APOLLO-5-LUAD-manifest.tcia from [here](https://wiki.cancerimagingarchive.net/display/Public/APOLLO-5-LUAD)
3. Open the file with the NBI Dat Retriever. 
4. Download the data 
5. In the images below, I used the
   APOLLO-5-LUAD/AP-78LL/07-27-1977-NA-CT_CHEST_W-O_CON-49429/2.000000-CT CHEST-28012/
   data set.


## Installation and Dependencies :
1. Python 3.6+ is required for this code to work.
2. Install dependencies including 
    a) `pydicom` - tested with version `2.2.2`
    #) `numpy` - tested with version `1.18.2`
    #) `matplotlib` - tested with version `3.2.1`
3. Clone the directory, e.g.
```
git clone https://github.com/astrophys/dicom_analysis.git
```

## Usage:
### Segment the images
```
python3 src/dicom_analysis.py path/to/dicom/dir series output 1,2,3
```
where 
a) `series|single` : denotes whether a series of DICOM images are used
b) `output`        : denotes the stem to use on the output files (which are python `pkl` files)
c) `1,2,3`         : denotes the width of the several Gaussian kernels used to compute
                     the spatial derivatives on the data.



### Visualize
1. Visualize single dicom file
```
python3 src/visualize.py path/to/dicom/file.dcm single 2D
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/dicom-single-2D.png" width="400" />
where

* `single` : denotes a single DICOM image is used

* `2D`     : denotes the type of plotting to do


---
2. Visualize series of dicom files in 2D (using `matplotlib`) 
```
python3 src/visualize.py path/to/dicom/dir series 2D
```
<!-- ![alt text](https://github.com/astrophys/dicom_analysis/blob/main/images/cancer-slice-2D.png?raw=true)-->
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/cancer-slice-series-2D.png" width="400" />
where

* `series` : denotes a series of DICOM images are used

* `2D`     : denotes the type of plotting to do (using `matplotlib`)



---
3. Visualize raw 2D and segmented data 
```
python3 src/visualize.py path/to/dicom/dir series 2Dseg output_clust.pkl
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/cancer-slice-series-2Dseg.png" width="600" />

* `series` : denotes a series of DICOM images are used

* `2Dseg`  : flag to indicate plotting the 2D segmented data alongside the raw data.

* `output_clust.pkl`  : output file generated by `dicom_analysis.py`


---
4. Visualize raw DICOM data in 3D using VTK
```
python3 src/visualize.py path/to/dicom/dir series 3D 1100
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/dicom-series-3D.png" width="400" />

* `series` : denotes a series of DICOM images are used

* `3D`     : flag to indicate plotting the 2D segmented data alongside the raw data.

* `1100`   : threshold to plot above. Could use string 'otsu' for automatic thresholding


---
5. Segmented data (in pickle file generated by `dicom_analysis.py`)
```
python3 src/visualize.py output_clust.pkl single 3D 0.35
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/seg-series-3D.png" width="400" />

* `single` : denotes a single file being read 

* `3D`     : flag to indicate plotting the 2D segmented data alongside the raw data.

* `0.35`   : threshold to plot above. Could use string 'otsu' for automatic thresholding






#### References:
1. Clark K, et al. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. DOI: 10.1007/s10278-013-9622-7
2. Snedden A, et al. A new multi-scale structure finding algorithm to identify cosmological structure, Journal of Computational Physics, Volume 299, 2015, pp 92-97. DOI: 10.1016/j.jcp.2015.07.004

#### Other Useful Links :  
