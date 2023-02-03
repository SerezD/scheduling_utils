from matplotlib import pyplot as plt
import random

from schedulers import CosineScheduler, LinearScheduler


def plot_schedulers():

    for name, scheduler in zip(['cosine', 'linear'], [CosineScheduler, LinearScheduler]):

        # may raise Error if stop step < start step (intended)
        start_step = random.randint(0, 20)
        stop_step = random.randint(15, 40)

        start_value = random.randint(0, 50)
        stop_value = random.randint(0, 50)

        try:
            s = scheduler(start_step, stop_step, start_value, stop_value)

            values = []
            for i in range(stop_step + 5):
                values.append(s.step(i))

            plt.suptitle(f'{name}: from ({start_step}, {start_value}) to ({stop_step}, {stop_value})')
            plt.plot(values)
            plt.show()

        except AttributeError as e:
            print(f'start_step: {start_step} - stop_step: {stop_step}')
            print(e)


if __name__ == '__main__':

    plot_schedulers()
