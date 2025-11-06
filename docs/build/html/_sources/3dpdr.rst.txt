Upgraded 3D-PDR (2025)
======================

To install 3D-PDR, you will first need to install SUNDIALS (version
7.0.0). You will need ``gfortran`` and ``gcc`` compilers, as well as
``cmake``. Before continuing, create a directory to do all the below
installations, e.g. ``~/PDRmodels/``:

.. code:: console

    $ cd 
    $ mkdir PDRmodels
    $ cd PDRmodels

You can now compile, create initial conditions and run 3D-PDR using the
python wrapper ``py3DPDR.py``. It is strongly recommended that you first
install and run the code in a terminal before you use the python
wrapper. If you have already done that, you can read the `Python
wrapper <#python-wrapper>`__ manual on how to use it.

-  Summary

   -  `Installing ``cmake`` <#installing-cmake>`__
   -  `Installing SUNDIALS 7.0.0 <#sundials>`__
   -  `Installing 3D-PDR <#3DPDR>`__
   -  `The ``makefile`` <#the-makefile>`__
   -  `The ``params.dat`` <#params>`__
   -  `Constructing initial
      conditions <#constructing-initial-conditions>`__
   -  `Changing initial elemental
      abundances <#changing-initial-elemental-abundances>`__
   -  `Including more coolants <#including-more-coolants>`__
   -  `Understanding and plotting the
      outputs <#understanding-and-plotting-the-outputs>`__
   -  `The radiative transfer algorithm
      ``RTtool`` <#the-radiative-transfer-algorithm-rttool>`__

Installing ``cmake``
====================

Check if you have already ``cmake``. If you do, go directly to the next
Section.

Within the ``~/PDRmodels/``, download ``cmake``:

.. code:: console

    $ wget https://github.com/Kitware/CMake/releases/download/v3.23.0/cmake-3.23.0-linux-x86_64.tar.gz

Extract the tarball:

.. code:: console

    $ tar -xzvf cmake-3.23.0-linux-x86_64.tar.gz

Move the extracted directory:

.. code:: console

    $ mv cmake-3.23.0-linux-x86_64 /opt/cmake-3.23.0

Create a symbolic link:

.. code:: console

    $ ln -sf /opt/cmake-3.23.0/bin /usr/bin/

Verify the ``cmake`` version:

.. code:: console

    $ cmake --version

Installing SUNDIALS 7.0.0 
==========================

Clone the Sundials repository:

.. code:: console

    $ git clone https://github.com/LLNL/sundials.git sundials-7.0.0

Create and navigate to the build directory:

.. code:: console

    $ mkdir sundials-7.0.0/build
    $ cd sundials-7.0.0/build

Configure Sundials with ``cmake``:

.. code:: console

    $ cmake -DCMAKE_INSTALL_PREFIX=/YOUR-HOMEPATH/PDRmodels/sundials ../

Build and install SUNDIALS

.. code:: console

    $ make
    $ make install

Edit the ``rc`` file of your shell e.g. ``.bashrc`` in your home
directory and include the following commands

.. code:: console

    export LD_LIBRARY_PATH=/home/tbisbas/data/Codes/3D-PDR_sundials7/sundials/lib
    export SUNDIALS_DIR=/home/tbisbas/data/Codes/3D-PDR_sundials7/sundials

and then either type ``source ~/.bashrc`` or close this terminal and
open a new one. If you use different shell, you will need to adjust the
above commands accordingly.

Installing 3D-PDR 
==================

In the directory ``~/PDRmodels/`` extract the ``3DPDR.tgz``

.. code:: console

    $ cd ~/PDRmodels/
    $ tar xvzf 3DPDR.tgz

Advance in the ``src/`` directory

.. code:: console

    $ cd 3D-PDR-main/src

Compile the code and run a test model
-------------------------------------

To compile the code, you will need to edit the ``config.mk`` and adjust
the ``F90`` (for Fortran) and ``CC`` (for C++) compilers accordingly.
For Mac users: it is possible that the ``makefile`` will fail if you
have ``conda`` activated. It is recommended to type
``conda deactivated`` before compiling 3D-PDR.

You are now ready to compile 3D-PDR for the first time! While still
within the ``src/`` directory, type:

.. code:: console

    $ make

If the ``makefile`` has been executed without issues, you will see the
``3DPDR`` executable in the ``~/PDRmodels/`` directory. You are now
ready to perform the first model. This default model is for benchmarking
purposes only to ensure that installation has been properly done. To run
a model, simply type:

.. code:: console

    $ ./3DPDR

and within just a few seconds (depending on your machine) the test model
will finish. You can check whether the run is successful by plotting the
gas temperature versus visual extinction against the benchmark model
that is already run. With a plotting tool, simply compare columns 3
(visual extinction, first column is 1) and 4 (gas temperature) of the
file ``sims/test.pdr.fin`` (your model) against the same columns of the
``benchmark/model.pdr.fin`` (the benchmarking model). For instance, in
``gnuplot`` the command should be

.. code:: console

    set log
    plot 'sims/test.pdr.fin' u 3:4 w l t 'my model', 'benchmark/model.pdr.fin' u 3:4 w l t 'benchmark'

The ``makefile``
================

The main flags of the code are specified in the ``config.mk`` file. This
is then called in ``makefile``. In ``config.mk``, flags can be divided
in two main sections. The first section are options for the compiler.
The second section are options for the chemistry and the density
distribution.

First section (compiler options)
--------------------------------

.. code:: console

    F90               = gfortran
    CC                = gcc-14
    CPPFLAGS          = -cpp
    SUNDIALS          = 7.0
    OPENMP            = 1
    OPTIMISE          = 3
    PYWRAP            = 0

-  ``F90`` specifies the fortran compiler. The default compiler is
   ``gfortran``. No other Fortran compilers have been tested yet, so
   change this only if you are willing to solve possible bugs yourself.
-  ``CC`` specifies the gcc compiler. For Mac users, check the
   ``gcc-14`` or ``mp-gcc-14`` compilers instead of the ``gcc``. *It is
   strongly recommended to use gcc versions >7.3.0.*
-  ``CPP`` flag is set to ``-cpp``
-  ``SUNDIALS`` should be set to ``7.0``
-  ``OPENMP`` specifies whether the code will run in parallel (flag 1)
   or in serial (flag 0). It is recommended always to use ``OPENMP = 1``
   unless you have a reason.
-  ``OPTIMISE`` specifies the optimisation of the compiler. In general,
   flags 0 and 1 are used for development and debugging purposes. Flags
   2 and 3 are used for running models. It is recommended to have
   ``OPTIMISE = 3`` for running your models. There exists a flag 4, but
   it is not recommended to use as it lowers the precision and the code
   may crash.
-  ``PYWRAP`` should be used for the `python wrapper
   ``py3DPDR.py`` <#python-wrapper>`__

