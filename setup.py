from distutils.core import setup

setup(
    name='SemanticLabeling',
    version='1.0',
    packages=['semantic_labeling', "semantic_labeling.data_source", "semantic_labeling.machine_learning",
              "semantic_labeling.main", "semantic_labeling.search_engine", "semantic_labeling.utils"],
    url='',
    license='',
    author='Minh Pham',
    author_email='minhpham@usc.edu',
    description='Semantic Labeling: A domain-independent approach', install_requires=['scikit-learn', 'numpy', 'pandas',
                                                                                      'elasticsearch', 'scipy']
)
