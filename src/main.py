import multiprocessing
from multiprocessing import Process
import math

def prefix_sum(elements):
    res = [0] * (len(elements) + 1)
    for i in range(0, len(elements)):
        res[i+1] = res[i] + elements[i]

    return res


def _get_number_of_processes(arr_len, cores, step_size):
    max_processes = int(arr_len / step_size) + 1
    return max_processes if max_processes >= cores else cores


def up_sum(arr, proc_number, total_processes, step_size):
    start = proc_number * step_size
    end = (proc_number + 1) * step_size - 1


def up_phase(arr, cores):
    for l in range(0, int(math.log(len(arr), 2))):
        step_size = 2 ** (l + 1)
        number_of_processes = _get_number_of_processes(len(arr), cores, step_size)
        for i in range(0, number_of_processes):
            process = Process(target=up_sum)

def parallel_prefix_sum(elements):
    thread_safe_arr = multiprocessing.Array(int, elements + [0])

