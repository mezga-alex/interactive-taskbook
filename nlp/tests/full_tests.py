"""
Script for complete testing the speed of applying
the Natural Language Processing (NLP) model to the given text
"""

import spacy
import matplotlib.pyplot as plt
import time
import pandas as pd
import seaborn as sns
import os
from tqdm import tqdm
import platform


def export_csv(result, param, continue_df):
    """
    Export calculated results to csv

    Parameters
    ----------
    result : list
        List of results parameters
    param : str
        Num of iterations
    continue_df : bool
        Signs of continuous experiment. Getting N times to illustrate mean expectance perfomance with deviation

    Returns
    -------
    path : str
        Path of saved csv table
    """

    indexes = ['time', 'size', 'num_batch']

    path = param + '_batch_result.csv'
    if continue_df and os.path.exists(path):
        df_default = pd.read_csv(path)
        df = pd.DataFrame(list(zip(result[0], result[1], result[2])),
                          columns=indexes)
        df = pd.concat([df_default, df], axis=0)
        print(df.shape)
    else:
        df = pd.DataFrame(list(zip(result[0], result[1], result[2])),
                          columns=indexes)

    df.to_csv(path, index=False, index_label=None)
    return path


def gather_csv(path):
    """
    Gather csv files by certain length of text

    Parameters
    ----------
    path_to_csv : str
        The path to the csv file

    Returns
    -------
    Nested list of csv file paths
    """
    all_size_file = []
    csv_files = os.listdir(path)
    for i in range(5000, 65000, 5000):
        current_size_file = []
        for file in csv_files:
            result = file.split('_')[1]
            if result == str(i):
                current_size_file.append(file)
        all_size_file.append(current_size_file)
    return all_size_file


def merge_csv(path):
    """
    Merge csv files by certain length of text

    Parameters
    ----------
    path_to_csv : str
        The path to the csv file

    Returns
    -------
    List of merged csv file paths
    """
    merged_paths = []
    all_size_file = gather_csv(path)
    mean_path = '/'.join(path.split('/')[:-2]) + '/mean/'
    os.makedirs(mean_path, exist_ok=True)
    for count in range(len(all_size_file)):
        df_all = pd.read_csv(path + all_size_file[count][0])
        for i in range(len(all_size_file[count])):
            cur_file = path + all_size_file[count][i]
            df_cur = pd.read_csv(cur_file)
            df_all = pd.concat([df_all, df_cur], axis=0)
        cur_csv_name = mean_path + 'text_all_' + str((count + 1) * 5000) + '.csv'
        df_all.to_csv(cur_csv_name)
        print(cur_csv_name)
        merged_paths.append(cur_csv_name)
    return merged_paths


def plot_results(path_to_csv, save_path='', res_type='len', computation_type='cpu', plt_show=False, verbose=True):
    """
    Plot results by provided path of csv file and type of result to plot

    Parameters
    ----------
    path_to_csv : str
        The path to the csv file
    save_path : str
        The path to save the plot.
    res_type : str
        'len' or 'num' - Build plot by length or number of batches.
    computation_type : str
        'cpu', 'gpu' - The type was used.
    plt_show : bool
        True for showing on IDE, False for better look in jupyter notebook.
    verbose : bool
        Detailed description.

    Returns
    -------
    Saved plot image
    """

    if save_path == '':
        save_path = os.path.dirname(os.path.abspath(path_to_csv)) + '/img/'
    os.makedirs(save_path, exist_ok=True)

    if res_type == "len":
        index_col = "size"
    elif res_type == "num":
        index_col = "num_batch"
    else:
        print("provided type: {} is not supported. Exiting".format(res_type))
        return

    df = pd.read_csv(path_to_csv, index_col=index_col)
    f, axes = plt.subplots(1, 1, figsize=(20, 10))
    f.canvas.set_window_title(path_to_csv)
    plt.title(path_to_csv)
    ax = sns.lineplot(x=df.index, y="time", data=df)
    print(path_to_csv)
    print(path_to_csv.split('/')[-1].split('.')[0])
    file_path = save_path + path_to_csv.split('/')[-1].split('.')[0] + '_' + res_type + '_' + computation_type + '.png'
    f.savefig(file_path)

    if verbose:
        print('image saved in: ', file_path)
    if plt_show:
        plt.show()


