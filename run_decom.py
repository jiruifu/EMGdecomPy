# loadmat is used to load MATLAB data
from scipy.io import loadmat

# Pickle allows saving and loading Python objects into a file
import os
from logger import setup_experiment_logger, log_and_print
import scipy.io as sio
import pickle as pkl
import joblib as jb


from decomposition import *
from contrast import *
from viz import *
from preprocessing import *
from file_utils import find_mat_files, load_mat_file, update_mat_file, save_pkl_file
import argparse 

import tkinter as tk
from tkinter import filedialog

import traceback


def find_mat_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    else:
        mat_files = [f for f in os.listdir(directory) if f.endswith('.mat')]
        sorted_mat_files = sorted(mat_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        return mat_files, sorted_mat_files

def find_pkl_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    else:
        pkl_files = [f for f in os.listdir(directory) if f.endswith(('.pkl', '.pickle'))]
        try:
            # Try to sort by number in filename
            sorted_pkl_files = sorted(pkl_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        except (ValueError, IndexError):
            # If sorting by number fails, sort alphabetically
            sorted_pkl_files = sorted(pkl_files)
        return pkl_files, sorted_pkl_files

    
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

def select_single_pkl_file(pkl_files):
    def on_select():
        selected_indices = listbox.curselection()
        if selected_indices:  # Check if any selection was made
            selected_file = listbox.get(selected_indices[0])  # Get only the first selection
            window.selected_file = selected_file
        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("Select PKL file")
    window.selected_file = None
    
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    label = tk.Label(frame, text="Select a single pkl file")
    label.pack()
    
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50)  # Changed to SINGLE mode
    listbox.pack()
    
    for file in pkl_files:
        listbox.insert(tk.END, file)
    
    select_button = tk.Button(frame, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    window.mainloop()
    return window.selected_file

def select_single_mat_file(pkl_files):
    def on_select():
        selected_indices = listbox.curselection()
        if selected_indices:  # Check if any selection was made
            selected_file = listbox.get(selected_indices[0])  # Get only the first selection
            window.selected_file = selected_file
        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("Select PKL file")
    window.selected_file = None
    
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    label = tk.Label(frame, text="Select a single mat file")
    label.pack()
    
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50)  # Changed to SINGLE mode
    listbox.pack()
    
    for file in pkl_files:
        listbox.insert(tk.END, file)
    
    select_button = tk.Button(frame, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    window.mainloop()
    return window.selected_file

def select_path(message:str="Select folder for raw data"):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=message)
    return folder_path

def visualize_result():
    import panel as pn
    import sys
    
    # Initialize panel extension for running outside notebook
    pn.extension()
    
    def close_app(event):
        """Close the application and exit"""
        sys.exit(0)
    
    result_dir = select_path("Please select directory for result files")
    mat_files, sorted_mat_files = find_mat_files(result_dir)
    selected_file = select_single_mat_file(mat_files)
    data = load_mat_file(os.path.join(result_dir, selected_file))
    raw = data["SIG"]
    name = selected_file[:-4]
    pkl_file = f"{name}_decom.pkl"
    output = jb.load(os.path.join(result_dir, pkl_file))
    
    # Create the dashboard
    dashboard = visualize_decomp(output, raw)
    
    # Add a close button
    close_button = pn.widgets.Button(name='Close Visualization', button_type='danger')
    close_button.on_click(close_app)
    
    # Add the close button to the dashboard
    dashboard_with_button = pn.Column(dashboard, close_button)
    
    # Serve the panel application
    dashboard_with_button.show(title=f"Decomposition Results - {name}", port=5006)

def select_action():
    """
    Create a GUI window to select the action to perform
    
    Returns:
        str: Selected action ('visualize', 'train', or None)
    """
    def on_visualize():
        window.selected_action = 'visualize'
        window.quit()
        window.destroy()
        
    def on_train():
        window.selected_action = 'train'
        window.quit()
        window.destroy()
        
    def on_cancel():
        window.selected_action = None
        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("Select Action")
    window.selected_action = None
    
    frame = tk.Frame(window)
    frame.pack(padx=20, pady=20)
    
    label = tk.Label(frame, text="What would you like to do?", font=('Arial', 12))
    label.pack(pady=10)
    
    visualize_button = tk.Button(frame, text="Visualize Result", command=on_visualize, width=20)
    visualize_button.pack(pady=5)
    
    train_button = tk.Button(frame, text="Train Model", command=on_train, width=20)
    train_button.pack(pady=5)
    
    cancel_button = tk.Button(frame, text="Cancel", command=on_cancel, width=20)
    cancel_button.pack(pady=10)
    
    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    window.mainloop()
    return window.selected_action

def main():

    """
    Run the motor unit decomposition pipeline
    """
    def select_folder(message:str="Select folder for raw data"):
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title=message)
        return folder_path
    try:
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
            log_and_print(logger, f"Processing file: {file}")
            
            file_name = os.path.join(data_dir, file)
            name = file[:-4]
            data = load_mat_file(file_name)
            raw = data["SIG"]
            discard_channel = data["discardChannelsVec"]
            fsamp = data["fsamp"]
            log_and_print(logger, f"Sampling rate: {fsamp}")
            iterations = data["DecompRuns"]
            log_and_print(logger, f"Will run decomposition for {iterations[0][0]} iterations")
            threshold = True
            if threshold == False:
                PNR_list = data["PNR"]
                min_pnr = min(PNR_list)
                log_and_print(logger, f"Minimum PNR: {min_pnr}")
                pnr_thred = float(input("Enter PNR threshold: "))
                thred = pnr_thred
            else:
                thred = 0.9
            output = decomposition(raw,\
                            discard=None,\
                            discard_indices=None,\
                            R=16,\
                            M=iterations[0][0],\
                            bandpass=True,\
                            lowcut=10,\
                            highcut = 900,\
                            fs=fsamp[0][0],\
                            order=6,\
                            Tolx=10e-4,\
                            contrast_fun=skew,\
                            ortho_fun=gram_schmidt,\
                            max_iter_sep=10,\
                            l=31,\
                            sil_pnr=threshold,\
                            thresh=thred,\
                            max_iter_ref=10,\
                            random_seed=None,\
                            verbose=True,\
                            log=logger)
            MuPulse = output["MUPulses"]
            old_MuPulse = data["MUPulses"]
            B = output["B"]
            log_and_print(logger, f"The shape of B is {B.shape}")
            data["old_MUPulses"] = old_MuPulse
            data["MUPulses"] = MuPulse
            log_and_print(logger, f"The shape of MUPulses is {MuPulse.shape}")
            old_pnr = data["PNR"]
            data["old_PNR"] = old_pnr
            data["PNR"] = output["PNR"]
            log_and_print(logger, f"The new PNR is {output['PNR']}")
            data["SIL"] = output["SIL"]
            log_and_print(logger, f"The new SIL is {output['SIL']}")
            update_mat_file(data, output_dir, file)
            output_name = f"{name}_decom.pkl"
            save_pkl_file(output, output_dir, output_name)

            visualize = input("Visualize result? (y/n)")
            if visualize == "y":
                visualize_result()
            else:
                log_and_print(logger, "Skipping visualization")
        
    except Exception as e:
        traceback.print_exc()
        log_and_print(logger, f"Error: {e}")
        print(f"End with error: {e}")


        



if __name__ == "__main__":
    action = select_action()
    if action == 'visualize':
        visualize_result()
    elif action == 'train':
        main()
    else:
        print("Operation cancelled")