Second section (chemistry options)
----------------------------------

.. code:: console

    DIMENSIONS        = 1
    RAYTHEIA          = 0
    RAYTHEIA_MO       = 0
    XYZ               = 0
    NETWORK           = REDUCED
    XRAYS             = 0
    DUST              = HTT91
    GUESS_TEMP        = 1
    THERMALBALANCE    = 1
    FORCECONVERGENCE  = 1
    GRAINRECOMB       = 0
    SUPRATHERMAL      = 0
    H2FORM            = CT02
    CRATTENUATION     = 0
    RESTART           = 0

-  ``DIMENSIONS`` specifies the density distribution you would like to
   run. If it is an one-dimensional model, set ``DIMENSIONS = 1``. For
   three-dimensional models, set ``DIMENSIONS = 3``.
-  ``RAYTHEIA`` is the new ray-tracing algorithm implemented for
   three-dimensional models in 3D-PDR. It is a self-consisted algorithm
   and performs extremely fast ray-tracing to calculate column
   densities, line emission and escape probability in 3D. Set
   ``RAYTHEIA = 1`` to switch it on (works *only* for
   ``DIMENSIONS = 3``). If you set ``DIMENSIONS = 3`` and
   ``RAYTHEIA = 0``, the code will compile with the original ray-tracing
   method presented in Bisbas+12. The latter is a much slower
   ray-tracing algorithm with a high memory consumption. For
   one-dimensional models, you will always need ``RAYTHEIA = 0``.
-  ``RAYTHEIA_MO`` allows to perform ray-tracing on-the-fly, reducing
   the total RAM consumption. However it increases the CPU runtime by at
   least 30%. This flag is ideal for higher resolution models.
-  ``XYZ`` specifies the format of the 3D density distribution (for
   ``DIMENSIONS = 1`` use ``XYZ = 0`` always). For ``XYZ = 0`` the file
   is created in a xyz format with z changing first. For ``XYZ = 1``,
   the file is created in a xyz format with x changing first. See
   Section "Constructing initial conditions" below for more information.
-  ``NETWORK`` specifies the chemical network of the model based on the
   UMIST database. There are three possibilities in this version: 1)
   ``NETWORK = REDUCED`` consists of 33 species and 331 reactions, 2)
   ``NETWORK = MEDIUM`` consists of 77 species and 1158 reactions
   (written by B. Gaches), 3) ``NETWORK = FULL`` consists of 215 species
   and 2926 reactions. The higher the complexity of the network, the
   slower the code becomes. For 3D runs, a more complex network comes at
   an extra RAM cost.
-  ``XRAYS`` includes X-ray chemistry. This is currently under
   development and works in limited cases only for
   ``NETWORK = REDUCED``. It is not recommended to do X-ray chemistry
   with this version of the code, so use ``XRAYS = 0`` at all times.
-  ``DUST`` specifies the way dust temperature is treated. There are two
   possibilities: 1) ``DUST = HTT91`` using the treatment presented in
   Hollenbach, Takahashi & Tielens (1991) -default flag-, and 2)
   ``DUST = 0`` used if you would like to perform isothermal dust runs.
   If you use ``DUST = 0``, you will need to specify the value of the
   dust temperature in the ``params.dat`` file (see below).
-  ``GUESS_TEMP`` refers to the initial gas temperature the code uses to
   start iterations. For ``GUESS_TEMP = 1`` the code uses an approximate
   function based on the FUV intensity (discussed in Bisbas+ 12). For
   ``GUESS_TEMP = 0`` the code uses a uniform gas temperature throughout
   all cloud. The recommended flag is ``GUESS_TEMP = 1`` as this reduced
   the total number of iterations and minimizes errors.
-  ``THERMALBALANCE`` specifies whether your PDR model will converge due
   to therma balance (``THERMALBALANCE = 1``) *or* if it is a simple
   isothermal model (``THERMALBALANCE = 0``). If the second case is
   selected, you will need to have ``GUESS_TEMP = 0`` as well. The value
   of the gas temperature in isothermal runs is specified in the
   ``params.dat`` file (see below).
-  ``FORCECONVERGENCE`` helps the code to converge fast by restricting
   the change of values after a number of iterations. It is recommended
   to have ``FORCECONVERGENCE = 1`` at all times, unless you know what
   you do (so setting it to 0).
-  ``GRAINRECOMB`` switches on (``GRAINRECOMB = 1``) the routine to
   consider electron recombination on dust grains (see Weingartner &
   Draine 2001, ApJ, 563, 842). For ``GRAINRECOMB = 0`` the routine is
   switched off. There are some known issues (not fixed) when using this
   flag for the FULL chemical network.
-  ``SUPRATHERMAL`` switches on (``SUPRATHERMAL = 1``) the suprathermal
   formation of CO via CH+ (see Visser+ 09; Bisbas+ 19). The values of
   Av critical (at which this formation pathway ceases to be important)
   and the Alfven velocity are specified in the ``params.dat`` file (see
   below).
-  ``H2FORM`` specifies the H2 formation recipe. There are three flags
   available: 1) ``H2FORM = CT02`` for the Cazaux & Tielens (2002, 2004)
   treatment, 2) ``H2FORM = SIMPLE`` for a simpler function (see
   ``makefile`` comments), and 3) ``H2FORM = R07`` for the H2 formation
   function used in the Roellig+ (2007) benchmarking paper.
-  ``CRATTENUATION`` calculates attenuation of cosmic-rays (both for
   ``DIMENSIONS = 1`` and ``3``). There are two options available. For
   ``CRATTENUATION=1``, the user can use the L and H models of Padovani
   et al (2018). For ``CRATTENUATION = 1``, you will need to replace the
   cosmic-ray ionizaion rate value in the ``params.dat`` by either
   ``L``, ``l`` (for the Low model) or ``H``, ``h`` (for the High
   model). For ``CRATTENUATION=2``, the use can use a softened power-law
   attenuation curve which takes the form
   ``zeta(N) = zeta0 * (1 + N/N0)**alpha``. There are three parameters
   used for this model, replacing the CRIR, in line order ``zeta0``,
   ``N0``, ``alpha``. For ``CRATTENUATION = 0``, you simply specify the
   value of the CR ionization rate which is treated as a constant value
   for all depth points.
-  ``RESTART`` allows to continue an interrupted model
   (``RESTART = 1``). This is particularly useful for large 3D models
   rather than 1D. The default value is ``RESTART = 0`` (switched off).
   Once activated, ``RESTART`` writes the file ``restart.bin`` in binary
   format in the directory where ``3DPDR`` is executed. If you are lucky
   enough for your model to stop due to external factors (power cut,
   exceed of wall time), you can simply re-run it without any further
   change. IMPORTANT: for any completely new model, you *must* delete
   ``restart.bin`` if it already exists from your previous run. The
   ``RESTART`` function operates only for ``THERMALBALANCE = 1``.

