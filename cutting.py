import rasterio
from rasterio.windows import Window
import numpy as np

def cut_by_pixwindow(img_path, window, save_path=None):
            '''
                 window in format [[upper_left_x, upper_left_y], [bottom_right_x, bottom_right_y]]
                 
                 if save path is None returns data_arry and cutted_image_profile,
                 otherwise save image on the provided path
                 
            '''

            with rasterio.open(img_path, 'r') as src:
            
                # The size in pixels of your desired window
                xsize, ysize = window[1][0]-window[0][0], window[1][1] - window[0][1]

                xoff, yoff = window[0]

                # Create a Window and calculate the transform from the source dataset    
                window = Window(xoff, yoff, xsize, ysize)
                transform = src.window_transform(window)

                # Create a new cropped raster to write to
                profile = src.profile
                profile.update({
                    'height': xsize,
                    'width': ysize,
                    'transform': transform,
                    'driver' : 'GTIff'})
                
                
                if save_path is None:
                    return src.read(window=window), profile
                else:
                    with rasterio.open(save_path, 'w', **profile) as dst:
                        dst.write(src.read(window=window))

        
def cut_by_img_geowindow(base_img, img_to_cut, save_path=None, border=0, v=False):   
    with rasterio.open(base_img, 'r') as src:
        
        # getting base img geo window
        h, w = src.shape
        corners_coords = [src.xy(0,0), src.xy(h,0), src.xy(0,w), src.xy(h,w)]


    with rasterio.open(img_to_cut, 'r') as cut_src:

        # finging pixels corresponding to geo window corners
        pixel_corner_coords = [cut_src.index(*coords)[::-1] for coords in corners_coords]
        pixel_corner_coords = np.array(pixel_corner_coords, dtype=np.int64)
        pixel_corner_coords = [pixel_corner_coords.min(axis=0) - border, pixel_corner_coords.max(axis=0)+ border]

        if v: print('Pixel coordinates of cutted window:', pixel_corner_coords)


    return cut_by_pixwindow(img_to_cut, pixel_corner_coords, save_path)                    