def time_measurement(text, nlp, min_batch_size=500, max_batch_size=5000, step=100, verbose=False):
    """
    Measures time of given text and params for it's evaluation

    Parameters
    ----------
    text : str
        Text for analysis.
    nlp :
        Loaded NLP Model.
    min_batch_size : int
        Minimum batch size.
    max_batch_size : int
        Maximum batch size.
    step : int
        Step to iterate over size.
    verbose : bool
        Detailed description

    Returns
    -------
    list:
        List contains:
        1. Runtime list
        2. Batches size list.
        3. Number of batches list.
    """
    text_len = len(text)

    # Check the boundaries
    if min_batch_size > text_len:
        min_batch_size = text_len
    if max_batch_size > text_len:
        max_batch_size = text_len
    if max_batch_size < min_batch_size:
        max_batch_size = min_batch_size

    # Outer loop for batch size
    time_arr = []
    size_arr = []
    num_batches = []
    batch_size = min_batch_size
    while batch_size <= max_batch_size:
        text_batches = []
        start_span = 0

        # Inner loop for a specific size
        while start_span < text_len:
            end_span = start_span + batch_size
            # Check the out of range
            if end_span > text_len:
                end_span = text_len

            batch = text[start_span:end_span]
            text_batches.append(batch)

            start_span = end_span

        # Runtime Measure
        start_time = time.time()
        list(nlp.pipe(text_batches))
        elapsed_time = time.time() - start_time

        time_arr.append(elapsed_time)
        num_batches.append(len(text_batches))
        size_arr.append(batch_size)

        if verbose:
            last_batch = text_batches[len(text_batches) - 1]
            print("-" * 30)
            print("Text length = ", text_len)
            print("Batch size = ", batch_size)
            print("Num of batches = ", len(text_batches))
            print("Last batch size = ", len(last_batch))

        batch_size += step

    return [time_arr, size_arr, num_batches]


def test_batch(path, num_of_times=3, min_batch_size=500, max_batch_size=5000, step=100, computation_type='cpu'):
    """
    Test text splitted by batches for given number of times
    Parameters
    ----------
    path : str
        Path of given text.
    num_of_times : int
        Number of times to measure each text.
    min_batch_size : int
        Minimum size of batches.
    max_batch_size : int
        Maximum size of batches.
    step : int
        Step to increase the size of the batch.
    gpu : bool
        Flag to enable calculations on GPU.

    Returns
    -------
    Saves csv and png file with results
    """
    available_comp_types = ['cpu', 'gpu']
    if computation_type not in available_comp_types:
        print('wrong computation type: {} from available {}', format(computation_type, available_comp_types))
    if computation_type == 'gpu':
        activated = spacy.prefer_gpu()
        if activated:
            print('GPU is activated.')
        else:
            print('GPU is not activated. Running on the CPU.')
            computation_type = 'cpu'

    os.chdir(os.path.dirname(os.path.abspath(path)))
    os.chdir('..')
    res_root_path = os.curdir + '/results/' + computation_type + '/'

    img_res_path = res_root_path + 'img/'
    if not os.path.exists(img_res_path):
        os.makedirs(img_res_path)

    csv_res_path = res_root_path + 'csv/'
    if not os.path.exists(csv_res_path):
        os.makedirs(csv_res_path)

    # extract name of text file
    text_name = path.split('/')[-1].split('.')[0]

    # ######## PARSING WITH BATCHES ######
    text_full = open(path).read().lower()

    nlp = spacy.load('en_core_web_lg')
    nlp.max_length = 1500000

    csv_path_name = csv_res_path + text_name + '_' + str(num_of_times)
    for i in range(num_of_times):
        result = time_measurement(text_full, nlp, min_batch_size, max_batch_size, step)
        csv_file = export_csv(result, csv_path_name, continue_df=True)

    print("csv saved in: ", csv_file)

    # plot results by csv files
    plot_results(csv_file, save_path=img_res_path, res_type='len', computation_type=computation_type, plt_show=False)
    plot_results(csv_file, save_path=img_res_path, res_type='num', computation_type=computation_type, plt_show=False)


