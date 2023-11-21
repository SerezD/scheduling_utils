import ctypes
from pathlib import Path
import platform

# Load the shared library
this_directory = Path(__file__).parent

if 'windows' in platform.system().lower():
    schedulers_cpp = ctypes.CDLL(f'{this_directory}/cpp_extensions/schedulers_win.dll')
else:
    schedulers_cpp = ctypes.CDLL(f'{Path(__file__).parent}/cpp_extensions/schedulers.so')


# Define Python wrappers
class CosineScheduler:

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):

        super().__init__()

        # method signatures
        schedulers_cpp.CosineScheduler_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
        schedulers_cpp.CosineScheduler_create.restype = ctypes.c_void_p

        schedulers_cpp.CosineScheduler_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
        schedulers_cpp.CosineScheduler_step.restype = ctypes.c_double

        schedulers_cpp.CosineScheduler_destroy.argtypes = [ctypes.c_void_p]

        # constructor
        self.s = schedulers_cpp.CosineScheduler_create(start_step, stop_step, start_value, stop_value)

    def step(self, step: int):
        return schedulers_cpp.CosineScheduler_step(self.s, step)

    def destroy(self):
        schedulers_cpp.CosineScheduler_destroy(self.s)


class LinearScheduler:

    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float):

        super().__init__()

        # method signatures
        schedulers_cpp.LinearScheduler_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
        schedulers_cpp.LinearScheduler_create.restype = ctypes.c_void_p

        schedulers_cpp.LinearScheduler_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
        schedulers_cpp.LinearScheduler_step.restype = ctypes.c_double

        schedulers_cpp.LinearScheduler_destroy.argtypes = [ctypes.c_void_p]

        # constructor
        self.s = schedulers_cpp.LinearScheduler_create(start_step, stop_step, start_value, stop_value)

    def step(self, step: int):
        return schedulers_cpp.LinearScheduler_step(self.s, step)

    def destroy(self):
        schedulers_cpp.LinearScheduler_destroy(self.s)


class LinearCosineScheduler:
    def __init__(self, start_step: int, stop_step: int, start_value: float, stop_value: float, th_step: int):

        # method signatures
        schedulers_cpp.LinearCosineScheduler_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double,
                                                            ctypes.c_double]
        schedulers_cpp.LinearCosineScheduler_create.restype = ctypes.c_void_p

        schedulers_cpp.LinearCosineScheduler_step.argtypes = [ctypes.c_void_p, ctypes.c_int]
        schedulers_cpp.LinearCosineScheduler_step.restype = ctypes.c_double

        schedulers_cpp.LinearCosineScheduler_destroy.argtypes = [ctypes.c_void_p]

        # constructor
        self.s = schedulers_cpp.LinearCosineScheduler_create(start_step, stop_step, start_value, stop_value, th_step)

    def step(self, step: int):
        return schedulers_cpp.LinearCosineScheduler_step(self.s, step)

    def destroy(self):
        schedulers_cpp.LinearCosineScheduler_destroy(self.s)
