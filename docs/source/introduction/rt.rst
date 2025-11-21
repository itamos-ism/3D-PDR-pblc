Radiative Transfer
==================

Constructing synthetic observations enables direct comparison between modeled results and observational data (see review by `Haworth et al., 2018 <https://ui.adsabs.harvard.edu/abs/2018NewAR..82....1H/abstract>`_). Both **RT-tool** and **RT-synth** algorithms are based on the method presented in Bisbas et al. (`2017 <https://ui.adsabs.harvard.edu/abs/2017ApJ...850...23B/abstract>`_; `2021 <https://ui.adsabs.harvard.edu/abs/2021MNRAS.502.2701B/abstract>`_).

We solve the radiative transfer equation along the line-of-sight element :math:`dz`:

.. math::
   \frac{dI_{\nu}}{dz} = -\alpha_{\nu}I_{\nu} + \alpha_{\nu}S_{\nu} + \rho\kappa_{\nu,\text{dust}}(B_{\nu}(T_{\text{dust}}) - I_{\nu})

where :math:`I_{\nu}` is the intensity, :math:`\alpha_{\nu}` the absorption coefficient, :math:`S_{\nu}` the source function, :math:`\rho` the density, :math:`\kappa_{\nu,\text{dust}}` the dust opacity, and :math:`B_{\nu}(T_{\text{dust}})` the Planck function at dust temperature :math:`T_{\text{dust}}`.

For dust opacity at solar metallicity, we adopt:

.. math::
   \kappa_{\nu,{\rm dust}} = 0.1\times {\cal D}\left(\frac{\nu}{1000\,{\rm GHz}^2}\right)\,{\rm cm}^2\,{\rm g}^{-1}

per unit total gas and dust density (see `Arzoumanian et al. 2011 <https://ui.adsabs.harvard.edu/abs/2011A%26A...529L...6A/abstract>`_), where :math:`\cal D` is the dust-to-gas mass ratio normalized to :math:`10^{-2}`.

The source function and absorption coefficient for transition :math:`i \rightarrow j` are:

.. math::
   S_{\nu} &= \frac{2h\nu_{0}^{3}}{c^{2}}\frac{n_{i}g_{j}}{n_{j}g_{i} - n_{i}g_{j}} \\
   \alpha_{\nu} &= \frac{c^{2}n_{i}A_{ji}}{8\pi\nu_{0}^{2}}\left\{\frac{n_{j}g_{i}}{n_{i}g_{j}} - 1\right\}\phi_{\nu}

where :math:`\nu_{0}` is the line center frequency, :math:`A_{ji}` the Einstein A coefficient, :math:`n_{i}, n_{j}` level populations, :math:`g_{i}, g_{j}` statistical weights, and :math:`\phi_{\nu}` the line profile.

The line profile assumes a Maxwellian velocity distribution:

.. math::
   \phi_{\nu} = \frac{1}{\sqrt{2\pi\sigma_{\nu}^{2}}}\exp\left\{-\frac{[(1+v_{\text{los}}/c)\nu - \nu_{0}]^{2}}{2\sigma_{\nu}^{2}}\right\}

with :math:`v_{\text{los}}` the gas velocity along the line of sight and :math:`\sigma_{\nu}` the dispersion:

.. math::
   \sigma_{\nu} = \frac{\nu_{0}}{c}\sqrt{\frac{k_{\text{B}}T_{\text{gas}}}{m_{\text{mol}}} + v_{\text{turb}}^{2}}

The formal solution is:

.. math::
   I_{\nu}(z) = I_{\nu}(0)e^{-\tau_{\nu}(z)} + \int_{0}^{\tau_{\nu}(z)}S_{\nu}(z')e^{-(\tau_{\nu}(z)-\tau_{\nu}(z'))}d\tau_{\nu}(z')

where :math:`\tau_{\nu} = \int_{0}^{z}\alpha_{\nu}(z')dz'` is the optical depth.

The line intensity is obtained by subtracting dust continuum: :math:`I_{\nu,\text{line}} = I_{\nu} - I_{\nu,\text{dust}}`, as well as background emission.

The antenna temperature is:

.. math::
   T_{A} = \frac{c^{2}I_{\nu,\text{line}}}{2k_{\text{B}}\nu^{2}}

in units of [K], and the velocity-integrated intensity is:

.. math::
   W = \int T_{A}dv_{\text{los}}

in units of [K km/s].

For further reading on radiative transfer, the notes of `C.P. Dullemond <https://www.ita.uni-heidelberg.de/~dullemond/lectures/radtrans_2012/index.shtml>`_ are recommended.
