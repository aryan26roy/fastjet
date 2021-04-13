import numpy as np
import _core
a = [[1,2,3,4],[1,2,3,4]]
attr = {"R": 0.7}
sttr = {"algo": "antikt_algorithm"}
aa = _core.interface(a,attr,sttr)
print(aa)

