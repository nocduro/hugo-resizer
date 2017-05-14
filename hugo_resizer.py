"""
Resize images for a Hugo static site.
Run this script from the same directory that `hugo` command is run.

Currently only works if the folder structure is:
└───content
    └───post
        ├───arc-reactor
        │   └───images
        ├───beer-pong
        │   └───img
        └───flashlight
            └───images

Each generated size is placed in its own folder inside the images folder for that post:
└───content
    └───post
        ├───arc-reactor
        │   └───images
        │       ├───1080
        │       ├───300
        │       └───600
        ├───beer-pong
        │   └───img
        │       ├───1080
        │       ├───300
        │       └───600
        └───flashlight
            └───images
                ├───1080
                ├───300
                └───600

"""

import glob
import multiprocessing
import os
import shutil
import time

from PIL import Image

SIZES = ((1080, 800), (600, 600), (300, 300))
DIR_NAMES = ("images", "image", "img", "imgs")
EXTENSIONS = (".jpg", ".png", ".gif")

def delete_generated_images():
    """Deletes all the folders inside an images folder that match one of the sizes in SIZES
    """

    for root, dirs, files in os.walk("content"):
        if root.endswith(DIR_NAMES):
            print("deleting generated images from:", root)
            for size in SIZES:
                folder_dir = os.path.join(root, str(size[0]))
                if os.path.isdir(folder_dir):
                    shutil.rmtree(folder_dir)

def find_images():
    """Return list of all image paths below the contents directory that are in an images folder
    """

    print("finding image paths...")
    images = []
    for root, dirs, files in os.walk("content"):
        if root.endswith(DIR_NAMES):
            print("found images folder:", root)
            # make folder for each generated size if they dont exist
            for size in SIZES:
                os.makedirs(os.path.join(root, str(size[0])), exist_ok=True)
            for ext in EXTENSIONS:
                # get filenames for all images
                images.extend(glob.glob(root + "/*" + ext))
    '''
    # remove images from list that have already been processed
    size_ending = tuple(str(size[0]) for size in SIZES)
    for image in images:
        if os.path.splitext(image)[0].endswith(size_ending):
            images.remove(image)
    '''
    return images

def image_worker(image_path):
    # generate an image for each size
    for size in SIZES:
        directory, filename = os.path.split(image_path)
        im = Image.open(image_path)
        im.thumbnail(size)
        im.save(os.path.join(directory, str(size[0]), filename))

def multi_processing(num_processes):
    pool = multiprocessing.Pool(num_processes)
    images = find_images()

    # If tqdm (progress bar library) is installed, use it.
    # If not, do the work with no progress indicator
    try:
        import tqdm
        for _ in tqdm.tqdm(pool.imap_unordered(image_worker, images), total=len(images)):
            pass
    except ImportError:
        pool.map(image_worker, images)


if __name__ == "__main__":
    processes = 4

    delete_generated_images()

    start_time = time.time()
    #multi_processing(processes)
    end_time = time.time()
    m_time = time.time() - start_time

    print("time for {} processes: {}".format(processes, m_time))
