from scipy.io import loadmat

# Pickle allows saving and loading Python objects into a file
import pickle

from emgdecompy_wenlab.decomposition import *
from emgdecompy_wenlab.contrast import *
from emgdecompy_wenlab.viz import *
from emgdecompy_wenlab.preprocessing import *

import os

dir = r"C:\Users\Jerry Fu\Documents\nmi_dataset\GM under different intensities"
name = "1_10_GM.mat"
fname = os.path.join(dir, "1_10_GM.mat")
raw = loadmat(fname)['SIG']

output = decomposition(
    raw,
    discard=5,
    R=16,
    M=64,
    bandpass=True,
    lowcut=10,
    highcut=900,
    fs=2048,
    order=6,
    Tolx=10e-4,
    contrast_fun=skew,
    ortho_fun=gram_schmidt,
    max_iter_sep=10,
    l=31,
    sil_pnr=True,
    thresh=0.9,
    max_iter_ref=10,
    random_seed=None,
    verbose=False
)

decomp_sample = output 
decomp_sample_pkl = open('decomp_sample_pkl.obj', 'wb') 
pickle.dump(decomp_sample, decomp_sample_pkl)

with open('decomp_sample_pkl.obj', 'rb') as f: output = pickle.load(f)

visualize_decomp(output, raw)