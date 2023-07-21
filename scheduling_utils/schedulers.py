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

        # get step normalized in 0_1 range
        return max(0, min(1, (step - self._start_step) / (self._stop_step - self._start_step)))

    def _get_value(self, perc_step: float):
        # get value at perc_step
        return self._start_value + (self._stop_value - self._start_value) * perc_step

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
        # math.cos(math.pi * perc_step) goes from 1 to -1
        # sum 1 and mul 0.5 to normalize
        # then reverse since you still want a perc step as output
        return 1 - (0.5 * (1. + math.cos(math.pi * perc_step)))


class LinearScheduler(Scheduler):

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):
        super().__init__(start_step, stop_step, start_value, stop_value)

    def warp_func(self, perc_step: float):

        # Identity warp
        return perc_step


class LinearCosineScheduler:
    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float, th_step: int):
        """
        Linear Warmup Followed by Cosine Decay.
        Learning rate increases from start_step tp th_step (0.0 to start_value) and then decays to stop_value
        """

        if start_value <= stop_value:
            raise AttributeError('the LinearCosine Scheduler must decay.')

        if start_step >= stop_step:
            raise AttributeError('In the scheduler, start step must be minor that stop step!')

        if not start_step < th_step and th_step < stop_step:
            raise AttributeError('In the scheduler, threshold step must lay between start and stop steps!')

        super().__init__()

        self.th_step = th_step
        self.linear_wu = LinearScheduler(start_step, th_step, 0, start_value)
        self.cosine_decay = CosineScheduler(th_step, stop_step, start_value, stop_value)

    def step(self, step: int):

        if step < self.th_step:
            return self.linear_wu.step(step)
        else:
            return self.cosine_decay.step(step)
