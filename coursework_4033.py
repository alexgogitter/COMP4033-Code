import matplotlib.pyplot as plt
import numpy as np
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Input import Input
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
from juzzyPython.type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
from juzzyPython.type1.system.T1_Rule import T1_Rule
from juzzyPython.type1.system.T1_Antecedent import T1_Antecedent
from juzzyPython.type1.system.T1_Consequent import T1_Consequent
from juzzyPython.type1.system.T1_Rulebase import T1_Rulebase

# ---------- Main Type-1 Fuzzy Logic ----------
def perform_fls_case1(age_val, headache_val, temp_val):
    # --- Inputs & Output ---
    patient_age_input = Input("Patient Age", Tuple(0,130))
    headache_severity_input = Input("Headache Severity", Tuple(0,10))
    patient_temperature_input = Input("Patient Temperature", Tuple(30,45))
    patient_urgency_output = Output("Patient Urgency", Tuple(0,100))

    

    # --- Membership Functions ---
    # Temperature
    temp_low    = T1MF_Trapezoidal("Hypothermia", [30, 30, 35.5, 36.5])
    temp_normal = T1MF_Triangular("Normal", 36, 37, 38)
    temp_high   = T1MF_Trapezoidal("Fever", [37.5, 38.5, 45, 45])
    # Headache
    headache_mild     = T1MF_Trapezoidal("Mild", [0, 0, 2, 4])
    headache_moderate = T1MF_Triangular("Moderate", 3, 5, 7)
    headache_severe   = T1MF_Trapezoidal("Severe", [6, 8, 10, 10])
    # Age
    age_young = T1MF_Trapezoidal("Young", [0, 0, 14, 24])
    age_adult = T1MF_Triangular("Adult", 20, 40, 64)
    age_elderly = T1MF_Trapezoidal("Elderly", [60, 70, 130, 130])
    # Urgency Output
    urgency_standard = T1MF_Trapezoidal("Standard", [0, 0, 30, 50])
    urgency_urgent   = T1MF_Triangular("Urgent", 40, 55, 70)
    urgency_emergency = T1MF_Trapezoidal("Emergency", [60, 80, 100, 100])

    membership_functions = {urgency_standard, urgency_urgent, urgency_emergency}

    # --- Antecedents & Consequents ---
    temp_low_a = T1_Antecedent(temp_low, patient_temperature_input, "TempLow")
    temp_normal_a = T1_Antecedent(temp_normal, patient_temperature_input, "TempNormal")
    temp_high_a = T1_Antecedent(temp_high, patient_temperature_input, "TempHigh")

    headache_mild_a = T1_Antecedent(headache_mild, headache_severity_input, "HeadacheMild")
    headache_moderate_a = T1_Antecedent(headache_moderate, headache_severity_input, "HeadacheModerate")
    headache_severe_a = T1_Antecedent(headache_severe, headache_severity_input, "HeadacheSevere")

    age_young_a = T1_Antecedent(age_young, patient_age_input, "AgeYoung")
    age_adult_a = T1_Antecedent(age_adult, patient_age_input, "AgeAdult")
    age_elderly_a = T1_Antecedent(age_elderly, patient_age_input, "AgeElderly")

    urgency_std_c = T1_Consequent(urgency_standard, patient_urgency_output, "UrgencyStandard")
    urgency_urg_c = T1_Consequent(urgency_urgent, patient_urgency_output, "UrgencyUrgent")
    urgency_emg_c = T1_Consequent(urgency_emergency, patient_urgency_output, "UrgencyEmergency")

    antecedents = {temp_low_a, temp_normal_a, temp_high_a,
                   headache_mild_a, headache_moderate_a, headache_severe_a,
                   age_young_a, age_adult_a, age_elderly_a}
    
    consequents = {urgency_std_c, urgency_urg_c, urgency_emg_c}

    # --- Rulebase ---
    rulebase = T1_Rulebase()
    # Hypothermia rules
    rulebase.addRule(T1_Rule([temp_low_a, age_young_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_low_a, age_adult_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_low_a, age_elderly_a], urgency_emg_c))
    # Fever rules
    rulebase.addRule(T1_Rule([temp_high_a, age_young_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_high_a, age_adult_a], urgency_urg_c))
    rulebase.addRule(T1_Rule([temp_high_a, age_elderly_a], urgency_urg_c))
    # Normal temp + headache rules
    for age_a in [age_young_a, age_adult_a, age_elderly_a]:
        rulebase.addRule(T1_Rule([age_a, temp_normal_a, headache_mild_a], urgency_std_c))
        rulebase.addRule(T1_Rule([age_a, temp_normal_a, headache_moderate_a], urgency_urg_c))
        rulebase.addRule(T1_Rule([age_a, temp_normal_a, headache_severe_a], urgency_emg_c))

    # --- Set input values ---
    patient_age_input.setInput(age_val)
    headache_severity_input.setInput(headache_val)
    patient_temperature_input.setInput(temp_val)
    patient_urgency_output.setDiscretisationLevel(100)
    # rule_cut = []
    # for rule in rulebase.getRules():
    #     print(rule.getFStrength(1))
    #     for cons in rule.getConsequents():
    #         rule_cut.append(cons.getMF().getAlphaCut(rule.getFStrength(1)))
    #     # Combine antecedent cuts (min t-norm)
    #     #aggregated_mfs
        
    #print(rule_cut)
    # --- Evaluate ---
    output_dict = rulebase.evaluate(1)
    urgency_value = output_dict[patient_urgency_output]

    print(f"\n Defuzzified Patient Urgency: {urgency_value:.2f}")

    # --- Input Membership Degree Visualization ---
    fig, axes = plt.subplots(3,1, figsize=(10,10))

    # Age
    axes[0].set_title("Patient Age Membership Degrees")
    x_vals = np.linspace(0,130,500)
    for mf in [age_young, age_adult, age_elderly]:
        y_vals = [mf.getFS(x) for x in x_vals]
        axes[0].plot(x_vals, y_vals, label=mf.getName())
        mu = mf.getFS(age_val)
        if mu > 0:
            axes[0].text(age_val+1, mu+0.02, f"{mu:.2f}", fontsize=10)
    axes[0].axvline(age_val, color='red', linestyle='--', label='Input')
    axes[0].set_ylabel("Membership"); axes[0].set_xlabel("Age"); axes[0].legend()

    # Headache
    axes[1].set_title("Headache Severity Membership Degrees")
    x_vals = np.linspace(0,10,500)
    for mf in [headache_mild, headache_moderate, headache_severe]:
        y_vals = [mf.getFS(x) for x in x_vals]
        axes[1].plot(x_vals, y_vals, label=mf.getName())
        mu = mf.getFS(headache_val)
        if mu > 0:
            axes[1].text(headache_val+0.1, mu+0.02, f"{mu:.2f}", fontsize=10)
    axes[1].axvline(headache_val, color='red', linestyle='--', label='Input')
    axes[1].set_ylabel("Membership"); axes[1].set_xlabel("Severity"); axes[1].legend()

    # Temperature
    axes[2].set_title("Patient Temperature Membership Degrees")
    x_vals = np.linspace(30,45,500)
    for mf in [temp_low, temp_normal, temp_high]:
        y_vals = [mf.getFS(x) for x in x_vals]
        axes[2].plot(x_vals, y_vals, label=mf.getName())
        mu = mf.getFS(temp_val)
        if mu > 0:
            axes[2].text(temp_val+0.1, mu+0.02, f"{mu:.2f}", fontsize=10)
    axes[2].axvline(temp_val, color='red', linestyle='--', label='Input')
    axes[2].set_ylabel("Membership"); axes[2].set_xlabel("Temperature (°C)"); axes[2].legend()

    # --- Output Membership & Defuzzified Value ---
    fig2, ax = plt.subplots(figsize=(10,5))
    ax.set_title("Patient Urgency Membership Functions with Defuzzified Value")
    x_vals = np.linspace(0,100,500)
    y_vals_max = np.zeros_like(x_vals)
    for mf in [urgency_standard, urgency_urgent, urgency_emergency]:
        y_mf = np.array([mf.getFS(x) for x in x_vals])
        ax.plot(x_vals, y_mf, label=mf.getName(), linewidth=2)
        y_vals_max = np.maximum(y_vals_max, y_mf)

    for rule in rulebase.getRules():
        for cons in rule.getConsequents():
            mf = cons.getMF()
            alpha = rule.getFStrength(1)
            y_cut = np.array([min(mf.getFS(x), alpha) for x in x_vals])
            ax.fill_between(x_vals, 0, y_cut, alpha=0.1, color='blue')
    ax.plot([urgency_value], [0], marker='o', markersize=10, color='purple', label=f"Defuzzified Value: {urgency_value:.2f}", zorder=5)
    #ax.fill_between(x_vals, 0, y_vals_max, color="lightblue", alpha=0.3, label="Aggregated Output")
    ax.set_xlabel("Urgency Score")
    ax.set_ylabel("Membership")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show(block=True)
    plt.show()

    return urgency_value

def main():
    print("Welcome to the Type-1 Fuzzy Medical Triage System (Case 1) \n")
    try:
        # age_val = float(input("Enter patient age (0–130): "))
        # headache_val = float(input("Enter headache severity (0–10): "))
        # temp_val = float(input("Enter temperature (30–45 °C): "))
        urgency_value = perform_fls_case1(65, 5, 37.5)
        print(f"\n Final Defuzzified Patient Urgency: {urgency_value:.2f}")
    except ValueError:
        print(" Invalid input. Please enter numeric values.")

if __name__ == "__main__":
    main()


