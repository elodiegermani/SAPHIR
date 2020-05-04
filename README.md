# Image Explorer

### Introduction 

### Requirements 
#### Images 
The image file to analyse must be in TIFF format. It can be up to 4 dimensions with third and fourth dimensions representing channel and depth (z coordinate). 

#### Data File 
File containing for each ROI its ID, its intensity on each channel of the image and values for other variables like area, roundness... 
You can choose the separator and the type of decimals in your file with the radioButtons. 
If the first line of the file represent the names of the columns, check the "Header" button. 
The table must have column headers with unique column names. Columns names are requisites : 
- the column containing the IDs must be named "ID"
- the column containing the areas must be names "Cell area"
- the columns containing the cell type must be named "Cell type"
- if there is a 4th dimension with depth, the file must contain a column "Slice" which contain for each ROI the Slice in which it is. 

#### File ROIs 
Zip file containing the ROIs of the image defined with ImageJ. 

### Using the application 
To launch the app, you have to open the app.R file in RStudio and click on the "Run app" button on the right top corner. 

#### First step : upload the image you want to analyse 
Use the first item of the menu "Choose your image" and click on the "Browse" button. Select the image you want to analyse in your documents. 

#### Second step : select ROIs to remove
Under the browse box, you can plot variables of the results or the intensity file and select ROIs with extreme values to remove them from the datas to analyse. For choosing the variables to plot, use the select widget : 
* if you select ONE variable, an histogram of this variable will be plotted with a bin width of 10. 
* if you select TWO variables, a scatter plot will be displayed with the first selected variable in X and the second in Y. 

Make a selection on the plot and click on the "Remove" button. 
* for the histogram, the ROIs having the values selected for the plotted variable will be selected 
* for the scatterplot, the ROIs corresponding to the points will be selected
The selection will be removed from the intensity and result files and from the Roi set. 

#### Third step 
##### Part 1 : Plot to Image
Use the second item of the menu : "Plot to Image". <br>
Zones of the plot : 
* A plot representing for ROIs their intensities on different channels is displayed. The variables plotted in X and Y can be modified. 
* The plot can be cut in 4 zones : Up Left (UL), Up Right (UR), Down Left (LL) and Down Right (DR) depending on movable horizontal and a vertical lines. At the beginning, all the points have the same color. The colors of the points in each zone can be modified with the button "Reload colors".
* The datas (result file) of the ROIs of each zone can be downloaded in a zip file containing 4 csv files, one for each zone, with the button "Download Groups subtable". 


Selections on the plot :
* Points of the plot can be selected (by clicking or brushing) and datas of the ROIs selected are printed in a table below. 
* These datas can be downloaded in a csv file with the button "Download selected ROIs subtable". 

Image : <br>
The image is displayed on the left, channel and slice to display can be modified with the sliders. 
ROIs selected on the plot are displayed on the image and the color of the mask correspond to cell type. 

Cropped ROIs : <br>
The ROIs selected on the plot can be displayed with the button "Load ROIs". Each time a new selection is made, you need to reload the viewer with the "Load ROIs" button. 
The ROIs are displayed in the viewer in order of ROIs IDs. 

##### Part 2 : Image to plot 
Use the third item of the menu : "Image to plot". <br> 
The image is displayed on the left with the ROIs you retained. You can choose channel and slice to display with sliders and the color with which the ROIs are displayed. <br> 

You can select ROIs on the image (one click or selection) and check the datas on the ROIs selected. These datas can be plotted with the plot on the left. 