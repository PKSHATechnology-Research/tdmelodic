tdmelodic Documentation
=======================


.. image:: https://github.com/PKSHATechnology-Research/tdmelodic/actions/workflows/docker-image.yml/badge.svg
   :target: https://github.com/PKSHATechnology-Research/tdmelodic/actions/workflows/docker-image.yml
.. image:: https://github.com/PKSHATechnology-Research/tdmelodic/actions/workflows/img.yml/badge.svg
   :target: https://github.com/PKSHATechnology-Research/tdmelodic/actions/workflows/img.yml
.. image:: https://img.shields.io/badge/arXiv-2009.09679-B31B1B.svg
   :target: https://arxiv.org/abs/2009.09679
.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

**Tokyo Dialect MELOdic accent DICtionary**

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
