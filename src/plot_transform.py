#!/usr/bin/env python
# https://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script

"""
plot_feature.py: visualize model features from random samples to display ROI (regions of interest) the moodel focuses on
"""

__author__ = "Hua Zhao"

from src import *
from matplotlib import pyplot as plt
from src.transform import *


def plot_example_transforms(example_num=5, save_path='./diagnosis/', size=5, use_seg=False):
    """
    visualize random original and transformed training or testing images
    """
    _processor = ImgPreprocessor(CLAHE=params['etl']['use_CLAHE'], 
                            crop_top=params['etl']['crop_top'], 
                            size=params['etl']['image_size'], 
                            use_seg=use_seg,
                            clipLimit=params['etl']['CLAHE_clip_limit'],
                            tileGridSize=(params['etl']['CLAHE_tile_size'], params['etl']['CLAHE_tile_size'])
    )

    if not os.path.isdir(os.path.join(save_path, 'transform')):
        os.makedirs(os.path.join(save_path, 'transform'))

    meta = pickle.load(open(os.path.join(CACHE_PATH, 'meta', 'meta'), 'rb'))
    fns = np.random.choice(meta.img, example_num)
    
    fig, axs = plt.subplots(len(fns), 2, constrained_layout=True)
    fig.set_size_inches(size*2, size*len(fns))

    for i, fn in enumerate(fns):
        if fn[-3:] == 'dcm':  # .dcm
            ds = dicom.dcmread(fn)
            img = ds.pixel_array
            img = cv2.merge((img,img,img))  # CXR images are exactly or almost gray scale (meaning 3 depths have very similar or same values); checked
        else:  # .png., .jpeg, .jpg
            img = cv2.imread(fn)

        img_pre = cv2.resize(img, (params['etl']['image_size'], params['etl']['image_size']))
        img_cur = _processor(img)

        axs[i, 0].imshow(img_pre, cmap='gray')
        axs[i, 0].set_title(f"example {i+1} - original")
        
        axs[i, 1].imshow(img_cur, cmap='gray')
        axs[i, 1].set_title(f"example {i+1} - transformed")

    title = f'images: original vs transformed'
    fig.suptitle(title, fontsize=16)
    plt.show()
    fig.savefig(os.path.join(save_path, 'transform', f'transform example.png'))
    return