"""Geothermal drilling cost economics — Kenya-focused field development model.

Central question: what drives geothermal drilling cost, and how sensitive are
project economics to drilling outcomes?

Drilling is typically 35-50% of total geothermal CAPEX and carries the risk a
lender cannot diversify away: dry wells. This model builds a simple 100 MW
field development case (Olkaria-style assumptions) and tests how well success
rate, well cost and well productivity move installed cost per MW and LCOE.

Sources for anchor values (see README for full list):
- IFC "Success of Geothermal Wells" global study: average success ~74% for
  development wells, lower for exploration.
- Kenya (Olkaria/Menengai): wells ~2,500-3,000 m, USD 5-6m per well,
  average ~5 MW per successful production well.
- Fervo Energy published learning curve: >50% drilling time reduction 2022-24
  (used for the "learning" scenario, not the base).

Usage: python drilling_economics.py   (writes charts + CSVs to outputs/)
"""

import os
from dataclasses import dataclass, replace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = "outputs"


@dataclass(frozen=True)
class Field:
    target_mw: float = 100.0
    mw_per_well: float = 5.0          # avg successful production well, Kenya
    success_rate: float = 0.74        # IFC global development-well average
    cost_per_well_musd: float = 5.5   # ~2,500-3,000 m Kenyan well
    injection_ratio: float = 0.25     # injection wells per production well
    makeup_pct: float = 0.15          # extra wells over life for decline
    surface_capex_musd_per_mw: float = 2.0   # plant, steam gathering, grid
    fixed_dev_cost_musd: float = 30.0        # infrastructure, roads, studies

    # LCOE layer (simple real-terms annuity)
    capacity_factor: float = 0.90
    life_yrs: int = 25
    wacc_real: float = 0.10
    opex_usd_mwh: float = 12.0


def economics(f: Field) -> dict:
    prod_wells = f.target_mw / f.mw_per_well
    wells_drilled = prod_wells / f.success_rate          # dry holes included
    total_wells = wells_drilled * (1 + f.injection_ratio) * (1 + f.makeup_pct)
    drilling_capex = total_wells * f.cost_per_well_musd
    total_capex = drilling_capex + f.surface_capex_musd_per_mw * f.target_mw + f.fixed_dev_cost_musd

    crf = f.wacc_real / (1 - (1 + f.wacc_real) ** -f.life_yrs)
    mwh_yr = f.target_mw * f.capacity_factor * 8760
    lcoe = (total_capex * 1e6 * crf) / mwh_yr + f.opex_usd_mwh

    return {
        "wells drilled (incl. dry & injection)": round(total_wells, 1),
        "drilling CAPEX (USDm)": round(drilling_capex, 1),
        "total CAPEX (USDm)": round(total_capex, 1),
        "drilling share of CAPEX": round(drilling_capex / total_capex, 3),
        "USDm per MW installed": round(total_capex / f.target_mw, 2),
        "LCOE (USD/MWh)": round(lcoe, 1),
    }


BASE = Field()
SCENARIOS = {
    "Base (Kenya today)": BASE,
    "Poor resource (55% success, 3.5 MW/well)": replace(BASE, success_rate=0.55, mw_per_well=3.5),
    "Cost inflation (+30% well cost)": replace(BASE, cost_per_well_musd=5.5 * 1.3),
    "Learning case (Fervo-style, -35% well cost, 85% success)":
        replace(BASE, cost_per_well_musd=5.5 * 0.65, success_rate=0.85),
}


def main() -> None:
    os.makedirs(OUT, exist_ok=True)

    scen = pd.DataFrame({k: economics(v) for k, v in SCENARIOS.items()})
    scen.to_csv(os.path.join(OUT, "scenario_summary.csv"))
    print(scen.to_string(), "\n")

    # Sensitivity: LCOE vs success rate for three well-cost levels
    rates = np.linspace(0.4, 0.95, 40)
    fig, ax = plt.subplots(figsize=(9, 5))
    for cost in (4.0, 5.5, 7.0):
        lcoes = [economics(replace(BASE, success_rate=r, cost_per_well_musd=cost))["LCOE (USD/MWh)"]
                 for r in rates]
        ax.plot(rates * 100, lcoes, label=f"US${cost}m per well")
    ax.axhline(70, color="grey", ls=":", lw=1)
    ax.text(41, 71, "typical PPA ceiling ~US$70/MWh", fontsize=8, color="grey")
    ax.set_xlabel("Well success rate (%)"), ax.set_ylabel("LCOE (USD/MWh)")
    ax.set_title("Geothermal LCOE vs drilling success rate — 100 MW field, Kenya-style assumptions")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "lcoe_vs_success_rate.png"), dpi=150)

    # CAPEX waterfall by driver (tornado on USDm/MW)
    shocks = {
        "Success rate 55% / 90%": [replace(BASE, success_rate=r) for r in (0.55, 0.90)],
        "Well cost +30% / -30%": [replace(BASE, cost_per_well_musd=5.5 * m) for m in (1.3, 0.7)],
        "Well output 3.5 / 6.5 MW": [replace(BASE, mw_per_well=m) for m in (3.5, 6.5)],
        "Make-up wells 25% / 5%": [replace(BASE, makeup_pct=m) for m in (0.25, 0.05)],
    }
    base_cost = economics(BASE)["USDm per MW installed"]
    rows = {k: [economics(lo)["USDm per MW installed"], economics(hi)["USDm per MW installed"]]
            for k, (lo, hi) in shocks.items()}
    sens = pd.DataFrame(rows, index=["low_case", "high_case"]).T
    sens.to_csv(os.path.join(OUT, "sensitivity_cost_per_mw.csv"))

    order = (sens["low_case"] - sens["high_case"]).abs().sort_values().index
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, k in enumerate(order):
        lo, hi = sorted(sens.loc[k])
        ax.barh(i, hi - lo, left=lo, color="#c05621", alpha=0.85)
    ax.axvline(base_cost, color="black", lw=1.2)
    ax.set_yticks(range(len(order))), ax.set_yticklabels(order)
    ax.set_xlabel("Installed cost (USDm per MW)")
    ax.set_title(f"What moves installed cost per MW (base = US${base_cost}m)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "tornado_cost_per_mw.png"), dpi=150)

    print("Sensitivity (USDm/MW):")
    print(sens.to_string())


if __name__ == "__main__":
    main()
