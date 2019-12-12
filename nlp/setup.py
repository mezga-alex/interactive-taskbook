from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy


extensions = [
    Extension("nlp.spaCy.spacy", sources=["./processing/cython_module/passive_voice.pyx"],
              include_dirs=[numpy.get_include()], extra_compile_args=["-O3"], language="c++")
]

setup(
    name="nlp_cython",
    ext_modules = cythonize(extensions),
)