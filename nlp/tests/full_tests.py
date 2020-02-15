import spacy
import matplotlib.pyplot as plt
import time
import pandas as pd
import seaborn as sns
import os
import platform


def export_csv(result, param, continue_df):
    """
    Export results to csv

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
    merged_paths = []
    all_size_file = gather_csv(path)
    print(all_size_file)
    for count in range(len(all_size_file)):
        df_all = pd.read_csv(path + all_size_file[count][0])
        for i in range(len(all_size_file[count])):
            cur_file = path+all_size_file[count][i]
            df_cur = pd.read_csv(cur_file)
            df_all = pd.concat([df_all, df_cur], axis=0)
        cur_csv_name = path+'text_all_'+str((count+1)*5000)+'.csv'
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
    file_path = save_path+path_to_csv.split('/')[-1].split('.')[0]+'_'+res_type+'_'+computation_type+'.png'
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


def test_batch(path, num_of_times=3, min_batch_size=500, max_batch_size=5000, step=100, gpu=False):
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
    comp_type = 'cpu'
    if gpu:
        activated = spacy.prefer_gpu()
        if activated:
            comp_type = 'gpu'
            print('GPU is activated.')
        else:
            print('GPU is not activated. Running on the CPU.')

    os.chdir(os.path.dirname(os.path.abspath(path)))
    os.chdir('..')
    res_root_path = os.curdir + '/results/' + comp_type + '/'

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

    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    csv_path_name = csv_res_path + text_name + '_' + str(num_of_times)
    for i in range(num_of_times):
        result = time_measurement(text_full, nlp, min_batch_size, max_batch_size, step)
        csv_file = export_csv(result, csv_path_name, continue_df=True)

    print("csv saved in: ", csv_file)

    # plot results by csv files
    plot_results(csv_file, save_path=img_res_path, res_type='len', computation_type=comp_type, plt_show=False)
    plot_results(csv_file, save_path=img_res_path, res_type='num', computation_type=comp_type, plt_show=False)


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
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000

    start_time = time.time()
    doc = nlp(text_full)
    elapsed_time = time.time() - start_time
    return elapsed_time


def main():
    # for text folders
    folder_path = './texts/'
    text_files = os.listdir(folder_path)
    print('Files in a folder: ', len(text_files))

    for file in text_files:
        if file.endswith(".txt"):
            file_path = folder_path + file
            print('processing: ', file_path)
            test_batch(file_path, num_of_times=3, min_batch_size=500, max_batch_size=10000, step=100, gpu=False)

    csv_path = './results/cpu/csv/'
    img_path = './results/cpu/img/mean'
    merged_paths = merge_csv(csv_path)
    for merged_csv in merged_paths:
        plot_results(merged_csv, save_path=img_path, res_type='len', computation_type='cpu', plt_show=False)
        plot_results(merged_csv, save_path=img_path, res_type='num', computation_type='cpu', plt_show=False)


if __name__ == '__main__':
    main()
