from distutils.core import setup

setup(
    name='SemanticLabeling',
    version='1.0',
    packages=["semantic_labeling", "semantic_labeling.lib", "semantic_labeling.search",
              "semantic_labeling.main", "semantic_labeling.tests"],
    url='',
    license='',
    author='Minh Pham',
    author_email='minhpham@usc.edu',
    description='Semantic Labeling: A domain-independent approach', install_requires=['scikit-learn', 'numpy', 'pandas',
                                                                                      'elasticsearch', 'scipy',
                                                                                      'pymongo']
)
