from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy



extensions = [
    Extension("nlp.spaCy.spacy", sources=["passive_voice.pyx"],
              include_dirs=[numpy.get_include()], extra_compile_args=["-O3"], language="c++")
]

setup(
    name="nlp_cython",
    ext_modules = cythonize(extensions),
)


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
