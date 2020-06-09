#!/usr/bin/env python

# --- Compiler call
# gcc -shared -rdynamic aurem_c.c -o aurem_c.so

from obspy import read
import numpy as np
import ctypes as C
import pathlib
import matplotlib.pyplot as plt


libname= "/home/matteo/miniconda3/envs/aurem/lib/python3.6/site-packages/aurem_clib.cpython-36m-x86_64-linux-gnu.so"
#libname = pathlib.Path().absolute()/"aurem_c.so"
myclib = C.CDLL(libname)

print(libname)
st = read()
tr = st[0]
tr.detrend("linear")
tr.detrend("demean")

#simplearr = np.array([7.5, 8.5, 9.5, 10.5, 11.5, 12.5])
#simplearr = np.ascontiguousarray(simplearr, np.float32)

simplearr = np.ascontiguousarray(tr.data, np.float32)

myclib.aicp.restype = C.c_int
myclib.aicp.argtypes = [np.ctypeslib.ndpointer(
                                        dtype=np.float32, ndim=1,
                                        flags='C_CONTIGUOUS'), C.c_int,
                        # OUT
                        np.ctypeslib.ndpointer(
                                        dtype=np.float32, ndim=1,
                                        flags='C_CONTIGUOUS'),
                        C.POINTER(C.c_int)]

pminidx = C.c_int()
aic_cf_arr = np.zeros(simplearr.size - 1, dtype=np.float32, order="C")

ret = myclib.aicp(simplearr, simplearr.size,
                  aic_cf_arr, C.byref(pminidx))
if ret != 0:
    raise MemoryError("Something wrong with AIC picker")
print()
print(ret)
print(pminidx.value)
print(aic_cf_arr)


plt.plot(aic_cf_arr)
plt.show()

print("arrivato")


# ==== To compile at pipinstall stage
# from setuptools import setup, Extension
# from setuptools.command.install import install
# import subprocess
# import os

# class CustomInstall(install):
#     def run(self):
#         command = "git clone https://mygit.com/myAwesomeCLibrary.git"
#         process = subprocess.Popen(command, shell=True, cwd="packageName")
#         process.wait()
#         install.run(self)

# module = Extension('packageName.library',
#                    sources = ['packageName/library.c'],
#                    include_dirs = ['packageName/include'],
#                    extra_compile_args=['-fPIC'])

# setup(
#     name='packageName',
#     version='0.1',
#     packages=['packageName'],
#     install_requires=[
#         ...
#     ],
#     cmdclass={'install': CustomInstall},
#     include_package_data=True,
#     ext_modules=[module],
# )
#