The ``params.dat`` 
===================

In the ``params.dat`` file the user specifies the input-output prefixes,
the PDR environmental parameters, thermal balance options, coolants and
other technical parameters. Below, the default parameters are explained.
The user is free to change those for their PDR models.

Users can also define their own parameter file, i.e. ``paramsUser.dat``,
which can be passed to 3DPDR using command line options ``-p=`` or
``--params``. For example, to use this parameter file, one would call
3DPDR as ``./3DPDR -p=paramsUser.dat``. The parameter file name can only
be 50 characters long.

Input/Output - Densities
------------------------

.. code:: console

    ===========================|-------------------------
    Input/Output - Densities   |    ~~~ COMMENTS ~~~
    ===========================|-------------------------
    ics                        !ICs directory
    1Dn30.dat                  !ICs file
    sims                       !Output directory
    test                       !Output prefix

-  ``ics`` is the directory of the initial conditions. All density
   distributions are included in that directory. See below how to
   construct 1D and 3D data.
-  ``1Dn30.dat`` is the input file for the 1D density distribution. This
   particular file is a uniform density cloud with n=1e3 cm-3 and a
   visual extinction of Av=10mag. It has been constructed with 30 points
   per Av dex.
-  ``sims`` is the output directory of the models.
-  ``test`` is the prefix of the default PDR model. After running the
   code, there will be various files of that prefix saved in ``sims/``
   e.g. ``sims/test.pdr.fin``.

PDR parameters
--------------

.. code:: console

    ===========================|
    PDR parameters             |
    ===========================|
    10                         !G0 (in Draine field units) -x to +x in 1D
    1.0E-16                    !Cosmic-ray ionization rate (s^-1)
    0.0                        !Xray flux (erg/cm2/s)
    1.0                        !Dust-to-gas normalized to 1e-2
    1.0                        !Turbulent velocity (km/s)
    1e7                        !End time (yr)
    1.0E-5                     !Grain radius (cm)
    6.289e-22                  !Av conversion factor
    3.02                       !UV factor
    0                          !Redshift (for CMB temperature)
    0.7                        !Av critical (SUPRATHERMAL switch)
    3.3                        !Alfven velocity (km/s) (SUPRATHERMAl switch)

-  ``10`` is the intensity of the FUV radiation field normalized to the
   spectral shape of Draine (1978). For ``DIMENSIONS = 1``, this is an
   one-sided radiation field. For ``DIMENSIONS = 3``, this corresponds
   to the intensity of an isotropic radiation field. For the 12-ray
   HEALPix structure, this means that for each ray an intensity field of
   10/12 is calculated, so that the total intensity of the cell assuming
   no attenuation is 10.
-  ``1.0E-16`` is the value of the cosmic-ray ionization rate (in s-1).
   In this version, the cosmic-ray ionization rate is fixed everywhere
   in the cloud.
-  ``0.0`` is the X-ray flux (in erg/cm2/s) for X-ray models. It is
   recommended not to change this value in this version.
-  ``1.0`` is the dust-to-gas ratio normalized to 1e-2. There is no
   ``metallicity`` parameter in this version. For metallicities other
   than the solar (default), the user must change this value *and*
   specify the elemental abundances separately (see below).
-  ``1.0`` is the microtubulent velocity (in km/s) controlling the
   turbulent heating.
-  ``1e7`` is the end chemical time (in yr). It is set to 10Myr to
   ensure that chemical balance has been reached. The user can change
   this for more advanced studies concerning young clouds.
-  ``1.0E-05`` is the assumed grain radius (in cm).
-  ``6.289e-22`` is the visual extinction conversion factor (taken from
   the Roellig+07 benchmarking paper).
-  ``3.02`` is a factor used for the attenuation of the UV radiation
   (taken from the Roellig+07 benchmarking paper).
-  ``0`` is the redshift. This value controls the CMB temperature
-  ``0.7`` is the critical Av for the ``SUPRATHERMAL = 1`` switch. This
   is the value of the Av above which the suprathermal formation of CO
   via CH+ ceases to be important. If the code is compiled with
   ``SUPRATHERMAL = 0``, this value is not accounted for.
-  ``3.3`` is the Alfven velocity (in km/s) for the ``SUPRATHERMAL = 1``
   switch. If the code is compiled with ``SUPRATHERMAL = 0``, this value
   is not accounted for.

Using the softened-power-law cosmic ray attenuation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If using the softened-power-law cosmic ray attenuation, the first lines
of the params file would be formatted such as this

::

    ===========================|
    PDR parameters             |
    ===========================|
    10                         !G0 (in Draine field units) -x to +x in 1D
    1.0E-16                    !Surface cosmic-ray ionization rate, zeta0 (s^-1)
    1.0E21                     !Normalizing column density, N0
    -1.0                       !Attenuation slope, alpha
    .... continued as normal

Ray-tracing, ODE Solver, Chemistry iteration parameters
-------------------------------------------------------

.. code:: console

    ===========================|
    Ray-tracing parameters     |
    ===========================|
    0                          !HEALPix level of refinement
    1.3                        !Theta critical (0<phi<pi/2)
    ===========================|
    ODE Solver parameters      |
    ===========================|
    1.0D-8                     !relative abundance tolerance
    1.0D-30                    !absolute abundance tolerance
    ===========================|
    Chemistry iterations       |
    ===========================|
    8                          !First set of Chemical Iterations
    6000                       !Total iterations

It is recommended not to change the values of these sections, unless you
know what you are doing.

Thermal balance values
----------------------