def test_full_text(path):
    """
    Test full text by it's given path

    Parameters
    ----------
    path : str
        Path to the text

    Returns
    -------
    elapsed_time :
        Execution time in seconds
    """
    text_full = open(path).read().lower()
    nlp = spacy.load('en_core_web_lg')
    nlp.max_length = 1500000

    start_time = time.time()
    doc = nlp(text_full)
    elapsed_time = time.time() - start_time
    return elapsed_time


def test_text_folder(folder_path, computation_type='cpu'):
    """
    Test full text by it's given path

    Parameters
    ----------
    folder_path : str
        Path to the folder full of texts to test

    Returns
    -------
    Run tests for given parameters, check test_batch
    Merge calculated results by merge_results functions
    Plots merge results of various text length
    """
    # for text folders
    # folder_path = './texts/'
    text_files = os.listdir(folder_path)
    print('Files in a folder: ', len(text_files))

    # for file in text_files:
    # if file.endswith(".txt"):
    for i in tqdm(range(len(text_files))):
        if text_files[i].endswith(".txt"):
            file_path = folder_path + text_files[i]
            print('processing: ', file_path)
            test_batch(file_path, num_of_times=3, min_batch_size=500, max_batch_size=10000, step=100,
                       computation_type=computation_type)

    csv_path = './results/'+computation_type+'/csv/'
    img_path = './results/'+computation_type+'/img/mean'
    merged_paths = merge_csv(csv_path)
    for merged_csv in merged_paths:
        plot_results(merged_csv, save_path=img_path, res_type='len', computation_type=computation_type, plt_show=False)
        plot_results(merged_csv, save_path=img_path, res_type='num', computation_type=computation_type, plt_show=False)


def plot_mean(csv_mean_path, res_type):
    if res_type == "len":
        index_col = "size"
    elif res_type == "num":
        index_col = "num_batch"
    else:
        print("provided type: {} is not supported. Exiting".format(res_type))
        return

    g = plt.figure(figsize=(12, 20))
    sns.set(style="darkgrid")
    sns.despine(offset=10, trim=True);

    mode = csv_mean_path.split('/')[-3].upper()
    results = '/'.join(csv_mean_path.split('/')[:-3]) + "/"

    csv_files = sorted(os.listdir(csv_mean_path), reverse=True)
    # print(csv_files)

    labels = [mode + ', length: ' + i.split(".")[0].split("_")[-1] for i in csv_files]
    # print(labels)
    for i in range(len(csv_files)):
        csv_file = csv_mean_path + csv_files[i]
        df = pd.read_csv(csv_file)
        sns.lineplot(x=index_col, y="time", data=df, legend=False)
    plt.legend(title='Comparison', loc='center right', labels=labels)
    file_path = results + 'mean_all_' + mode + "_" + res_type + '.png'
    g.savefig(file_path)
    # plt.show(g)


def plot_each_mean(csv_mean_path, res_type):
    if res_type == "len":
        index_col = "size"
    elif res_type == "num":
        index_col = "num_batch"
    else:
        print("provided type: {} is not supported. Exiting".format(res_type))
        return

    mode = csv_mean_path.split('/')[-3].upper()
    results = '/'.join(csv_mean_path.split('/')[:-3]) + "/"

    csv_files = sorted(os.listdir(csv_mean_path), reverse=True)
    # print(csv_files)

    labels = [mode + ', length: ' + i.split(".")[0].split("_")[-1] for i in csv_files]
    lengths = [i.split(".")[0].split("_")[-1] for i in csv_files]
    # print(labels)
    for i in range(len(csv_files)):
        g = plt.figure(figsize=(8, 6))
        sns.set(style="darkgrid")
        sns.despine(offset=10, trim=True)
        csv_file = csv_mean_path + csv_files[i]
        df = pd.read_csv(csv_file)
        ax = sns.lineplot(x=index_col, y="time", data=df, legend=False)
        ax.set_title("length: " + lengths[i])
        # plt.legend(title='Comparison', loc='center right', labels=labels[i])
        file_path = results + 'mean_' + lengths[i] + "_" + mode + "_" + res_type + '.png'
        g.savefig(file_path)


