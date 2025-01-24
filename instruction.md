# EMGdecomPy Workflow

This notebook allows for simple visualisation of the decomposition results obtained from the `EMGDecomPy` package.

## Imports - dependencies

Please run the cells below to add all the dependencies to run this notebook.   
First, import the Python packages for loading in and saving data:

```python
# loadmat is used to load MATLAB data
from scipy.io import loadmat

# Pickle allows saving and loading Python objects into a file
import pickle
import os

# Import the EMGDecomPy package
import EMGdecomPy as emg
``` 

## Imports - EMGDecomPy

Now, import the `EMGDecomPy` package scripts for decomposing and visualizing the electromyography data:

```python
from emgdecompy_wenlab.decomposition import *
from emgdecompy_wenlab.contrast import *
from emgdecompy_wenlab.viz import *
from emgdecompy_wenlab.preprocessing import *
from emgdecompy_wenlab.file_utils import *
```

## Load the raw EMG data

Please specify the filepath where the raw data is located, and use it to define the  `raw_data` variable.

This raw data will be processed via an algorithm based on the the process proposed by `Negro et al. (2016)`.

In order for the decomposition to accurately process the data, it needs to be in the correct format. The `decomposition` function and the `visualize_decomp` functions expect the `raw` argument to be a numpy array of arrays, where each inner element array is a time series of electromyography signal observations per channel.

For instance, during this project, we used data in the MATLAB `.mat` format. A simplified example of the raw data dictionary can be seen below.

Below, we load the data via the `loadmat` function, which we index into its signal series with the `SIG` key.

```python
dir = r"C:\Users\jerry_pc\Documents\GitHub\EMGdecomPy\data\raw"
name = "GL_10.mat"
fname = os.path.join(dir, name)
data = loadmat(fname)
raw = data["SIG"]
discard_channel = data["discardChannelsVec"]
```

Note the aforementioned `SIG` key-value pair, containing the array of arrays. For the purposes of decomposition, `SIG` is the only key needed within the dictionary. However, the rest of the information stored within the `.mat` file can be found below:

