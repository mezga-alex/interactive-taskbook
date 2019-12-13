from Cython.Distutils import build_ext
from distutils.core import setup
from distutils.extension import Extension
import numpy
import os
os.environ['CC'] = 'g++'
os.environ['CXX'] = 'g++'

ext_modules = [
    Extension(
        name="passive",
        sources=["passive_voice.pyx"],
        extra_compile_args=["-Wno-cpp", "-Wno-unused-function", "-O2", "-march=native", '-stdlib=libc++', '-std=c++11'],
        extra_link_args=["-O2", "-march=native", '-stdlib=libc++'],
        language="c++",
        include_dirs=[numpy.get_include()],
    )
]

setup(
    name="cython-processing", ext_modules=ext_modules, cmdclass={"build_ext": build_ext}
)
