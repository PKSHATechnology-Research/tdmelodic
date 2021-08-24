tdmelodic Documentation
=======================

| **Tokyo Dialect MELOdic accent DICtionary**

This module generates a large scale accent dictionary of
Japanese (Tokyo dialect) using a neural network based technique.

The objective of this module is to generate a large vocabulary Japanese accent dictionary,
exploiting existing two dictionaries: UniDic and NEologd.
UniDic provides accurate accent information of words, but its vocabulary size is not necessarilly large.
NEologd is a very large Japanese dictionary but it does not provide accent information of words.


.. toctree::
   :maxdepth: 3
   :caption: Background

   pages/introduction.md


.. toctree::
   :maxdepth: 3
   :caption: Prelininary Setting

   pages/docker.md

.. toctree::
   :maxdepth: 3
   :caption: Dictionary Generation

   pages/unidic-dicgen.md
   pages/ipadic-dicgen.md


.. toctree::
   :maxdepth: 3
   :caption: Install tdmelodic on your system

   pages/unidic-usage.md
   pages/ipadic-usage.md

.. toctree::
   :maxdepth: 3
   :caption: One-by-one Manual Inference Mode

   pages/onebyone.md

Citation
--------

For academic use, please cite the following paper.

.. code-block:: bibtex

   @inproceedings{tachibana2020icassp,
      author    = "H. Tachibana and Y. Katayama",
      title     = "Accent Estimation of {Japanese} Words from
                  Their Surfaces and Romanizations
                  for Building Large Vocabulary Accent Dictionaries",
      booktitle = {2020 IEEE International Conference on Acoustics,
                  Speech and Signal Processing (ICASSP)},
      pages     = "8059--8063",
      year      = "2020",
      doi       = "10.1109/ICASSP40776.2020.9054081"
   }

Paper Links: `[IEEE Xplore] <https://ieeexplore.ieee.org/document/9054081>`_, `[arXiv preprint] <https://arxiv.org/abs/2009.09679>`_