```raW

{'__header__': b'MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Thu Nov 19 19:29:51 2020',
 '__version__': '1.0',
 '__globals__': [],
 'MUPulses': array([[array([[ 92900,  93164,  93402,  93617,  93774,  94013,  94203,  94402,
                  94625,  94812,  94990,  95223,  95418,  95604,  95815,  96040,
                  96268,  96476,  96761,  97012,  97253,  97463,  97689,  97941,
                  98146,  98345,  98622,  98849,  99191,  99504,  99759,  99937,
                 100097, 100292, 100464, 100629, 100825, 100982, 101162, 101320,
                 101488, 101660, 101842, 102016, 102214, 102373, 102479, 102540,
                 102845, 103045, 103249, 103498, 103715, 103909, 104139, 104382,
                 104603, 104804, 105002, 105192, 105388, 105582, 105771, 105977,
                 106200, 106367, 106559, 106781, 107007, 107183, 107369, 107583,
                 107794, 107989, 108303, 108511, 108729, 108984, 109196, 109418,
                 109653, 109857, 110041, 110202, 110373, 110651, 110875, 111075,
                 111187, 111270, 111469, 111668, 111873, 112079, 112271, 112498,
                 112702, 112890, 113082, 113296, 113458, 113645, 113852, 114036,
                 114210, 114391, 114604, 114799, 114996, 115212, 115436, 115665,
                 115895, 116080, 116290, 116512, 116721, 116919, 117015, 117119,
                 117316, 117528, 117734, 117950, 118146, 118328, 118516, 118682,
                 118870, 119061, 119251, 119446, 119640, 119827, 120013, 120206,
                 120426, 120642, 120780, 120973, 121177, 121358, 121532, 121748,
                 121952, 122169, 122359]], dtype=int32)                         ,
         array([[ 92911,  93167,  93430,  93645,  93877,  94096,  94371,  94625,
                  94802,  94999,  95234,  95467,  95725,  95945,  96264,  96524,
                  97023,  97341,  97580,  97953,  98211,  98755,  99785,  99988,
                 100179, 100440, 100597, 100835, 101014, 101241, 101406, 101616,
                 101847, 102047, 102237, 102421, 102625, 102946, 103168, 103419,
                 103666, 103898, 104161, 104436, 104661, 104883, 105078, 105292,
                 105533, 105751, 106005, 106277, 106481, 106717, 107066, 107303,
                 107546, 107803, 108064, 108426, 108715, 109033, 109323, 109687,
                 109956, 110134, 110358, 110698, 110962, 111235, 111457, 111683,
                 111934, 112188, 112490, 112740, 112980, 113195, 113389, 113591,
                 113858, 114055, 114275, 114492, 114749, 114993, 115326, 115603,
                 115864, 116100, 116321, 116562, 116825, 117039, 117285, 117583,
                 117850, 118109, 118337, 118533, 118738, 118965, 119175, 119394,
                 119625, 119851, 120074, 120299, 120561, 120736, 120901, 121121,
                 121362, 121576, 121840, 122085, 122348]], dtype=int32) ,
               dtype=int32)                                                       ]],
       dtype=object),
 'MUIDs': array([[array(['A1'], dtype='<U2'), array(['A2'], dtype='<U2'),]], dtype=object),
 'Cost': array([[array([[0.17085427]]), array([[0.17596919]]),
         array([[0.26433915]]), array([[0.24786325]]),
         array([[0.30697674]])]], dtype=object),
 'PNR': array([[33.8, 39.8, 32. , 38.5, 27.1]]),
 'SIG': array([[array([], shape=(0, 0), dtype=uint8),
         array([[46.79361979, 13.22428385, -7.12076823, ..., 26.44856771,
                 50.86263021, 36.62109375]])                             ,
         array([[76.29394531, 39.67285156, 29.50032552, ..., 34.58658854,
                 47.8108724 , 57.98339844]])                             ,
         array([[74.2594401 ,  4.06901042, -5.08626302, ..., 21.36230469,
                 30.51757812, 36.62109375]])                             ,
         array([[62.05240885, 28.48307292, 17.29329427, ...,  3.05175781,
                 22.37955729, -5.08626302]])                             ],
        [array([[88.50097656, 29.50032552, 12.20703125, ..., 17.29329427,
                 48.828125  , 77.31119792]])                             ,
         array([[108.84602865,  71.20768229,  25.4313151 , ...,  20.34505208,
                  62.05240885,  67.13867188]])                               ,
         array([[81.38020833, 35.60384115, 10.17252604, ..., 27.46582031,
                 66.12141927, 89.51822917]])                             ,
         array([[74.2594401 , 10.17252604,  7.12076823, ...,  2.03450521,
                 62.05240885, 71.20768229]])                             ,
         array([[70.19042969, 27.46582031, 12.20703125, ..., 11.18977865,
                 47.8108724 , 99.69075521]])                             ],
        [array([[84.43196615, 65.10416667, 22.37955729, ..., 32.55208333,
                 67.13867188, 77.31119792]])                             ,
         array([[85.44921875, 40.69010417, 14.24153646, ..., 39.67285156,
                 76.29394531, 72.2249349 ]])                             ,
         array([[75.27669271, 47.8108724 , 26.44856771, ..., 19.32779948,
                 31.53483073, 75.27669271]])                             ,
         array([[68.15592448, 40.69010417,  1.0172526 , ..., 15.25878906,
                 54.93164062, 75.27669271]])                             ,
         array([[78.32845052, 18.31054688, -5.08626302, ..., 15.25878906,
                 63.06966146, 52.89713542]])                             ],
        [array([[66.12141927, 16.27604167,  1.0172526 , ..., 29.50032552,
                 52.89713542, 78.32845052]])                             ,
         array([[ 82.39746094,   7.12076823, -18.31054688, ...,  13.22428385,
                  70.19042969,  86.46647135]])                               ,
         array([[68.15592448, 29.50032552,  6.10351562, ..., 11.18977865,
                 51.87988281, 79.34570312]])                             ,
         array([[80.36295573, 37.63834635, 16.27604167, ..., 52.89713542,
                 74.2594401 , 77.31119792]])                             ,
         array([[64.08691406, 27.46582031, -7.12076823, ..., 24.4140625 ,
                 52.89713542, 77.31119792]])                             ]],
       dtype=object),
 'IPTs': array([[0., 0., 0., ..., 0., 0., 0.],
        [0., 0., 0., ..., 0., 0., 0.],
        [0., 0., 0., ..., 0., 0., 0.],
        [0., 0., 0., ..., 0., 0., 0.],
        [0., 0., 0., ..., 0., 0., 0.]]),
 'fsamp': array([[2048]], dtype=uint16),
 'startSIGInt': array([[45]], dtype=uint8),
 'stopSIGInt': array([[60]], dtype=uint8),
 'ref_signal': array([[66833496.09375, 67749023.4375 , 67138671.875  , ...,
         54626464.84375, 50659179.6875 , 52490234.375  ]]),
 'origRecMode': array(['MONO'], dtype='<U4'),
 'SIGFilePath': array(['C:\\Users\\hug_f\\Documents\\Data\\InterDrive\\S10\\Raw\\'],
       dtype='<U49'),
 'SIGFileName': array(['vaMiKT_10.otb+'], dtype='<U14'),
 'DecompRuns': array([[50]], dtype=uint8),
 'IED': array([[8]], dtype=uint8),
 'discardChannelsVec': array([[0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]], dtype=uint8),
 'description': array(['C:\\Users\\hug_f\\Documents\\Data\\InterDrive\\S10\\Raw\\'],
       dtype='<U49'),
 'SIGlength': array([[105.21142578]]),
 'ProcTime': array([[  7.8472085,  14.0359775,  20.3020407,  26.6780681,  33.1434723,
          39.5730774,  46.0549393,  52.4345215,  58.8978001,  65.4029372,
          71.8402833,  78.3977499,  84.9143059,  91.414722 ,  97.8160689,
         104.1980256, 110.6378523, 117.0923444, 123.4877615, 129.9538468,
         299.2515221, 305.935486 , 312.5607617, 319.0872198, 325.7498793]]),
 'DecompStat': array([[4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5]], dtype=uint8)}
```

