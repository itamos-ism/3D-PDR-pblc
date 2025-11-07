The species_network.d
=====================

To modify the initial elemental abundances in your PDR model, edit the ``species_NETWORK.d`` file located in the ``chemfiles/`` directory. The specific file name depends on the chemical network you are using.

.. important::
   No re-compilation of 3D-PDR is required when only modifying elemental abundances. Simply edit the appropriate species file and run your simulation.

The ``species_NETWORK.d`` file contains the initial abundance values for all chemical elements included in the network. Modify these values according to your desired metallicity or abundance pattern.

Example modification for the REDUCED network
--------------------------------------------

If using the ``species_reduced.d`` network, you would edit ``chemfiles/species_reduced.d`` and adjust the abundance values for elements such as hydrogen, carbon, oxygen, etc., to reflect your desired chemical composition.

When editing ``species_reduced.d``, pay special attention to these critical species:

- **C+ (entry 11)**: Carbon abundance should be specified here rather than in neutral C (entry 25) to allow the code to start the chemical network from the ionized phase of carbon
- **O (entry 30)**: Oxygen abundance
- **H (entry 32)**: Atomic hydrogen abundance
- **H2 (entry 31)**: Molecular hydrogen abundance
- **He (entry 26)**: Helium abundance
- **Mg+ (entry 10)**: Ionized magnesium abundance (if desired)

Locate the relevant entries in your species file and modify the abundance values (third column):

.. code-block:: text

   11,C+,1.40e-04,12.0    # Carbon abundance
   30,O,3.00e-04,16.0     # Oxygen abundance
   32,H,4.00e-01,1.0      # Atomic hydrogen
   31,H2,3.00e-01,2.0     # Molecular hydrogen
   26,He,1.00e-01,4.0     # Helium abundance
   10,Mg+,0.0,24.0        # Ionized magnesium

.. note::
   - The total hydrogen abundance must satisfy: **HI + 2×H₂ = 1** at all times
   - The default values (H = 0.4, H₂ = 0.3) satisfy this constraint: 0.4 + 2×0.3 = 1
   - Electron abundance (e-, entry 33) is automatically calculated by 3D-PDR from the input ionized elements and should not be modified manually, unless specialized runs need to be performed
   - For specialized runs, you may adjust the HI/H₂ ratio, but always maintain the total hydrogen constraint

After saving your changes to the species file, 3D-PDR will automatically use the updated abundances in your next simulation without requiring recompilation.





