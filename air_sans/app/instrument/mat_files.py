import scipy.io as sio


def read_mask_mat_file(filename):
    mat_contents = sio.loadmat(filename)
    return mat_contents["mask_data"]


def read_efficiency_mat_file_data(filename):
    mat_contents = sio.loadmat(filename)
    return mat_contents["eff_data"]


def read_efficiency_mat_file_error(filename):
    mat_contents = sio.loadmat(filename)
    return mat_contents["eff_err_data"]
