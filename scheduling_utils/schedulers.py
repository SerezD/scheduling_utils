from abc import ABC, abstractmethod
import math


class Scheduler(ABC):
    """
    Base abstract class for all schedulers
    """
    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):

        if start_step >= stop_step:
            raise AttributeError('In the scheduler, start step must be minor that stop step!')

        if start_value < stop_value:
            print('Initializing Scheduler to Ramp Value')
        elif start_value > stop_value:
            print('Initializing Scheduler to Decay Value')
        else:
            print('Initializing Scheduler with no effect!')

        self._start_step = start_step
        self._stop_step = stop_step

        self._start_value = start_value
        self._stop_value = stop_value

    @abstractmethod
    def warp_func(self, perc_step: float):
        pass

    def _get_perc_step(self, step: int):

        # step normalized in 0_1 range
        return max(0, min(1, (step - self._start_step) / (self._stop_step - self._start_step)))

    def _get_value(self, perc_step: float):
        return perc_step * self._stop_value + (1 - perc_step) * self._start_value

    def step(self, step: int):

        # step normalized in 0_1 range
        perc_step = self._get_perc_step(step)

        # warp perc according to scheduler type
        perc_step = self.warp_func(perc_step)

        return self._get_value(perc_step)


class CosineScheduler(Scheduler):

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):
        super().__init__(start_step, stop_step, start_value, stop_value)

    def warp_func(self, perc_step: float):

        # warp with cosine
        return 1.0 - math.cos(perc_step * math.pi / 2)


class LinearScheduler(Scheduler):

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):
        super().__init__(start_step, stop_step, start_value, stop_value)

    def warp_func(self, perc_step: float):

        # Identity warp
        return perc_step


