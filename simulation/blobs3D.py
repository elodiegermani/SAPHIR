## BLOBS 3D

import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import label
import skimage.measure
from skimage.io import imsave, imread
import napari
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from scipy import ndimage

import roifile
from roifile import ImagejRoi
import pandas as pd
import shutil
from pathlib import Path


%gui qt

def blob(pos, center, size, intensity=10, xy_symmetric=True):
    """3D Gaussian
    pos: 3 arrays of x, y, and z values
    center : tuple of 3 floats for the gaussian center position
    size: tuple of 3 floats for the gaussian widths

    """
    x, y, z = pos
    # The idea is to make the computation in a 5D array
    # of shape ()
    
    x = x[np.newaxis, :, :, :] # 1, nx, ny, nz
    y = y[np.newaxis, :, :, :]
    z = z[np.newaxis, :, :, :]
    
    x0, y0, z0 = center.T
    x0 = x0[:, np.newaxis, np.newaxis, np.newaxis] # n_cells, 1, 1, 1
    y0 = y0[:, np.newaxis, np.newaxis, np.newaxis]
    z0 = z0[:, np.newaxis, np.newaxis, np.newaxis]
    sx, sy, sz = size.T[:, :, np.newaxis, np.newaxis, np.newaxis]
    
    intensity = intensity[:, np.newaxis, np.newaxis, np.newaxis]# n_cells, 1, 1, 1
    
    if xy_symmetric:
        sy = sx
        
    
    #print(((x - x0)/sx).shape)
    # broadcasting
    sig = (
        np.exp(-(((x - x0) / sx) ** 2))
        * np.exp(-(((y - y0) / sy) ** 2))
        * np.exp(-(((z - z0) / sz) ** 2))
        * intensity
    ) # n_cells, n_x, n_y, n_z
    #print(sig.shape)
    sig = sig.sum(axis=0) # n_x, n_y, n_z
    return sig


def generate_blobs(num_cells, shape, dtype, seed=0):
    """ Creates an image of shape `shape` with num_cells blobs in it
    """
    
    rng = np.random.default_rng(seed)
    cell_size = (5, 5, 1)
    cell_size_std = (1, 1, 0.01)
    max_int = 100
    max_int_std = 30

    centers = rng.integers(low=np.zeros(3), high=shape, size=(num_cells, 3))
    
    sizes = rng.normal(loc=cell_size, scale=cell_size_std, size=(num_cells, 3))

    intensities0 = rng.normal(loc=max_int, scale=max_int_std, size=num_cells)
    intensities1 = rng.normal(loc=max_int, scale=max_int_std, size=num_cells)

    
    stack0 = np.zeros(shape)
    stack1 = np.zeros(shape)
    
    
    pos = np.mgrid[ :shape[0], :shape[1], :shape[2]] # xyz
    
    stack0 += blob(pos, centers, sizes, intensities0)
    stack1 += blob(pos, centers, sizes, intensities1)
    #print(f"z = {z} / {shape[-1]}")
    
    stack0 = (stack0 / stack0.max()) * dtype(-1) # np.uint8 -> 255
    stack1 = (stack1 / stack1.max()) * dtype(-1)
    
    stack0 = stack0.clip(0).swapaxes(0, 2).astype(dtype)  # zyx
    stack1 = stack1.clip(0).swapaxes(0, 2).astype(dtype)  # zyx 
    
    return stack0, stack1

#watershed segmentation 
def segmentation(mask):
    distance = ndimage.distance_transform_edt(mask)
    local_maxi = peak_local_max(distance, indices=False,labels = mask, exclude_border=False)
    markers = ndimage.label(local_maxi, structure=np.ones((3,3,3)))[0]
    labels = watershed(-distance, markers, mask=mask)
    return labels

def make_3canals(num_cells, shape, dtype, seed=0):
    """ Creates a 3 canals stack with the blobs, a transformed value
    (as a way to add diversity) and the labels from a simple thresholding
    """
    canal0, canal1 = generate_blobs(num_cells, shape, dtype, seed=seed) 
    # apply threshold
    thresh = threshold_otsu(canal0)
    bw = canal0 > thresh

    #bw = bw[:, :, :].astype(bool)
    # canal2 = label(bw).astype(dtype) # max 255 cells !!
    canal2 = segmentation(bw)
    return np.stack([canal0, canal1, canal2]) 


def create_tiff(fname, num_cells, shape, dtype=np.uint8):
    """Creates an image with make_3canals and saves it to fname
    num_cells: the number of blobs in the image
    shape : tuple of ints, the image shape (as x, y, z)
    dtype : the image dtype (default uint8)
    """
    image = make_3canals(num_cells, shape, dtype)
    imsave(fname, image, plugin="tifffile", metadata={'axes': 'CZYX'})
    return image

def main():
    shape = (1024, 1024, 10)
    num_cells = 1000
    image = create_tiff("test.tif", num_cells, shape)
    return image
  
  #3D 

num_cells =10
shape = (104, 104, 2)
stack = make_3canals(num_cells, shape, np.uint8)
print(stack.shape) # C Z Y X


## view on napari
napari.view_image(stack, channel_axis=0)

## save 3D image as .tif
#imsave("test.tif", stack, plugin="tifffile", metadata={'axes': 'CZYX'})

# segmentation 
labels = segmentation(stack[2])
#print(labels.shape)

region0 = skimage.measure.regionprops_table(labels, intensity_image=stack[0], properties=['label','mean_intensity'])
region1 = skimage.measure.regionprops_table(labels, intensity_image=stack[1], properties=['label','mean_intensity'])
region1['mean_intensity1'] =  region1.pop('mean_intensity')
region0.update(region1) 
df = pd.DataFrame(region0) #, 'Circularity': [], 'size': []})
print(df)

## generate .cvs file with intensities
#result = df.to_csv("result1.csv",float_format='%.4f', header = ["ID", "Int0", "Int1"], index = False, sep = "\t")       



def get_roi(contour, level) :
    return ImagejRoi.frompoints(contour[level])

def generate_zip(racine_zip : str) : 
    directory = racine
    path = Path(directory)
    pathROIset = path/"ROIset1"
    pathROIset.mkdir(parents=True, exist_ok=False)

    for i, level in enumerate(contours) : 
        roi = get_roi(contours,i)
        roi.tofile(f'roi_{i:04d}.roi')
        filepath = str(path/f'roi_{i:04d}.roi')
        shutil.move(filepath,pathROIset)
      
    shutil.make_archive('ROIset1', 'zip', 'ROIset1' )    

## generate ROIset.zip at racine
racine = 'C:\\Users\\jouan\\Documents\\cours\\M1\\stage\\python'
#generate_zip(racine)


def chunked(shape, n_cells, chunk_size=100, dtype=np.uint16):
    cell_lots =  n_cells // chunk_size

    stack = np.zeros(
        (3, shape[-1], shape[0], shape[1]), #CZXY
        dtype=np.uint8
    ) 
    max_lbl = 0
    # parallelize ?
    for i in range(cell_lots):
        print(f"\t## cell lot {i} / {cell_lots}")
        sstack = make_3canals(chunk_size, shape, dtype, seed=i)
        sstack[2, :, :][sstack[-1]!=0] += max_lbl # boolean indexing
        sstack[:2, ...] = sstack[:2, ...] // cell_lots
        max_lbl =a
        
        
        stack += sstack

    stack[-1, ...] -= stack[-1, ...].min()
    return stack
    
shape = (1024, 1024, 1) # XYZ
n_cells = 100
stack = chunked(shape, n_cells)