def plot_cpu_vs_gpu(cpu_csv_folder, gpu_csv_folder, res_type, plot_grid=True):
    """

    """
    if res_type == "len":
        index_col = "size"
    elif res_type == "num":
        index_col = "num_batch"
    else:
        print("provided type: {} is not supported. Exiting".format(res_type))
        return

    results = '/'.join(cpu_csv_folder.split('/')[:-3]) + "/"
    cpu_files = sorted(os.listdir(cpu_csv_folder), reverse=True)
    gpu_files = sorted(os.listdir(gpu_csv_folder), reverse=True)
    # print(cpu_files)
    # print(gpu_files)

    labels_gpu = ['GPU, length: ' + i.split(".")[0].split("_")[1] for i in gpu_files]
    labels_cpu = ['CPU, length: ' + i.split(".")[0].split("_")[1] for i in cpu_files]
    # print(labels_gpu)

    for i in tqdm(range(min(len(cpu_files), len(gpu_files)))):
        g = plt.figure(figsize=(6, 8))
        cpu_file = cpu_csv_folder + cpu_files[i]
        gpu_file = gpu_csv_folder + gpu_files[i]
        df_cpu = pd.read_csv(cpu_file)
        df_gpu = pd.read_csv(gpu_file)
        sns.set(style="darkgrid")
        sns.despine(offset=10, trim=True);
        sns.lineplot(x=index_col, y="time", data=df_cpu, legend=False)
        sns.lineplot(x=index_col, y="time", data=df_gpu, legend=False)
        plt.legend(title='Comparison', loc='center right', labels=[labels_cpu[i], labels_gpu[i]])
        file_path = results + labels_cpu[i].split(':')[-1] + "_" + res_type + '_CPU_vs_GPU.png'

        g.savefig(file_path)
        plt.close(g)
        # plt.show(g)

    if plot_grid:

        f, axes = plt.subplots(4, 3, figsize=(30, 30), sharex=True)
        plt.title("GPU vs CPU speed comparison on various texts length")
        sns.set(style="darkgrid")
        sns.despine(left=True)
        sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
        f.canvas.set_window_title("Grid")

        # plt.title(path_to_csv)
        count = 0
        for i in range(4):
            for j in range(3):
                cpu_file = cpu_csv_folder + cpu_files[count]
                gpu_file = gpu_csv_folder + gpu_files[count]

                df_cpu = pd.read_csv(cpu_file)
                df_gpu = pd.read_csv(gpu_file)

                ax = sns.lineplot(x=index_col, y="time", data=df_cpu, legend="brief", ax=axes[i, j])
                ax = sns.lineplot(x=index_col, y="time", data=df_gpu, legend=False, ax=axes[i, j])
                ax.legend(title='Comparison', loc='center right', labels=["CPU", "GPU"])
                ax.set_title("length: " + labels_cpu[count].split(':')[-1])
                count += 1

        grid_file_path = results + "_" + res_type + '_CPU_vs_GPU_Grid.png'
        f.savefig(grid_file_path)
        plt.close(f)



def main():
    folder_path = './texts/'
    cpu_results_csv = "./results_sm/cpu/csv/"
    gpu_results_csv = './results_sm/gpu/csv/'
    # test_text_folder(folder_path, 'cpu')
    plot_cpu_vs_gpu(cpu_results_csv, gpu_results_csv, 'len', plot_grid=True)

if __name__ == '__main__':
    main()
