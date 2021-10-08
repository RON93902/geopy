# This script runs an example matlab function from Python (triarea.m)

import matlab.engine
eng = matlab.engine.start_matlab()
ret = eng.triarea(1.0,5.0)
print(ret)