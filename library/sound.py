from microbit import *

offset = 580

def read():
    return pin2.read_analog() - offset

def wait_for_double_clap(timeout=1000, spread=500, sensitivity=75):
    sensitivity = 105 - sensitivity

    clap_one_time = None

    start_time = running_time()
    while running_time() - start_time < timeout:
        if read() > sensitivity:
            while read() > sensitivity:
                pass
            sleep(100)
            if clap_one_time is not None and running_time() - clap_one_time < spread:
                return True
            else:
                clap_one_time = running_time()

    return False

def wait_for_clap(timeout=1000, sensitivity=75):
    sensitivity = 105 - sensitivity

    start_time = running_time()
    while running_time() - start_time < timeout:
        if read() > sensitivity:
            return True

    return False
