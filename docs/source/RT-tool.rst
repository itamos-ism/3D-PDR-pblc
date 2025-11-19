The RT-tool Algorithm
=====================

**RT-tool** solves the radiative transfer equation for one-dimensional **3D-PDR** models. You can download the algorithm from this `GitHub link <https://github.com/itamos-ism/RT-tool>`_.

The algorithm can be used with the Python wrapper ``pyRTtool.py``. Refer to the ``HandsOn_RTtool.ipynb`` Jupyter notebook for usage instructions found on GitHub.

Running from Terminal
~~~~~~~~~~~~~~~~~~~~~

After running **3D-PDR**, compile **RT-tool**:

.. code-block:: bash

   cd RT-tool/
   make clean; make
   cd ..

Edit the ``paramsRT.dat`` file:

::

   1) sims
   2) test
   3) 1
   4) 0

* **Entry 1**: PDR output directory
* **Entry 2**: Model prefix
* **Entry 3**: Turbulent velocity (default 1 km/s)
* **Entry 4**: Redshift (to control the CMB temperature)

Run the tool:

.. code-block:: bash

   ./RTtool

Outputs are written to ``sims/`` (where ``PREF`` is the prefix of the model and ``LINE`` the calculated transition line):

* ``Tr_PREF_LINE.dat``: Radiation temperatures for coolant transitions
* ``tau_PREF_LINE.dat``: Optical depths for line transitions

Format of ``Tr_PREF_LINE.dat``::

   Ntot, NH2, Tgas, Ncool, Tr(transitions)

Format of ``tau_PREF_LINE.dat``::

   tau1, tau2, ...

Comparison with RADEX
~~~~~~~~~~~~~~~~~~~~~

`RADEX <https://var.sron.nl/radex/radex.php>`_ (`van der Tak et al., 2007 <https://ui.adsabs.harvard.edu/abs/2007A%26A...468..627V/abstract>`_) is a popular algorithm that solves radiative transfer for given column density, H₂ number density, and gas temperature. Comparison of **RADEX** with **3D-PDR** and **RT-tool** is only valid for:

* Isothermal runs (thermal balance switched off)
* Uniform-density 1D clouds
* No external radiation field

**3D-PDR Setup for Comparison:**

1. Edit ``config.mk``: set ``GUESS_TEMP=0`` and ``THERMALBALANCE=0`` for 1D runs
2. Modify ``params.dat``:

   ::

      2)  1Dn43.dat                  !ICs file
      ...
      4)  radexcomp                  !Output prefix
      5)  0                          !G0 (no FUV)
      6)  1.0E-17                    !Cosmic-ray rate
      ...
      9)  1.0                        !Turbulent velocity
      ...
      23) 30.0                       !Gas temperature
      ...
      33) hco+.dat                   !HCO+ coolant

3. Run ``./3DPDR``

**RT-tool Setup for Comparison:**

1. Edit ``paramsRT.dat`` accordingly 
2. Run ``./RTtool``

**RADEX Setup for Comparison:**

.. The linewidth is given by:

   .. math::
      \Delta V = 2 \sqrt{2 \ln{2}}\sqrt{\frac{k_{\rm B}T_{\rm gas}}{m_{\rm mol}} + v_{\rm turb}^2}

Set the RADEX "escape probability" to ``LVG`` for consistency. 

.. note::
   
   Differences are expected since **3D-PDR** treats the cloud as 1D with depth-dependent level populations, while RADEX uses a 0D approach.