.. code:: console

    ===========================|
    Thermal balance values     |
    ===========================|
    40.0                       !Gas temperature for isothermal models
    10.0                       !Floor temperature (if <Tcmb it's set to Tcmb)
    30000.0                    !Maximum allowed gas temperature
    20.0                       !Dust temperature for isothermal dust models
    0.005                      !Fcrit (% Accuracy)
    0.01                       !Tdiff (maximum temperature difference)

-  ``40.0`` is the gas temperature used in isothermal models (for which
   you need to set ``THERMALBALANCE = 0`` and ``GUESS_TEMP = 0`` in the
   ``makefile``)
-  ``10.0`` is the floor gas temperature below which the code does not
   allow the gas to cool further. If the floor temperature is below the
   CMB temperature (at any given redshift), the code will automatically
   select the CMB temperature as the floor.
-  ``30000.0`` maximum allowed gas temperature in the PDR model. It is
   recommended not to change this value.
-  ``20.0`` is the dust temperature used in isothermal dust models (for
   which ``DUST = 0`` in the ``makefile``)
-  ``0.005`` controls the thermal balance accuracy. Change this value
   only if you know what you are doing.
-  ``0.01`` is the maximum temperature diffence used in thermal balance
   iterations to control the accuracy. Change this value only if you
   know what you are doing.

Coolant files
-------------

.. code:: console

    ===========================|
    Coolant files              |Leiden Lambda format
    ===========================|
    12co.dat                   !CO Do not change the following order
    12c+.dat                   !CII
    12c.dat                    !CI
    16o.dat                    !OI

The default list of coolants is as shown above. The user is recommended
*not* to change this order. It is possible to include additional
coolants, depending on the chemical network used in the ``makefile``. To
do that, simply add the file(s) of the coolant(s) at the end of the
``params.dat`` file, below ``16o.dat``. The more coolants included, the
slower becomes the code. See relevant section below how to include more
coolants.

Constructing initial conditions
===============================

To run a PDR model, you will need to construct the density distribution
of the cloud. Once you create an initial conditions file, you can store
it in the ``ics/`` directory for future use (no need to create initial
conditions per PDR model). In the ``ics/`` directory, there are two
files that will help you with this depending on the model you want to
run. These are fortran files, however you can create your own density
function with your own tools, as long as the input format is respected.

One-dimensional density functions
---------------------------------

The input format in one-dimensional runs is:

.. code:: console

    x(pc), y(pc), z(pc), nH(cm-3)

with ``y = 0.0`` and ``z = 0.0`` set always. The spatial distribution is
measured in units of pc, and the total H-nucleus number density in the
fourth column in units of cm-3.

For simple one-dimensional distributions, you can use the
``uniform1D.f90`` file. You will need to compile it using the following
command

.. code:: console

    $ gfortran -o uniform1D uniform1D.f90

and run it with ``./uniform1D`` (within the ``ics/`` directory). This is
a simple and interactive algorithm that creates the uniform-density
distribution. Below there is an example when you run it:

.. code:: console

     give number density [cm^-3] (e.g. 1000)
    1000
     give avmax (e.g. 10)
    10
     length [pc] =    5.15322113    
     give log10(avmin) (e.g. -3)
    -3
     give x-resolution (e.g. 30)
    30
     file [outgrid.dat] written!

This will create the ``outgrid.dat`` containing a cloud with density of
1000 cm-3, a maximum visual extinction of 10mag, a minimum visual
extinction of 1e-3 (for resolving the HI-to-H2 transition) with 30
points per Av dex. So the total number of points for this model is 122
(including the first and last point). You can rename the ``outgrid.dat``
e.g. ``1Dn30.dat``.

Three-dimensional density distributions
---------------------------------------

In the current version of 3D-PDR, ray-tracing is performed for a uniform
grid of cells, the resolution of which must be a power of 2 e.g. 32^3,
64^3, 128^3 etc. In principle, to run a 3D model you will need a density
distribution generated by a hydrodynamical code, or a 3D density
distribution function. However, to understand how such a file can be
used in the code, you can experiment with the ``build3D.f90`` routine.
This file is meant to be used as a guide to build your own 3D cloud. In
its default version, it simply generates a sphere within a 32^3 box. The
sphere has a radius of 5 pc, a density of 1000 cm-3 and it is within a
box containing 32^3 cells. Each side of the box is 10pc. Cells that are
not included withing the spherical radius of 5pc have a density of 0
cm-3.

The format of the 3D density file is similar to that of the 1D models
described above. However, in the 3D case there is a header of two lines
at the start of the file e.g.

.. code:: console

    32 32 32
    10. 10. 10.

which give the number of cells in each side (integer number) as well as
the physical size of the box (in pc).

IMPORTANT: the box must start at (0,0,0) and expand along all positive
x,y,z axes. For instance, if you cut a density distribution from a
hydrodynamical model containing negative positions, you must shift the
cloud to have positive coordinates starting at (0,0,0). Each x,y,z
position in the initial conditions file represents the *centroid* of the
cell (not its corners).

When building a 3D cloud, you will need to make sure that the ``XYZ``
flag in the ``makefile`` follows the input format. Assuming that
nH(i,j,k) is a given density function, for ``XYZ = 0``, the file is
created in a xyz format with z changing first e.g.

.. code:: console

    do i = 1, itot
      do j = 1, itot
         do k = 1, itot
            write(1,*) x(i), y(j), z(k), nH(i,j,k)
         end do
      end do
    end do

For ``XYZ = 1``, the file is created in a xyz format with x changing
first e.g.

.. code:: console

    do k = 1, itot
      do j = 1, itot
         do i = 1, itot
            write(1,*) x(i), y(j), z(k), nH(i,j,k)
         end do
      end do
    end do

There are two 3D files that come with the code to experiment the
capabilities of 3D-PDR in modelling such structures. The first one is
the ``3Dsphere.dat`` at 32^3 resoltuion. The second one is called
``diffuse_64.dat'. It has a resolution of 64^3 and it is a sub-region from an MHD run (Wu+ 17; Bisbas+ 21) representing the diffuse ISM. Both these files have a``\ XYZ
= 0\` format. To run the 64^3 with the REDUCED network, your machine
must contain at least 16GB of RAM, otherwise you may experiment with the
32^3 model.

Changing initial elemental abundances
=====================================

To change the initial elemental abundances, you will need to edit the
``species_NETWORK.d`` file found in the ``chemfiles/`` directory,
according to the chemical network you use. You do not need to re-compile
3D-PDR in case the only change you do is this.

Including more coolants
=======================

Adding a particular coolant is important if we are interested in
studying its emission. For all coolants included, 3D-PDR outputs the
level populations of all transitions which are then used in the
``RTtool`` to estimate the radiation temperature along the
line-of-sight.

It is now very simple to include coolants, in addition to the default
ones of 12CO, C+, C, and 16O. In the ``chemfiles/`` you may identify the
coolants you can add. To add them, you will need to ensure that the
chemical network you use does contain the coolant of interest, and then
add its filename at the end of the ``params.dat`` file. And that's it!
If you are using the same chemical network, it is not necessary to
re-compile the code if you add a new coolant in the ``params.dat``.

In case you would like to add a coolant that is not listed in the
``chemfiles/`` directory, you will need to download it from the LEIDEN
LAMBDA database (or to construct your own following the LEIDEN LAMBDA
format), and then make sure that the header of the file is modified as
follows (here an example of the 16O as downloaded from the database, and
after the changes needed):

-  File directly from LEIDEN LAMBDA:

   .. code:: console

       !MOLECULE
       O (neutral atom)
       !MOLECULAR WEIGHT
       16.0
       !NUMBER OF ENERGY LEVELS
       5

-  File after changes (as is in ``chemfiles/``):

   .. code:: console

       !MOLECULE
       O           <--- comments removed. Name of species as in species_NETWORK.d
       !MOLECULAR WEIGHT
       16.0
       !NUMBER OF ENERGY LEVELS
       5 27        <--- the maximum number of "COLL TEMPS" added (search for it within the file) 

   IMPORTANT: The current version of 3D-PDR cannot handle hyper-fine
   structures, so do not include a cooling file containing hfs.

Then you need to add the cooling filename at the end of the
``params.dat``. For instance, to include cooling due to HCO+ and
therefore study its emission, you will need to add:

.. code:: console

    12co.dat                   !CO Do not change the following order
    12c+.dat                   !CII
    12c.dat                    !CI
    16o.dat                    !OI
    hco+.dat    <--- this one!

at the end of the ``params.dat``. It is possible to add as many coolants
as you like.

Understanding and plotting the outputs
======================================

The outputs are written in the ``sims/`` directory, unless the user has
specified another one. The outputs are written once the code has been
fully converged and finished. The code produces outputs with different
suffixes according to i) abundances of species (``pdr.fin``), ii) line
emission (``.line.fin``), iii) cooling functions (``.cool.fin``), iv)
heating functions (``.heat.fin``), v) level populations of each coolant
(``.COOL.spop.fin``) where ``COOL`` is the coolant name. There is also
the possibility to output the chemical reactions that take place in each
point (currently developing it). Currently the outputs are in ASCII
format and they are ready to be plotted using standard tools such as
GNUPLOT or PYTHON.

One-dimensional outputs
-----------------------

``OUTPUT.pdr.fin``:
~~~~~~~~~~~~~~~~~~~

+----------+---------+---------------------------------+
| Column   | Value   | Comments                        |
+==========+=========+=================================+
| 1        | ID      | Identity of cell (integer)      |
+----------+---------+---------------------------------+
| 2        | x       | Position (pc)                   |
+----------+---------+---------------------------------+
| 3        | Av      | Visual extinction (mag)         |
+----------+---------+---------------------------------+
| 4        | Tgas    | Gas temperature (K)             |
+----------+---------+---------------------------------+
| 5        | Tdust   | Dust temperature (K)            |
+----------+---------+---------------------------------+
| 6        | etype   | Type of cell (integer)          |
+----------+---------+---------------------------------+
| 7        | nH      | Number density of cell (cm-3)   |
+----------+---------+---------------------------------+
| 8        | UV      | Intensity of FUV (Draine)       |
+----------+---------+---------------------------------+
| 9-...    | ...     | Abundances of species           |
+----------+---------+---------------------------------+

The abundances of species follow the ``species_NETWORK.d`` sequence

``OUTPUT.cool.fin``:
~~~~~~~~~~~~~~~~~~~~

+-----------+---------+-------------------------------------------+
| Columns   | Value   | Comments                                  |
+===========+=========+===========================================+
| 1         | ID      | Identity of cell (integer)                |
+-----------+---------+-------------------------------------------+
| 2         | x       | Position (pc)                             |
+-----------+---------+-------------------------------------------+
| 3         | Av      | Visual extinction (mag)                   |
+-----------+---------+-------------------------------------------+
| 4         | CO      | CO cooling function                       |
+-----------+---------+-------------------------------------------+
| 5         | C+      | C+ cooling function                       |
+-----------+---------+-------------------------------------------+
| 6         | C       | C cooling function                        |
+-----------+---------+-------------------------------------------+
| 7         | O       | O cooling function                        |
+-----------+---------+-------------------------------------------+
| 8-...     | ...     | Cooling function of additional coolants   |
+-----------+---------+-------------------------------------------+
| Last      | Total   | Total cooling (sum of all)                |
+-----------+---------+-------------------------------------------+

The sequence of coolants is the same as in the ``params.dat``. If no
additional coolants are inserted, the ``total`` cooling function is
column 8.

``OUTPUT.heat.fin``:
~~~~~~~~~~~~~~~~~~~~

+-----------+---------+------------------------------+
| Columns   | Value   | Comments                     |
+===========+=========+==============================+
| 1         | ID      | Identity of cell (integer)   |
+-----------+---------+------------------------------+
| 2         | x       | Position (pc)                |
+-----------+---------+------------------------------+
| 3         | Av      | Visual extinction (mag)      |
+-----------+---------+------------------------------+
| 4         | HR01    | Not contributing             |
+-----------+---------+------------------------------+
| 5         | HR02    | Photoelectric                |
+-----------+---------+------------------------------+
| 6         | HR03    | Not contributing             |
+-----------+---------+------------------------------+
| 7         | HR04    | Carbon ionization            |
+-----------+---------+------------------------------+
| 8         | HR05    | H2 formation                 |
+-----------+---------+------------------------------+
| 9         | HR06    | H2 photodissociation         |
+-----------+---------+------------------------------+
| 10        | HR07    | FUV pumping                  |
+-----------+---------+------------------------------+
| 11        | HR08    | Cosmic-rays                  |
+-----------+---------+------------------------------+
| 12        | HR09    | Turbulent                    |
+-----------+---------+------------------------------+
| 13        | HR10    | Chemical                     |
+-----------+---------+------------------------------+
| 14        | HR11    | Gas-grain                    |
+-----------+---------+------------------------------+
| 15        | HR12    | Total (sum of all)           |
+-----------+---------+------------------------------+

Three-dimensional outputs
-------------------------

Three dimensional outputs follow a similar sequence to the above. New
routines to handle these are currently implemented, however you can
explore the ``pdr.fin`` output as follows:

+------------------+---------+-----------------------------------------+
| Column           | Value   | Comments                                |
+==================+=========+=========================================+
| 1                | ID      | Identity of cell (integer)              |
+------------------+---------+-----------------------------------------+
| 2                | x       | x position (pc)                         |
+------------------+---------+-----------------------------------------+
| 3                | y       | y position (pc)                         |
+------------------+---------+-----------------------------------------+
| 4                | z       | z position (pc)                         |
+------------------+---------+-----------------------------------------+
| 5                | Tgas    | Gas temperature (K)                     |
+------------------+---------+-----------------------------------------+
| 6                | Tdust   | Dust temperature (K)                    |
+------------------+---------+-----------------------------------------+
| 7                | etype   | Type of cell (integer)                  |
+------------------+---------+-----------------------------------------+
| 8                | nH      | Number density of cell (cm-3)           |
+------------------+---------+-----------------------------------------+
| 9                | UV      | Intensity of FUV (Draine)               |
+------------------+---------+-----------------------------------------+
| 10-10+species    | ...     | Abundances of species                   |
+------------------+---------+-----------------------------------------+
| 11+species-...   | Av      | Visual extinction of each HEALPix ray   |
+------------------+---------+-----------------------------------------+

You can use the ``columndensities3D.f90`` interactive algorithm to
project your 3D model and calculate the column density of species.

The radiative transfer algorithm RTtool
=======================================

The source code of this algorithm is in ``RadiativeTransfer/``
directory. Advance to this directory and ``make`` the code. As with
3D-PDR, the executable ``RTtool`` will be moved to the main directory
``~/PDRmodels/``. This algorithm reads the ``.RTspop.fin`` and the
``.pdr.fin`` outputs from the ``sims/`` directory and solves the
radiative transfer equation along the line of sight. The outputs are
on-screen and they follow the ``RADEX`` format to ease the reader
familiar with that algorithm. The integration is done for the entire
cloud.

The ``paramsRT.dat``
--------------------

This is very simple parameters file specifying the details for the input
model:

.. code:: console

    sims                    !Directory of PDR output
    test                    !Model prefix
    1                       !Vturb (km/s)

-  ``sims`` is the directory of the PDR output. If you have saved your
   model in a different directory, you will need to change the name
   here, too.
-  ``test`` is the model prefix you used (default name)
-  ``1`` is the macroturbulent velocity (in km/s) which is used to
   calculate the linewidth.

The output ``RT_[PDR-prefix].dat``
----------------------------------

Currently, ``RTtool`` writes out the first transition of each coolant as
a function of the total column density. In future versions the plan is
to output all quantities for the user to explore how i) the excitation
temperature, ii) the optical depth and iii) the radiation temperature
increase as a function of the total column density and/or the column
density of the coolant.

The output in this version is called ``RT_[prefix-of-PDR-model].dat``,
saved in the main directory ``~/PDRmodels/``. The columns are:

+----------+--------------+--------------------------------------------+
| Column   | Value        | Comments                                   |
+==========+==============+============================================+
| 1        | Ntot         | Total column density (cm-2)                |
+----------+--------------+--------------------------------------------+
| 2        | Tr CO(1-0)   | Radiation temperature of CO(1-0) (K)       |
+----------+--------------+--------------------------------------------+
| 3        | Tr CII       | Radiation temperature of CII 158um (K)     |
+----------+--------------+--------------------------------------------+
| 4        | Tr CI        | Radiation temperature of CI(1-0) (K)       |
+----------+--------------+--------------------------------------------+
| 5        | Tr OI        | Radiation temperature of OI 63um (K)       |
+----------+--------------+--------------------------------------------+
| 6...     | Tr X         | Radiation temperatures of added coolants   |
+----------+--------------+--------------------------------------------+

The ``py3DPDR`` python wrapper 
===============================

-  Summary
-  ```pdr.makefile()`` <#pdrmakefile>`__
-  ```pdr.ics()`` <#pdrics>`__
-  ```pdr.species()`` <#pdrspecies>`__
-  ```pdr.params()`` <#pdrparams>`__
-  ```pdr.run3DPDR()`` <#pdrrun3DPDR>`__
-  ```pdr.plot()`` <#pdrplot>`__

``py3DPDR.py`` is a python wrapper of the 3D-PDR code to facilitate its
use for simple one-dimensional models. Using this wrapper the user can
create one-dimensional uniform density clouds as initial conditions,
compile the code, change the parameters of the model, change the initial
elemental abundances, run the code, and plot the simulation results.

Import the wrapper:

.. code:: python

    import py3DPDR as pdr

Compile the 3D-PDR code: ``pdr.makefile()``\ 
---------------------------------------------

To compile 3D-PDR, use the ``pdr.makefile()``. Here you can specify the
flags to compile the code, as discussed in the `makefile
section <#the-makefile>`__. If a flag is not specified, the code will
compile with the default flags. The default flags are as follows:

+--------------------+--------------------------------+
| Flag               | Default value                  |
+====================+================================+
| F90                | gfortran                       |
+--------------------+--------------------------------+
| CC                 | gcc                            |
+--------------------+--------------------------------+
| CPPFLAGS           | -cpp                           |
+--------------------+--------------------------------+
| SUNDIALS           | 7.0                            |
+--------------------+--------------------------------+
| OPENMP             | 1                              |
+--------------------+--------------------------------+
| OPTIMISE           | 3                              |
+--------------------+--------------------------------+
| PYWRAP             | 1                              |
+--------------------+--------------------------------+
| DIMENSIONS         | 1 (do not change in py3DPDR)   |
+--------------------+--------------------------------+
| RAYTHEIA           | 0 (do not change in py3DPDR)   |
+--------------------+--------------------------------+
| RAYTHEIA\_MO       | 0 (do not change in py3DPDR)   |
+--------------------+--------------------------------+
| XYZ                | 0 (do not change in py3DPDR)   |
+--------------------+--------------------------------+
| NETWORK            | REDUCED                        |
+--------------------+--------------------------------+
| XRAYS              | 0                              |
+--------------------+--------------------------------+
| DUST               | HTT91                          |
+--------------------+--------------------------------+
| GUESS\_TEMP        | 1                              |
+--------------------+--------------------------------+
| THERMALBALANCE     | 1                              |
+--------------------+--------------------------------+
| FORCECONVERGENCE   | 1                              |
+--------------------+--------------------------------+
| GRAINRECOMB        | 0                              |
+--------------------+--------------------------------+
| SUPRATHERMAL       | 0                              |
+--------------------+--------------------------------+
| H2FORM             | CT02                           |
+--------------------+--------------------------------+
| CRATTENUATION      | 0                              |
+--------------------+--------------------------------+
| RESTART            | 0                              |
+--------------------+--------------------------------+

The code will not compile under ``PYWRAP=1`` and ``DIMENSIONS=3``
conditions. The purpose of this wrapper is to simplify the use of 3D-PDR
in one-dimensional models only.

Examples
~~~~~~~~

The command

.. code:: python

    pdr.makefile(CC='gcc-14')

will compile the C part of the code using ``gcc-14`` (e.g. for Mac
users).

The command

.. code:: python

    pdr.makefile(GRAINRECOMB=1, SUPRATHERMAL=1)

will compile the code with all above flags but the ``GRAINRECOMB`` flag
will change to ``1`` (switches on the electron recombination on dust
grains) and the ``SUPRATHERMAL`` flag will also change to ``1``
(switches on the suprathermal formation of CO via CH+)

Create initial conditions: ``pdr.ics()``\ 
------------------------------------------

``py3DPDR`` comes with the ``pdr.ics()`` function that allows to make
initial conditions for one-dimensional PDR models. The initial
conditions include uniform density clouds, the density, size, and
resolution of which are defined by the user. The list of arguments is as
follows:

+--------------+---------------+---------------------------+
| Variable     | Default       | Comments                  |
+==============+===============+===========================+
| nH           | 1000          | Density of cloud (cm-3)   |
+--------------+---------------+---------------------------+
| Avmax        | 10            | Maximum Av (mag)          |
+--------------+---------------+---------------------------+
| Avmin        | 1e-3          | Minimum Av (mag)          |
+--------------+---------------+---------------------------+
| resolution   | 30            | Resolution per Av dex     |
+--------------+---------------+---------------------------+
| avfac        | 6.289e-22     | Av factor (mag cm2)       |
+--------------+---------------+---------------------------+
| directory    | ics/          | Output directory          |
+--------------+---------------+---------------------------+
| filename     | outgrid.dat   | Output filename           |
+--------------+---------------+---------------------------+

If ``pdr.ics()`` is executed, with the above default values the function
creates a 1D uniform density cloud of n=1e3 cm-3, with a minimum Av of
1e-3 mag, a maximum Av of 10 mag, a resolution of 30 points per Av dex
(therefore from 1e-3 to 1e-2 there are 30 points logarithmically
distributed, similarly from 1e-2 to 1e-1 etc.), using an Av factor of
6.289e-22 mag cm2 that converts the total H-nucleus column density to
visual extinction. The output is written in the "ics/" directory and it
is called "outgrid.dat". If you want to save the file in a different
directory, make sure the directory exists before ``pdr.ics()`` is
executed.

Example
~~~~~~~

The command

.. code:: python

    pdr.ics(nH=2500, Avmax=20, resolution=40, filename='mymodel.dat')

creates a cloud with n=2500 cm-3 density, maximum Av of 20 mag and a
higher resolution of 40 points per Av dex. All other values are
equivalent to the above default values. The output "mymodel.dat" is
written in the default "ics/" directory. This should be the input
filename (``icsfile``) in the ``params.dat`` file to use it in the model
(`see below <#pdrparams>`__).

Specify the initial chemical abundances: ``pdr.species()``\ 
------------------------------------------------------------

With the function ``pdr.species()`` the user can specify the initial
abundances for the given network. The ``network`` variable is always
needed to execute the function. The available variables are ``REDUCED``,
``MEDIUM`` or ``FULL`` for the three available chemical networks. The
default initial elemental abundances are those listed in Asplund+2009
paper, with the exception of oxygen (3e-4) and carbon (1.4e-4)
abundances which are the local ISM depleted ones. The following table
shows the variables and the default values.

+------------+------------+------------+
| Variable   | Default    | Comments   |
+============+============+============+
| Mg\_plus   | 2.70E-07   | Mg+        |
+------------+------------+------------+
| C\_plus    | 1.40E-04   | C+         |
+------------+------------+------------+
| He         | 1.00E-01   | He         |
+------------+------------+------------+
| O          | 3.00E-04   | O          |
+------------+------------+------------+
| H2         | 3.00E-01   | H2         |
+------------+------------+------------+
| H          | 4.00E-01   | H          |
+------------+------------+------------+
| N\_plus    | 6.76E-05   | N+         |
+------------+------------+------------+
| Na\_plus   | 1.73E-06   | Na+        |
+------------+------------+------------+
| F\_plus    | 3.63E-08   | F+         |
+------------+------------+------------+
| P\_plus    | 2.57E-07   | P+         |
+------------+------------+------------+
| S\_plus    | 1.32E-05   | S+         |
+------------+------------+------------+
| Fe\_plus   | 3.16E-05   | Fe+        |
+------------+------------+------------+
| Si\_plus   | 3.23E-05   | Si+        |
+------------+------------+------------+
| Cl\_plus   | 3.16E-07   | Cl+        |
+------------+------------+------------+

Example
~~~~~~~

The command

.. code:: python

    pdr.species(network='REDUCED', C_plus=1.40E-05, O=3.00E-05, Mg_plus=0)

creates the ``species_reduced.d`` file in the ``chemfiles/`` directory
and sets C+=1.4e-5, O=3e-5, Mg=0 and all other species of the REDUCED
network to the default values.

Prepare the params.dat file: ``pdr.params()``\ 
-----------------------------------------------

You can specify all parameters of the PDR model from the
``pdr.params()`` function. The default values are as follows:

+------------------+-------------+----------------------------------------------+
| Variable         | Default     | Comments                                     |
+==================+=============+==============================================+
|                  |             | *Input/Output - Densities*                   |
+------------------+-------------+----------------------------------------------+
| icsdir           | ics         | Directory of initial conditions              |
+------------------+-------------+----------------------------------------------+
| icsfile          | 1Dn30.dat   | Initial conditions input filename            |
+------------------+-------------+----------------------------------------------+
| outdir           | sims        | Output directory                             |
+------------------+-------------+----------------------------------------------+
| prefix           | model       | Output prefix                                |
+------------------+-------------+----------------------------------------------+
|                  |             | *PDR parameters*                             |
+------------------+-------------+----------------------------------------------+
| fuv              | 1           | Intensity of FUV radiation (Draine)          |
+------------------+-------------+----------------------------------------------+
| zcr              | 1.0E-17     | Cosmic-ray ionization rate (s-1)             |
+------------------+-------------+----------------------------------------------+
| xrays            | 0.0         | X-ray flux (erg/cm2/s)                       |
+------------------+-------------+----------------------------------------------+
| d2g              | 1.0         | Dust-to-gas normalized to 1e-2               |
+------------------+-------------+----------------------------------------------+
| vturb            | 1.0         | Microturbulent velocity (km/s)               |
+------------------+-------------+----------------------------------------------+
| tend             | 1e7         | End chemical time (yr)                       |
+------------------+-------------+----------------------------------------------+
| grainrad         | 1.0E-5      | Grain radius (cm)                            |
+------------------+-------------+----------------------------------------------+
| avfac            | 6.289e-22   | Av factor converting Ntot to Av              |
+------------------+-------------+----------------------------------------------+
| uvfac            | 3.02        | UV factor for FUV attenuation                |
+------------------+-------------+----------------------------------------------+
| redshift         | 0           | Redshift (controls Tcmb value)               |
+------------------+-------------+----------------------------------------------+
| av\_crit         | 0.7         | Critical Av (for SUPRATHERMAL=1)             |
+------------------+-------------+----------------------------------------------+
| v\_alfv          | 3.3         | Alfven velocity (km/s for SUPRATHERMAL=1)    |
+------------------+-------------+----------------------------------------------+
|                  |             | *Ray-tracing parameters*                     |
+------------------+-------------+----------------------------------------------+
| healpix\_level   | 0           | Healpix level of refinment (DIMENSIONS=3)    |
+------------------+-------------+----------------------------------------------+
| theta\_crit      | 1.3         | Theta\_critical (DIMENSIONS=3, RAYTHEIA=0)   |
+------------------+-------------+----------------------------------------------+
|                  |             | *ODE Solver parameters*                      |
+------------------+-------------+----------------------------------------------+
| rel\_tol         | 1.0E-8      | Relative tolerance parameter                 |
+------------------+-------------+----------------------------------------------+
| abs\_tol         | 1.0E-30     | Absolute tolerance parameter                 |
+------------------+-------------+----------------------------------------------+
|                  |             | *Chemistry iterations*                       |
+------------------+-------------+----------------------------------------------+
| init\_iter       | 8           | Initial chemical iterations                  |
+------------------+-------------+----------------------------------------------+
| max\_iter        | 6000        | Maximum iterations over thermal balance      |
+------------------+-------------+----------------------------------------------+
|                  |             | *Thermal balance values*                     |
+------------------+-------------+----------------------------------------------+
| tgas             | 40.0        | Gas temperature (for THERMALBALANCE=0)       |
+------------------+-------------+----------------------------------------------+
| tfloor           | 2.725       | Floor tempearture (if tfloor                 |
+------------------+-------------+----------------------------------------------+

The command

.. code:: python

    pdr.run3DPDR()

runs the code. The code requires from a few seconds to several minutes
depending on your machine and the chosen PDR configuration to converge.

Plot PDR results: ``pdr.plot()``\ 
----------------------------------

The function ``pdr.plot()`` offers the ability to quickly plot results
for a particular model. It is *by no means* written to create
paper-quality plots and perform more advanced calculations /
comparisons. There is an extended list of available arguments for that
function, shown below:

+--------------------------------+--------------------------------------------+
| argument                       | Comments                                   |
+================================+============================================+
| x                              | position of element (pc)                   |
+--------------------------------+--------------------------------------------+
| Av                             | visual extinction (mag)                    |
+--------------------------------+--------------------------------------------+
| Tgas                           | gas temperature (K)                        |
+--------------------------------+--------------------------------------------+
| Tdust                          | dust temperature (K)                       |
+--------------------------------+--------------------------------------------+
| nH                             | total H-nucleus number density (cm-3)      |
+--------------------------------+--------------------------------------------+
| fuv                            | intensity of FUV radiation (Draine)        |
+--------------------------------+--------------------------------------------+
| photoelectric                  | Photoelectric heating (erg/cm3/s)          |
+--------------------------------+--------------------------------------------+
| Cionization                    | Carbon ionization heating (erg/cm3/s)      |
+--------------------------------+--------------------------------------------+
| H2formation                    | H2 formation heating (erg/cm3/s)           |
+--------------------------------+--------------------------------------------+
| H2photodis                     | H2 photodissociation heating (erg/cm3/s)   |
+--------------------------------+--------------------------------------------+
| FUVpumping                     | FUV pumping heating (erg/cm3/s)            |
+--------------------------------+--------------------------------------------+
| cosmicray                      | cosmic-ray heating (erg/cm3/s)             |
+--------------------------------+--------------------------------------------+
| turbulent                      | turbulent heating (erg/cm3/s)              |
+--------------------------------+--------------------------------------------+
| chemical                       | chemical heating (erg/cm3/s)               |
+--------------------------------+--------------------------------------------+
| gasgrain                       | gas-grain heating (erg/cm3/s)              |
+--------------------------------+--------------------------------------------+
| totheat                        | Total heating (erg/cm3/s)                  |
+--------------------------------+--------------------------------------------+
| COcool                         | CO cooling (erg/cm3/s)                     |
+--------------------------------+--------------------------------------------+
| C+cool                         | C+ cooling (erg/cm3/s)                     |
+--------------------------------+--------------------------------------------+
| Ccool                          | C cooling (erg/cm3/s)                      |
+--------------------------------+--------------------------------------------+
| Ocool                          | O cooling (erg/cm3/s)                      |
+--------------------------------+--------------------------------------------+
| any additional coolants here   |                                            |
+--------------------------------+--------------------------------------------+
| totcool                        | Total cooling (erg/cm3/s)                  |
+--------------------------------+--------------------------------------------+

where the additional coolants included in the params.dat file (e.g. HCO+
with ``hcop.dat``), follow the notation COOLANT+cool e.g. for HCO+ it
will be ``HCO+cool``. Other arguments include:

+-------------+-----------+--------------------------------------+
| Variable    | Default   | Comments                             |
+=============+===========+======================================+
| linestyle   | -         | Linestyle as in matplotlib           |
+-------------+-----------+--------------------------------------+
| directory   | sims/     | Specifies model output directory     |
+-------------+-----------+--------------------------------------+
| prefix      | None      | Prefix of model to plot              |
+-------------+-----------+--------------------------------------+
| scale       | loglog    | linear, loglog, semilogx, semilogy   |
+-------------+-----------+--------------------------------------+

In addition, the abundance of any species can be plotted by using the
name of the species in the function, as defined in the
``species_NETWORK.d`` chemical network file.

Example 1
~~~~~~~~~

.. code:: python

    pdr.plot("Av","Tgas",scale="semilogx")

plots the gas temperature versus Av on a semi-log scale (log in x axis)

Example 2
~~~~~~~~~

.. code:: python

    pdr.plot("Av","e-",scale="loglog")

plots the electron abundance versus Av in log-log scale

Example 3
~~~~~~~~~

It is possible to plot two or more species simultaneously

.. code:: python

    pdr.plot("Av",["H","H2"],scale="loglog")

for the HI-to-H2 transition, and

.. code:: python

    pdr.plot("Av",["C+","C","CO"],scale="loglog")

for the carbon cycle (C+, C, CO)

Example 4
~~~~~~~~~

.. code:: python

    pdr.plot("x",["totheat","totcool"],scale="semilogy")

plots the total heating and total cooling functions in a semi-log scale
(log in y axis). Under the THERMALBALANCE=1 flag, these two curves
should match.

General example
---------------

The script

.. code:: python

    import py3DPDR as pdr
    pdr.makefile()
    pdr.ics()
    pdr.species(network="REDUCED")
    pdr.params(icsfile="outgrid.dat", prefix="mymodel",coolant_files=["hcop.dat"])
    pdr.run3DPDR()
    pdr.plot("Av", "Tgas", prefix="mymodel", scale="semilogx")
    pdr.plot("Av",["H","H2"],prefix='mymodel',scale='loglog')
    pdr.plot("Av",["C+","C","CO"],prefix='mymodel',scale='loglog')
    pdr.plot("Av",["COcool","C+cool","Ccool","Ocool","HCO+cool","totcool"],prefix="mymodel")

compiles the code with the default flags, makes an initial conditions
file with the default variables (therefore output is named
``outgrid.dat``), creates the ``species_reduced.d`` file with the
default abundances of species for the REDUCED network, makes the
params.dat file with the user-defined initial conditions and prefix, and
adds HCO+ as an extra coolant. The script will then run the code and
will plot the gas temperature versus Av from the model specied with the
``prefix`` argument in a semilogx scale. It will also plot the HI-to-H2
transition, the C+/C/CO transition, and the cooling functions, all in
log-log scale.
