from concurrent.futures import ThreadPoolExecutor, as_completed
from glob import glob
from PIL import Image
import numpy as np
import os
import time
import tqdm

path = 'Datasets/Datasets'
ims = (64, 64)
category = ['shi', 'tsu', 'n', 'so', 'no', 'me']

image_paths = list(glob(os.path.join(path, '*', '*.png')))
n_images = len(image_paths)

print("Found images:", len(image_paths))

data = np.empty((n_images, ims[1], ims[0]), dtype=np.uint8)
labels = np.empty(n_images, dtype=np.int32)

def load_image(args):
    idx, im, ims, c = args
    img = np.array(Image.open(im).convert("L").resize((ims[0], ims[1])))
    label = c.index(os.path.basename(os.path.dirname(im)))
    return idx, img, label

start = time.time()
with ThreadPoolExecutor(max_workers=14) as executor:
    futures = {executor.submit(load_image, (idx, im, ims, category)): idx for idx, im in enumerate(image_paths)}
    for future in tqdm.tqdm(as_completed(futures), total=n_images):
        idx, img, label = future.result()
        data[idx] = img
        labels[idx] = label
end = time.time()

print(f"Loaded {n_images} images in {end - start:.2f} seconds.")