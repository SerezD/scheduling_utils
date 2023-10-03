import time
# from scheduling_utils.schedulers import CosineScheduler, LinearScheduler, LinearCosineScheduler
from scheduling_utils.schedulers_cpp import CosineScheduler, LinearScheduler, LinearCosineScheduler


def main():
    # keep track of execution time in different versions.
    time_version_python = {'linear': 0.3701941967010498,
                           'cosine': 0.4488193988800049,
                           'linear_cosine': 0.4803807735443115}

    time_version_cpp = {'linear': 0.3726363182067871,
                        'cosine': 0.3791532516479492,
                        'linear_cosine': 0.37397074699401855}

    for name, scheduler in zip(['cosine', 'linear', 'linear_cosine'],
                               [CosineScheduler, LinearScheduler, LinearCosineScheduler]):

        start_step, th_step, stop_step = 0, 5000, 1000000

        start_value = 1e-3
        stop_value = 1e-10

        if name == 'linear_cosine':
            s = scheduler(start_step, stop_step, start_value, stop_value, th_step)
        else:
            s = scheduler(start_step, stop_step, start_value, stop_value)

        values = []

        start_time = time.time()
        for i in range(stop_step):
            values.append(s.step(i))
        time_version_cpp[name] = time.time() - start_time

        s.destroy()

    print(time_version_cpp)


if __name__ == '__main__':
    main()