## Run decomposition

Run the decomposition on raw data to retrieve a dictionary containing the results of the blind source separation algorithm. Further documentation for each function can be found [here](https://emgdecompy.readthedocs.io/en/stable/autoapi/emgdecompy/index.html).

__There is a number of parameters you may choose to customize:__

| Parameter    | Data Type                    | Explanation                                                                                  |
|--------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| x            | numpy.ndarray                | Raw EMG signal. This is expected inside the 'SIG' key within the `.mat` file loaded above.  
| discard      | slice, int, or array of ints | Indices of channels to discard. Useful if you are looking to only analyze some channels, or expect some channels to contain significant noise.                               |
| R            | int                          | How far to extend x during the extension step of the algorithm.                                                                                                            |
| M            | int                          | Number of iterations to run the decomposition for.                                                                                                                             |
| bandpass       | bool                         | Whether to band-pass filter the raw EMG signal or not.                                                                                                                     |
| lowcut       | float                        | Lower range of band-pass filter.                                                                                                                                           |
| highcut      | float                        | Upper range of band-pass filter.                                                                                                                                           |
| fs           | float                        | Sampling frequency in Hz.                                                                                                                                                  |
| order        | int                          | Order of band-pass filter.                                                                                                                                                 |                                                                                                                          |
| Tolx         | float                        | Tolerance for element-wise comparison in separation.                                                                                                                       |
| contrast_fun | function                     | Contrast function to use. `skew`, `og_cosh` or `exp_sq`                                                                                                                          |
| ortho_fun    | function                     | Orthogonalization function to use. `gram_schmidt` or `deflate`                                                                                                                 |
| max_iter_sep | int > 0                      | Maximum iterations for fixed point algorithm.                                                                                                                              |
| l            | int                          | Required minimal horizontal distance between peaks in peak-finding algorithm. Default value of 31 samples is approximately equivalent to 15 ms at a 2048 Hz sampling rate. |
| sil_pnr      | bool                         | Whether to use SIL or PNR as the acceptance criterion. Default value of True uses SIL.                                                                                         |
| thresh       | float                        | SIL/PNR threshold for accepting a separation vector.                                                                                                                       |
| max_iter_ref | int > 0                      | Maximum iterations for refinement.                                                                                                                                         |
| random_seed  | int                          | Used to initialize the pseudo-random processes in the function.                                                                                                            |
| verbose      | bool                         | If true, decomposition information is printed.                                                                                                                             |
```python
remove = flatten_signal(discard_channel)
remove = np.delete(remove, 0)
indices = np.where(remove==1)[0]
print(f"Discarding channels: {indices}")

output = decomposition(
    raw,
    discard=indices[0],
    discard_indices=indices,
    R=16,
    M=64,
    bandpass=True,
    lowcut=10,
    highcut=900,
    fs=2048,
    order=6,
    Tolx=10e-4,
    contrast_fun=skew,
    ortho_fun=deflate,
    max_iter_sep=10,
    l=31,
    sil_pnr=True,
    thresh=0.9,
    max_iter_ref=10,
    random_seed=None,
    verbose=True
)
print(f"Complete")
```
The output of decomposition is a dictionary containing the following keys:

__'B'__: Matrix whose columns contain the accepted separation vectors.

__'MUPulses'__: Firing indices for each motor unit. This is the key used within this notebook, along with the raw data, for visualisation purposes.

__'SIL'__: Corresponding silhouette scores for each accepted source.

__PNR__: Corresponding pulse-to-noise ratio for each accepted source.

A simplified example of the output of the `decomposition` function can be seen below:

```raw
{'B': array([[ 0.00807129,  0.01498068, -0.05055092, ...,  0.03324424,
          0.01098719, -0.04423392],
        [ 0.00099551,  0.02325052, -0.04633348, ...,  0.01060206,
          0.00206237, -0.03023024],
        [-0.00079862,  0.04170231,  0.02396507, ..., -0.0069239 ,
         -0.00353031, -0.05398121],
        ...,
        [ 0.03401527,  0.00262566, -0.0032439 , ...,  0.00472695,
         -0.01023719,  0.02006415],
        [ 0.06270893,  0.00852112,  0.00463019, ..., -0.00228336,
         -0.03886996,  0.01297941],
        [ 0.05614772, -0.00944031,  0.00570728, ..., -0.00063509,
         -0.04714769, -0.00320849]]),
 'MUPulses': array([array([ 88042,  88264,  88598,  88810,  89117,  89359,  89597,  89814,
                90027,  90222,  90443,  90670,  90996,  91194,  91424,  91692,
                91920,  92273,  92650,  92922,  93178,  93441,  93656,  93888,
                94107,  94382,  94635,  94813,  95010,  95245,  95478,  95736,
                95956,  96275,  96535,  97034,  97352,  97591,  97964,  98221,
               122727, 122963, 123185, 123592, 123804, 124030, 124621, 124938,
               125287, 125634, 126067, 126212, 126400, 126609, 126802, 127068,
               127330, 127686, 128037, 128302, 128577, 128838, 129100, 129407,
               129682, 130028, 130287, 130652, 131062, 131518, 131799, 132185,
               132848])                                                       ,
        array([  6745,   6964,   7368,   8119,   8329,   8497,   8662,   8880,
                 9086,   9297,   9501,   9671,   9840,  10015,  10178,  10359,
                10551,  10741,  10916,  11099,  11228,  11396,  11554,  11710,
                11884,  12027,  12213,  12389,  12543,  12698,  12884,  13065,
                13237,  13391,  13555,  13724,  13881,  14049,  14234,  14394,
               202778, 203067, 203385, 203692, 203942, 204211, 204500, 204754,
               205087, 205415, 205794, 206021, 206292, 206559, 206830, 207179,
               207606, 207869, 208248, 209149, 209472, 209996])               ],
       dtype=object),
 'SIL': array([0.9935724 , 0.99662968]),
 'PNR': array([22.64379066, 25.86925002])}
 ```

 ## Optional: save the output object

 Cell below saves the output of the decomposition.

 ```python
 decomp_sample = output 
MuPulse = output["MUPulses"]
print(MuPulse.shape)
print(type(MuPulse))
# print(MuPulse[0, 1])
decomp_sample_pkl = open('decomp_sample_pkl.obj', 'wb') 
pickle.dump(decomp_sample, decomp_sample_pkl)
```

Cell below loads the output saved above. The sample pickle file is included in this directory, so you may uncomment the line below right away to become familiar with the UI.

```python
with open('decomp_sample_pkl.obj', 'rb') as f: output = pickle.load(f)
```

## Visualize results

Finally, run the cells below to get an interactive dashboard of the decomposed data.

There are two parameters for the `visualize_decomp` function. `decomp_results` and `raw` take in the decomposition results and raw signal, respectively. You are unlikely to want to change it within the function, and most likely will select those earlier. However, if you want to plug in the data directly, you may use those parameters.

There are three widgets controlling the rest of the dashboard:   
1. The `Motor Unit` widget for selecting the Motor Unit to examine.
2. The `Preset` parameter allows you to select arrangements of the channel. Currently, you may select between 'standard' and 'vert63' arrangements. New arrangements may easily be added within the `channel_preset` function in the `viz.py` script.
3. The `Method` widget allows you to select the metric for calculating the average mismatch score between peak contribution and average motor unit action potential (MUAP) shape. Currently, RMSE is the only available metric, but other metrics can be added easily in the future by adding functions to the `viz.py` script.

Below the widgets, dashboard contains four charts:

#### Chart 1: Signal Strength + Firing Rate. 
The top chart displays signal strength along with the instanteneous firing rate at that point.   
This chart allows for interval control. Select the interval of interest by clicking and dragging the mouse. Move around the interval by clicking on the selection and moving it around. The plots below zoom in according to this selection.

#### Chart 2: Firing Rate. 
The second chart displays the instanteneous firing rate of each spike. Outliers may be indicative of a false positive firing. Click on an individual data point to select corresponding the pulse. This will allow you to see the given firing's contribution to the MUAP shape.

#### Chart 3: Signal Strength
The third chart displays the signal strength of each firing. Click on an individual data point to select corresponding pulse. This will allow you to see the given firing's contribution to the MUAP shape.

#### Chart 4: MUAP Shapes + Peak Contributions
The last chart displays the average shape for each channel. The title displays the currently selected motor unit. If an individual peak has been selected using Chart 2 or 3, then an overlay will be displayed on each sub-chart that shows the contribution of the selected peak towards the shape for each channel. You may toggle the opacity of that overlay and the MUAP shape using the legend. Additionally, the peak firing time and RMSE will displayed in the title of the chart.

Further documentation of the visualization functions can be found [here](https://emgdecompy.readthedocs.io/en/stable/autoapi/emgdecompy/viz/index.html).

```python
visualize_decomp(output, raw)
```

