from juzzyPython.examples import SimpleT1FLS

from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Plot import Plot
from juzzyPython.generic.Input import Input
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
from juzzyPython.type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal

from juzzyPython.type1.system.T1_Rule import T1_Rule
from juzzyPython.type1.system.T1_Antecedent import T1_Antecedent
from juzzyPython.type1.system.T1_Consequent import T1_Consequent
from juzzyPython.type1.system.T1_Rulebase import T1_Rulebase
from juzzyPython.testing.timeRecorder import timeDecorator

from juzzyPython.intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from juzzyPython.intervalType2.sets.IntervalT2MF_Trapezoidal import IntervalT2MF_Trapezoidal
from juzzyPython.intervalType2.system.IT2_Antecedent import IT2_Antecedent
from juzzyPython.intervalType2.system.IT2_Consequent import IT2_Consequent
from juzzyPython.intervalType2.system.IT2_Rule import IT2_Rule
from juzzyPython.intervalType2.system.IT2_Rulebase import IT2_Rulebase



def perform_case1_fls(patient_age: int = 30, headache_severity: int = 5, patient_temperature: float = 37.0):
    patient_age_input = Input("Patient Age", Tuple(0, 130))
    headache_severity_input = Input("Headache Severity", Tuple(0, 10))
    patient_temperature_input = Input("Patient Temperature", Tuple(30.0, 45.0))

    patient_urgency_output = Output("Patient Urgency", Tuple(0, 100))

    patient_temp_extremely_low = T1MF_Trapezoidal("Extremely Low", parameters=[33.0, 33.0, 35.0, 36.0])
    patient_temp_normal = T1MF_Triangular("Normal", 33.5, 36.8, 37.8)
    patient_temp_extremely_high = T1MF_Trapezoidal("Extremely High", parameters=[37.0, 39.0, 42.0, 42.0])

    headache_severity_mild = T1MF_Triangular("Mild", 0, 2.5, 5)
    headache_severity_moderate = T1MF_Triangular("Moderate", 4, 6.5, 9)
    headache_severity_severe = T1MF_Trapezoidal("Severe", parameters=[7, 10, 10, 10])

    age_pediatric = T1MF_Trapezoidal("Pediatric", parameters = [0, 0, 14, 20])
    age_adult = T1MF_Triangular("Adult", 15, 30, 45)
    age_geriatric = T1MF_Trapezoidal("Geriatric", parameters = [40, 65, 130, 130])

    urgency_standard = T1MF_Trapezoidal("Standard Urgency", parameters = [0, 0, 20, 40])
    urgency_urgent = T1MF_Triangular("Urgent", 30, 50, 70)
    urgency_emergency = T1MF_Trapezoidal("Emergency", parameters = [60, 80, 100, 100])

    age_pediatric_antecedent = T1_Antecedent(age_pediatric, patient_age_input, "AgePediatric")
    age_adult_antecedent = T1_Antecedent(age_adult, patient_age_input, "AgeAdult")
    age_geriatric_antecedent = T1_Antecedent(age_geriatric, patient_age_input, "AgeGeriatric")

    headache_mild_antecedent = T1_Antecedent(headache_severity_mild, headache_severity_input, "HeadacheMild")
    headache_moderate_antecedent = T1_Antecedent(headache_severity_moderate, headache_severity_input, "HeadacheModerate")
    headache_severe_antecedent = T1_Antecedent(headache_severity_severe, headache_severity_input, "HeadacheSevere") 

    temp_extremely_low_antecedent = T1_Antecedent(patient_temp_extremely_low, patient_temperature_input, "TempExtremelyLow")
    temp_normal_antecedent = T1_Antecedent(patient_temp_normal, patient_temperature_input, "TempNormal")
