# loadmat is used to load MATLAB data
from scipy.io import loadmat

# Pickle allows saving and loading Python objects into a file
import os
from logger import setup_experiment_logger, log_and_print
import scipy.io as sio
import pickle as pkl
import joblib as jb


from emgdecompy_wenlab.decomposition import *
from emgdecompy_wenlab.contrast import *
from emgdecompy_wenlab.viz import *
from emgdecompy_wenlab.preprocessing import *
from file_utils import find_mat_files, load_mat_file, update_mat_file, save_pkl_file
import argparse 

import tkinter as tk
from tkinter import filedialog


def find_mat_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    else:
        mat_files = [f for f in os.listdir(directory) if f.endswith('.mat')]
        sorted_mat_files = sorted(mat_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        return mat_files, sorted_mat_files
    
def load_mat_file(file_path):
    data = sio.loadmat(file_path)
    return data

def update_mat_file(data, file_dir, file_name):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        print(f"Created directory: {file_dir}")
    
    else:
        file_path = os.path.join(file_dir, file_name)
        sio.savemat(file_path, data)
    print(f"Updated file: {file_path}")

def save_pkl_file(data, file_dir, file_name):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        print(f"Created directory: {file_dir}")
    file_path = os.path.join(file_dir, file_name)
    jb.dump(data, file_path)
    print(f"Updated file: {file_path}")

def select_files_from_list(mat_files):
    """
    Create a GUI window to select .mat files from a list
    
    Args:
        mat_files (list): List of available .mat files
        
    Returns:
        list: Selected .mat files
    """
    def on_select():
        selected_indices = listbox.curselection()
        selected_files = [listbox.get(i) for i in selected_indices]
        window.selected_files = selected_files
        window.quit()  # First quit the mainloop
        window.destroy()  # Then destroy the window

    window = tk.Tk()
    window.title("Select .mat files")
    window.selected_files = []
    
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    label = tk.Label(frame, text="Select one or multiple .mat files (hold Ctrl/Cmd for multiple)")
    label.pack()
    
    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50)
    listbox.pack()
    
    for file in mat_files:
        listbox.insert(tk.END, file)
    
    select_button = tk.Button(frame, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    window.mainloop()
    return window.selected_files


def main():
    """
    Run the motor unit decomposition pipeline
    """
    def select_folder(message:str="Select folder for raw data"):
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title=message)
        return folder_path
    
    log_dir = select_folder("Please select directory for log files")
    print(f"Selected folder: {log_dir}, all log files will be saved in this directory")
    logger = setup_experiment_logger(name="mudecomp", report_dir=log_dir)
    log_and_print(logger, f"Selected folder: {log_dir}, all log files will be saved in this directory")

    data_dir = select_folder("Please select directory for raw data")
    log_and_print(logger, f"Selected folder: {data_dir} for raw data")

    mat_files, sorted_mat_files = find_mat_files(data_dir)

    selected_files = select_files_from_list(mat_files)
    log_and_print(logger, f"Selected files: {selected_files}")

    output_dir = select_folder("Please select directory for output data")

    for file in selected_files:
        print(f"Processing file: {file}")
        file_name = os.path.join(data_dir, file)
        name = file[:-4]
        data = load_mat_file(file_name)
        raw = data["SIG"]
        discard_channel = data["discardChannelsVec"]
        fsamp = data["fsamp"]
        iterations = data["DecompRuns"]
        PNR_list = data["PNR"]
        min_pnr = min(PNR_list)
        print(f"Minimum PNR: {min_pnr}")
        pnr_thred = input("Enter PNR threshold: ")
        output = decomposition(raw,\
                        discard=None,\
                        discard_indices=None,\
                        R=16,\
                        M=iterations,\
                        bandpass=True,\
                        lowcut=10,\
                        highcut = 900,\
                        fs=fsamp,\
                        order=6,\
                        Tolx=10e-4,\
                        contrast_fun=skew,\
                        ortho_fun=gram_schmidt,\
                        max_iter_sep=10,\
                        l=31,\
                        sil_pnr=False,\
                        thresh=pnr_thred,\
                        max_iter_ref=10,\
                        random_seed=None,\
                        verbose=False)
        MuPulse = output["MUPulses"]
        old_MuPulse = data["MUPulses"]
        data["old_MUPulses"] = old_MuPulse
        data["MUPulses"] = MuPulse
        old_pnr = data["PNR"]
        data["old_PNR"] = old_pnr
        data["PNR"] = output["PNR"]
        data["SIL"] = output["SIL"]
        update_mat_file(data, output_dir, file)
        output_name = f"{name}_decom.pkl"
        save_pkl_file(output, output_dir, output_name)
        

        



if __name__ == "__main__":
    main()
