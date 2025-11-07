Constructing Initial Conditions
===============================

To run a PDR model, you must first construct the density distribution of your cloud. Initial condition files can be stored in the ``ics/`` directory for repeated use across different PDR models. The ``ics/`` directory contains a script (``uniform1D.f90``) to help create density distributions, though users may create their own using external tools as long as the input format is respected.

One-dimensional Density Functions
---------------------------------

**Input Format:**
::

    x(pc), y(pc), z(pc), nH(cm-3)

- **x, y, z**: Spatial coordinates in parsecs (set ``y`` and ``z`` to ``0.0`` for 1D models)
- **nH**: Total H-nucleus number density in cm⁻³

For simple 1D distributions, use the ``uniform1D.f90`` script:

.. code-block:: bash

    gfortran -o uniform1D uniform1D.f90
    ./uniform1D

This interactive script creates uniform-density distributions. Example session:

::

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

This creates ``outgrid.dat`` containing a cloud with:

- Density: 1000 cm⁻³
- Maximum visual extinction: 10 mag
- Minimum visual extinction: 10⁻³ mag (resolves HI-to-H₂ transition)
- Resolution: 30 points per Av dex
- Total points: 122 (including first and last points)

You may rename ``outgrid.dat`` to a more descriptive name (e.g., ``1Dn30.dat``).

Three-dimensional Density Distributions
---------------------------------------

3D-PDR performs ray-tracing on uniform grids where resolution must be a power of 2 (e.g., 32³, 64³, 128³) and the domain must be cubic.

**File Format:**
The 3D density file includes a two-line header followed by coordinate-density data:

::

    32 32 32
    10. 10. 10.
    x₁ y₁ z₁ nH₁
    x₂ y₂ z₂ nH₂
    ...

- **Header line 1**: Number of cells along each axis (integers)
- **Header line 2**: Physical box size in parsecs (floats)
- **Remaining lines**: Cell centroids (x,y,z in pc) and densities (nH in cm⁻³)

.. important::
   - The computational domain extends along positive x,y,z axes.
   - If your hydrodynamic data contains negative coordinates, shift them to positive values (positive octant).
   - Coordinates represent cell *centroids*, not corners. If you constructed the distribution so as the first set of coordinates starts from the values of (0,0,0), you are doing something wrong! You must shift it by half cell along all axes.

**XYZ Format Options:**
The ``XYZ`` flag in the makefile determines the data ordering:

- **XYZ = 0**: z changes first (x → y → z)
  
  .. code-block:: fortran

     do i = 1, itot
       do j = 1, itot
          do k = 1, itot
             write(1,*) x(i), y(j), z(k), nH(i,j,k)
          end do
       end do
     end do

- **XYZ = 1**: x changes first (z → y → x)
  
  .. code-block:: fortran

     do k = 1, itot
       do j = 1, itot
          do i = 1, itot
             write(1,*) x(i), y(j), z(k), nH(i,j,k)
          end do
       end do
     end do

See the examples section for a complete 3D implementation.
