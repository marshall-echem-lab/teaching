---
title: "Lecture 1 — Energy Balances: Open Systems"
---

## The General Energy Balance

$$
\dot{Q} - \dot{W}_s = \dot{m} \left[ \Delta h + \frac{\Delta u^2}{2} + g \Delta z \right]
$$
updated
<!-- book-only-start -->
where $\dot{Q}$ is heat input, $\dot{W}_s$ is shaft work, $\dot{m}$ is the
mass flow rate, $\Delta h$ is the specific enthalpy change, $\Delta u^2/2$
is the kinetic energy change, and $g \Delta z$ is the potential energy change.
<!-- book-only-end -->

:::{note}
:class: slide-only
**Key assumptions:**
- Steady state: accumulation = 0
- Single inlet, single outlet
- Neglect kinetic and potential energy (most cases)
:::

:::{admonition} Why these assumptions?
:class: dropdown book-only

In most chemical engineering equipment — heat exchangers, reactors,
distillation columns — fluid velocities are moderate and elevation
differences are small, so kinetic and potential energy terms are
negligible compared to enthalpy changes. This simplifies the balance to:

$$\dot{Q} - \dot{W}_s = \dot{m} \, \Delta h$$

which is the form used in the vast majority of problems.
:::

## Enthalpy and Heat Capacity

For a single-phase stream with no reaction:

$$
\Delta h = \int_{T_1}^{T_2} C_p(T) \, dT
$$

For an ideal gas with constant $C_p$ this simplifies to:

$$
\Delta h = C_p \left( T_2 - T_1 \right)
$$

<!-- book-only-start -->
These two expressions are the starting point for nearly all energy balance
calculations. The integral form is exact; the simplified form assumes $C_p$
is constant over the temperature range of interest.
<!-- book-only-end -->

:::{note}
:class: slide-only
**In practice:**
- Use $C_p$ tables or polynomial fits from NIST/Perry's
- $C_p$ varies significantly with $T$ for polyatomic gases
- For liquids, $C_p \approx$ constant is usually acceptable
:::

:::{admonition} Temperature dependence of $C_p$
:class: dropdown book-only

For real gases, $C_p$ is fitted as a polynomial in $T$:

$$C_p(T) = a + bT + cT^2 + dT^3$$

Coefficients are tabulated in Perry's Chemical Engineers' Handbook.
For liquids, a mean value $\bar{C}_p$ over the temperature range is
usually accurate to within 2–3%.
:::

## Worked Example — Heat Exchanger

**Problem:** Cooling water enters at 20 °C and leaves at 55 °C.
Mass flow rate is 2.5 kg/s. Find $\dot{Q}$.

$$
\dot{Q} = \dot{m} \, C_p \, \Delta T = 2.5 \times 4.18 \times 35 = \mathbf{365 \text{ kW}}
$$

<!-- book-only-start -->
Here we assume steady state, negligible shaft work, and constant $C_p$
for liquid water. The result tells us how much heat the exchanger must
transfer per second to achieve the specified temperature rise.
<!-- book-only-end -->

:::{note}
:class: slide-only
**Steps:**
1. Identify streams in and out
2. State assumptions (steady, neglect KE/PE)
3. Look up $C_p$
4. Substitute and check units
:::

:::{admonition} Full solution with unit checks
:class: dropdown book-only

**Given:** $\dot{m} = 2.5$ kg/s, $T_{in} = 20$ °C, $T_{out} = 55$ °C,
$C_p = 4.18$ kJ kg$^{-1}$ K$^{-1}$

$$\dot{Q} = 2.5 \times 4.18 \times (55 - 20) = 365.75 \text{ kW}$$

The steam condensation side requires a separate balance using latent heat $\lambda$:

$$\dot{Q} = \dot{m}_{steam} \cdot \lambda$$

which gives the required steam flow rate once $\dot{Q}$ is known.
:::