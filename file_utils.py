import os
import scipy.io as sio
import pickle as pkl
import joblib as jb

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

