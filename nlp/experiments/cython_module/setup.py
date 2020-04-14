from Cython.Distutils import build_ext
from distutils.core import setup
from distutils.extension import Extension
import numpy
import os
os.environ['CC'] = 'g++'
os.environ['CXX'] = 'g++'

ext_modules = [
    Extension(
        name="passive_voice_cython",
        sources=["passive_voice_cython.pyx"],
        extra_compile_args=["-Wno-cpp", "-Wno-unused-function", "-O2", "-march=native", '-stdlib=libc++', '-std=c++11'],
        extra_link_args=["-O2", "-march=native", '-stdlib=libc++'],
        language="c++",
        include_dirs=[numpy.get_include()],
    )
]

setup(
    name="passive_voice_cython", ext_modules=ext_modules, cmdclass={"build_ext": build_ext}
)


# from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Build import cythonize
# import numpy
#
#
# extensions = [
#     Extension("processing.passive_voice", sources=["passive_voice.pyx"],
#               include_dirs=[numpy.get_include()], extra_compile_args=["-O3"], language="c++")
# ]
#
# setup(
#     name="nlp_cython",
#     ext_modules = cythonize(extensions),
# )


# setup(
#     ext_modules = cythonize("passive_voice.pyx",  include_path=['/usr/include/c++/7/'])
# )

# ext_modules = [
#     Extension("passive_voice", sources=["passive_voice.pyx"],
#               extra_compile_args = ['-g0'],
#             )
# ]
#
# setup(
#     name='passive_voice',
#     # include_package_data=True,
#     # package_data={'': ['*.pyx', '*.pxd', '*.h', '*.c']},
#     # cmdclass = {'build_ext': build_ext},
#     ext_modules=cythonize(ext_modules)
# )
