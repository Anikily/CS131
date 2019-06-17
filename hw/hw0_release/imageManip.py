import math

import numpy as np
from PIL import Image
from skimage import color, io


def load(image_path):
    """Loads an image from a file path.

    HINT: Look up `skimage.io.imread()` function.

    Args:
        image_path: file path to the image.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    out = None

    out = Image.open(image_path)
    out = np.array(out)

    # Let's convert the image to be between the correct range.
    print(f'before div,the mean of img is {out.mean()}')
    out = out.astype(np.float64) / 255
    print(f'after div,the mean of img is {out.mean()}')
    return out


def dim_image(image):
    """Change the value of every pixel by following

                        x_n = 0.5*x_p^2

    where x_n is the new value and x_p is the original value.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None

    out = (image**2)*0.5

    return out


def convert_to_grey_scale(image):
    """Change image to gray scale.

    HINT: Look at `skimage.color` library to see if there is a function
    there you can use.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width).
    """
    out = None

    out = color.rgb2grey(image)

    return out


def rgb_exclusion(image, channel):
    """Return image **excluding** the rgb channel specified

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "R", "G" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None
    rgb = {'R':0,'G':1,'B':2}
    out = image
    #astype for deepcopy
    out = out.astype(np.float64)
    out[:,:,rgb[channel]] = 0

    return out


def lab_decomposition(image, channel):
    """Decomposes the image into LAB and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "L", "A" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    lab = color.rgb2lab(image)
    out = None
    hsv_ = {'L':0,'A':1,'B':2}
    mat = np.array([[1,0,0],[0,1,0],[0,0,1]]).astype(np.float)
    
    out = lab*mat[hsv_[channel]]

    return out


def hsv_decomposition(image, channel='H'):
    """Decomposes the image into HSV and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "H", "S" or "V".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    hsv = color.rgb2hsv(image)
    out = None
    hsv_ = {'H':0,'S':1,'V':2}
    mat = np.array([[1,0,0],[0,1,0],[0,0,1]]).astype(np.float)
    
    out = hsv*mat[hsv_[channel]]

    return out


def mix_images(image1, image2, channel1, channel2):
    """Combines image1 and image2 by taking the left half of image1
    and the right half of image2. The final combination also excludes
    channel1 from image1 and channel2 from image2 for each image.

    HINTS: Use `rgb_exclusion()` you implemented earlier as a helper
    function. Also look up `np.concatenate()` to help you combine images.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).
        image2: numpy array of shape(image_height, image_width, 3).
        channel1: str specifying channel used for image1.
        channel2: str specifying channel used for image2.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None
    img1 = rgb_exclusion(image1,'R')
    img2 = rgb_exclusion(image2,'G')
    h,w,c = img1.shape
    out = np.zeros_like(img1)
    out[:,:w//2,:] = img1[:,:w//2,:]
    out[:,w//2:,:] = img2[:,w//2:,:]
    return out


def mix_quadrants(image):
    """THIS IS AN EXTRA CREDIT FUNCTION.

    This function takes an image, and performs a different operation
    to each of the 4 quadrants of the image. Then it combines the 4
    quadrants back together.

    Here are the 4 operations you should perform on the 4 quadrants:
        Top left quadrant: Remove the 'R' channel using `rgb_exclusion()`.
        Top right quadrant: Dim the quadrant using `dim_image()`.
        Bottom left quadrant: Brighthen the quadrant using the function:
            x_n = x_p^0.5
        Bottom right quadrant: Remove the 'R' channel using `rgb_exclusion()`.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    out = None

    out = np.zeros_like(image)
    h,w,_ = out.shape
    h,w = h//2,w//2
    out[0:h,0:w,:] = rgb_exclusion(image,'R')[0:h,0:w,:]
    out[0:h,w:,:] = dim_image(image)[0:h,w:,:]
    out[h:,0:w,:] = (image**(0.5))[h:,0:w,:]
    out[h:,w:,:] = rgb_exclusion(image,'R')[h:,w:,:] 
    
    

    return out
