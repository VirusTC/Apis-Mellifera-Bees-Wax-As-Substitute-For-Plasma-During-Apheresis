import sys

class SFWBFormulationEngine:
    def __init__(self, target_volume_ml=1000):
        self.target_volume = target_volume_ml
        
        # Human physiological constants (Targets)
        self.TARGET_PH_MIN = 7.35
        self.TARGET_PH_MAX = 7.45
        self.TARGET_OSMOLALITY_MIN = 280 # mOsm/kg
        self.TARGET_OSMOLALITY_MAX = 300 # mOsm/kg
        self.TARGET_VISCOSITY_MIN = 3.5  # cP
        self.TARGET_VISCOSITY_MAX = 5.5  # cP

    def calculate_formulation(self, hematocrit_target=0.40, wax_saponification_efficiency=0.95):
        """
        Calculates the volumetric distribution of the three phases.
        
        Args:
            hematocrit_target (float): Synthetic cell/lipid volume fraction (0.0 - 1.0)
            wax_saponification_efficiency (float): Degree of wax conversion to water-soluble salts
        """
        if not (0.10 <= hematocrit_target <= 0.50):
            raise ValueError("Target hematocrit must be between 10% and 50% for human physiological stability.")

        # Allocate volumes based on target hematocrit
        lipid_capsule_vol = self.target_volume * hematocrit_target
        plasma_vol = self.target_volume * (1.0 - hematocrit_target)
        
        # Sub-component calculations within Lipid Capsule Phase (VerduraRX + Capsules)
        # Beta-carotene must be dissolved in the lipid phase at a tight 1:5 ratio to maintain solubility
        beta_carotene_mass_g = lipid_capsule_vol * 0.05 
        carrier_lipid_vol_ml = lipid_capsule_vol * 0.95
        
        # Sub-component calculations within Plasma Phase (Apis Matrix)
        # Saponified beeswax salts acting as fatty-acid surrogates + plant recombinant proteins
        saponified_wax_mass_g = (plasma_vol * 0.03) * wax_saponification_efficiency
        plant_albumin_mass_g = plasma_vol * 0.045  # Target 4.5 g/dL oncotic pressure
        sterile_water_ml = plasma_vol - (plant_albumin_mass_g / 1.35) # Adjusted for protein density
        
        # Predict Biophysical Properties
        predicted_viscosity = 1.0 + (2.5 * hematocrit_target) + (7.5 * (hematocrit_target ** 2))
        predicted_osmolality = 275 + (saponified_wax_mass_g * 1.5)
        
        # Safety Check Flags
        safety_status = "PASSED"
        reasons = []
        
        if not (self.TARGET_VISCOSITY_MIN <= predicted_viscosity <= self.TARGET_VISCOSITY_MAX):
            safety_status = "FAILED"
            reasons.append(f"Viscosity critical anomaly: {predicted_viscosity:.2f} cP (Out of range)")
            
        if not (self.TARGET_OSMOLALITY_MIN <= predicted_osmolality <= self.TARGET_OSMOLALITY_MAX):
            safety_status = "FAILED"
            reasons.append(f"Osmolality collapse threat: {predicted_osmolality:.1f} mOsm/kg")

        return {
            "Total Batch Volume": f"{self.target_volume} mL",
            "Phase A: Plasma Volume (Apis Matrix)": f"{plasma_vol:.1f} mL",
            "  - Sterile Reconstituted Water": f"{sterile_water_ml:.1f} mL",
            "  - Saponified Beeswax Salts": f"{saponified_wax_mass_g:.2f} g",
            "  - Rice-Derived Recombinant Albumin": f"{plant_albumin_mass_g:.2f} g",
            "Phase B & C: Oxygenated Lipid Capsules (VerduraRX Integration)": f"{lipid_capsule_vol:.1f} mL",
            "  - Encapsulated Carrier Lipids": f"{carrier_lipid_vol_ml:.1f} mL",
            "  - Complexed Beta-Carotene Carrier": f"{beta_carotene_mass_g:.2f} g",
            "Predicted Physical Properties": {
                "Viscosity": f"{predicted_viscosity:.2f} cP",
                "Osmolality": f"{predicted_osmolality:.1f} mOsm/kg"
            },
            "Clinical Clearance Status": safety_status,
            "Validation Errors": reasons
        }

if __name__ == "__main__":
    # Simulate a standard 1-Liter batch for trauma protocols
    engine = SFWBFormulationEngine(target_volume_ml=1000)
    
    # Run simulation with 35% synthetic cell concentration and 98% wax purity conversion
    batch_sheet = engine.calculate_formulation(hematocrit_target=0.35, wax_saponification_efficiency=0.98)
    
    print("=================================================================")
    print("      SYNTHETIC FRESH WHOLE BLOOD (SFWB) BATCH FORMULATION       ")
    print("=================================================================")
    for key, value in batch_sheet.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    print("=================================================================")
