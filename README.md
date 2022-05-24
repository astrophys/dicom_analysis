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
### Visualize
1. Visualize single dicom file
```
python3 src/visualize.py path/to/dicom/file.dcm single 2D
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/dicom-single-2D.png" width="400" />



2. Visualize series of dicom files in 2D (using `matplotlib`) 
```
python3 src/visualize.py path/to/dicom/dir series 2D
```
<!-- ![alt text](https://github.com/astrophys/dicom_analysis/blob/main/images/cancer-slice-2D.png?raw=true)-->
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/cancer-slice-series-2D.png" width="400" />



3. Visualize raw 2D and segmented data (using pickle file generated by `dicom_analysis.py`)
```
python3 src/visualize.py data/series series 2Dseg output_clust.pkl
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/cancer-slice-series-2Dseg.png" width="600" />



4. Visualize raw DICOM data in 3D using VTK
```
python3 src/visualize.py data/series series 3D 1100
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/dicom-series-3D.png" width="400" />


5. Segmented data (in pickle file generated by `dicom_analysis.py`)
```
python3 src/visualize.py output_clust.pkl single 3D 0.35
```
<img src="https://github.com/astrophys/dicom_analysis/blob/main/images/seg-series-3D.png" width="400" />





#### References:
1. 

#### Other Useful Links :  