#temp_high_antecedent = T1_Antecedent(patient_temp_high, patient_temperature_input, "TempHigh")
    temp_extremely_high_antecedent = T1_Antecedent(patient_temp_extremely_high, patient_temperature_input, "TempExtremelyHigh")

    urgency_standard_consequent = T1_Consequent(urgency_standard, patient_urgency_output, "UrgencyStandard")
    urgency_urgent_consequent = T1_Consequent(urgency_urgent, patient_urgency_output, "UrgencyUrgent")
    urgency_emergency_consequent = T1_Consequent(urgency_emergency, patient_urgency_output, "UrgencyEmergency") 

    rulebase = T1_Rulebase()
    rulebase.addRule(T1_Rule([temp_extremely_low_antecedent, headache_mild_antecedent, age_pediatric_antecedent], consequent=urgency_emergency_consequent))
    rulebase.addRule(T1_Rule([temp_extremely_low_antecedent, headache_moderate_antecedent, age_pediatric_antecedent], consequent=urgency_emergency_consequent))
    rulebase.addRule(T1_Rule([temp_extremely_low_antecedent, headache_severe_antecedent, age_pediatric_antecedent], consequent=urgency_emergency_consequent))
    rulebase.addRule(T1_Rule([temp_normal_antecedent, headache_mild_antecedent, age_pediatric_antecedent], consequent=urgency_standard_consequent ))
    rulebase.addRule(T1_Rule([temp_normal_antecedent, headache_moderate_antecedent, age_pediatric_antecedent], consequent=urgency_urgent_consequent))
    rulebase.addRule(T1_Rule([temp_normal_antecedent, headache_severe_antecedent, age_pediatric_antecedent], consequent=urgency_emergency_consequent))
    rulebase.addRule(T1_Rule([temp_extremely_high_antecedent, headache_mild_antecedent, age_pediatric_antecedent], consequent=urgency_emergency_consequent))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))
    # rulebase.addRule(T1_Rule([], consequent=))

    patient_urgency_output.setDiscretisationLevel(100)
    patient_age_input.setInput(patient_age)
    headache_severity_input.setInput(headache_severity)
    patient_temperature_input.setInput(patient_temperature)

   
    urgency_value_height = rulebase.evaluate(0)[patient_urgency_output]
    urgency_value_centroid = rulebase.evaluate(1)[patient_urgency_output]

    print("Patient Age: " + str(patient_age_input.getInput()))
    print("Headache Severity: " + str(headache_severity_input.getInput()))
    print("Patient Temperature: " + str(patient_temperature_input.getInput()))
    print("Using height defuzzification, the FLS recommends patient urgency value of: " + str(urgency_value_height))
    print("Using centroid defuzzification, the FLS recommends patient urgency value of: " + str(urgency_value_centroid))

    plot = Plot()

    plotMFs(plot, "Patient Age Membership Functions", [age_pediatric, age_adult, age_geriatric], patient_age_input.getDomain(), 100)
    plotMFs(plot, "Headache Severity Membership Functions", [headache_severity_mild, headache_severity_moderate, headache_severity_severe], headache_severity_input.getDomain(), 100)
    plotMFs(plot, "Patient Temperature Membership Functions", [patient_temp_extremely_low, patient_temp_normal, patient_temp_extremely_high], patient_temperature_input.getDomain(), 100)
    plotMFs(plot, "Patient Urgency Membership Functions", [urgency_standard, urgency_urgent, urgency_emergency], patient_urgency_output.getDomain(), 100)


    plot.show()

def perform_case2_fls(patient_age: list[int] = [15, 40], headache_severity: list[int] = [2, 8], patient_temperature: list[float] = [36.5, 39.0]):
    pass

@timeDecorator
def plotMFs(plot,name,sets,xAxisRange,discretizationLevel):
    """Plot the lines for each membership function of the sets"""
    plot.figure()
    plot.title(name)
    for i in range(len(sets)):
        plot.plotMF(name.replace("Membership Functions",""),sets[i].getName(),sets[i],discretizationLevel,xAxisRange,Tuple(0.0,1.0),False)
    plot.legend()

def main():
    print("Performing FLS for Case 1:")
    perform_case1_fls(patient_age=11, headache_severity=10, patient_temperature=34)
    print("\nPerforming FLS for Case 2:")
    perform_case2_fls()


main()