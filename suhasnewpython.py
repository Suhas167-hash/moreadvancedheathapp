import streamlit as st

# Page setup for a professional clinical portfolio
st.set_page_config(
    page_title="Pre-Med Health & Triage Suite",
    page_icon="🏥",
    layout="centered"
)

# Multi-Tool Navigation Sidebar
st.sidebar.title("🏥 Health Suite Navigation")
app_mode = st.sidebar.radio(
    "Select a Health Tool:",
    [
        "1. BMI Screening (Your Original)", 
        "2. BMR & Caloric Needs Calculator", 
        "3. Target Heart Rate Zone Calculator",
        "4. Ideal Body Weight Calculator",
        "5. Hydration & Daily Water Calculator",
        "6. Advanced Clinical Diagnostics (Coming Soon)"
    ]
)

# =========================================================================
# TOOL 1: YOUR ORIGINAL BMI CALCULATOR
# =========================================================================
if app_mode == "1. BMI Screening (Your Original)":
    st.title("⚖️ Body Mass Index (BMI) Calculator")
    st.write("Calculate your Body Mass Index quickly and easily!")

    weight = st.number_input("What is your weight in pounds?", min_value=0.0, step=0.1, value=150.0)
    height = st.number_input("What is your height in inches?", min_value=0.0, step=0.1, value=65.0)

    if weight > 0 and height > 0:
        bmi = (weight * 703) / (height * height)
        st.subheader(f"Your BMI is: {bmi:.2f}")

        if bmi < 18.5:
            st.error("You are underweight")
        elif 18.5 <= bmi < 24.9:
            st.success("You have regular weight")
        elif 24.9 <= bmi < 29.9:
            st.warning("You are overweight")
        else:
            st.error("You are obese")
    else:
        st.info("Please enter a valid weight and height to calculate your BMI.")

# =========================================================================
# TOOL 2: BMR & CALORIC NEEDS (MIFFLIN-ST JEOR)
# =========================================================================
elif app_mode == "2. BMR & Caloric Needs Calculator":
    st.title("🔥 Basal Metabolic Rate & TDEE Calculator")
    st.write("Estimate baseline metabolic energy expenditure using the clinically validated Mifflin-St Jeor equation.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=25)
        sex = st.selectbox("Biological Sex", ["Male", "Female"])
    with col2:
        weight_lbs = st.number_input("Weight (pounds)", min_value=10.0, value=150.0, step=0.1)
        height_in = st.number_input("Height (inches)", min_value=10.0, value=67.0, step=0.1)
        
    weight_kg = weight_lbs / 2.20462
    height_cm = height_in * 2.54
    
    if sex == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    st.subheader("Results")
    st.metric(label="Basal Metabolic Rate (BMR)", value=f"{int(bmr)} kcal/day")
    
    st.subheader("⚡ Total Daily Energy Expenditure (TDEE)")
    activity = st.selectbox(
        "Select Daily Activity Level:",
        [
            "Sedentary (Little or no exercise)",
            "Lightly Active (Light exercise 1-3 days/week)",
            "Moderately Active (Moderate exercise 3-5 days/week)",
            "Very Active (Hard exercise 6-7 days/week)"
        ]
    )
    
    multipliers = {
        "Sedentary (Little or no exercise)": 1.2,
        "Lightly Active (Light exercise 1-3 days/week)": 1.375,
        "Moderately Active (Moderate exercise 3-5 days/week)": 1.55,
        "Very Active (Hard exercise 6-7 days/week)": 1.725
    }
    
    tdee = bmr * multipliers[activity]
    st.metric(label="Estimated Maintenance Calories (TDEE)", value=f"{int(tdee)} kcal/day")

# =========================================================================
# TOOL 3: TARGET HEART RATE ZONE (KARVONEN FORMULA)
# =========================================================================
elif app_mode == "3. Target Heart Rate Zone Calculator":
    st.title("🫀 Target Heart Rate Zone Calculator")
    st.write("Calculate aerobic and anaerobic training zones using the clinical Karvonen Formula.")
    
    col1, col2 = st.columns(2)
    with col1:
        age_hr = st.number_input("Age (years)", min_value=1, max_value=120, value=20)
    with col2:
        rhr = st.number_input("Resting Heart Rate (BPM)", min_value=30, max_value=120, value=65)
        
    max_hr = 220 - age_hr
    hrr = max_hr - rhr
    
    st.subheader("Results")
    st.metric(label="Estimated Maximum Heart Rate", value=f"{max_hr} BPM")
    
    st.markdown("### 🏃‍♂️ Cardiovascular Training Zones")
    zones = [
        {"name": "Warm Up / Recovery (50% - 60%)", "low": 0.50, "high": 0.60},
        {"name": "Fat Burning / Light Aerobic (60% - 70%)", "low": 0.60, "high": 0.70},
        {"name": "Cardio / Aerobic Endurance (70% - 85%)", "low": 0.70, "high": 0.85},
        {"name": "Peak / Anaerobic Threshold (85% - 100%)", "low": 0.85, "high": 1.00}
    ]
    
    for zone in zones:
        low_bpm = int((hrr * zone["low"]) + rhr)
        high_bpm = int((hrr * zone["high"]) + rhr)
        st.markdown(f"**{zone['name']}:** `{low_bpm} - {high_bpm} BPM`")

# =========================================================================
# TOOL 4: IDEAL BODY WEIGHT (DEVINE FORMULA)
# =========================================================================
elif app_mode == "4. Ideal Body Weight Calculator":
    st.title("🧬 Ideal Body Weight (IBW) Calculator")
    st.write("Calculate clinical Ideal Body Weight thresholds using the verified Devine Formula.")
    st.info("💡 **Clinical Note:** IBW equations are critical in medicine for calculating precise critical care medication dosages and mechanical ventilator settings.")

    col1, col2 = st.columns(2)
    with col1:
        ibw_sex = st.selectbox("Patient Biological Sex", ["Male", "Female"])
    with col2:
        ibw_height = st.number_input("Patient Height (inches)", min_value=60.0, max_value=90.0, value=68.0, step=0.5)

    # Devine Formula applies to heights above 60 inches (5 feet)
    inches_over_5ft = ibw_height - 60.0
    
    if ibw_sex == "Male":
        ibw_kg = 50.0 + (2.3 * inches_over_5ft)
    else:
        ibw_kg = 45.5 + (2.3 * inches_over_5ft)
        
    ibw_lbs = ibw_kg * 2.20462

    st.subheader("Results")
    m_col1, m_col2 = st.columns(2)
    m_col1.metric(label="Ideal Weight (Kilograms)", value=f"{ibw_kg:.1f} kg")
    m_col2.metric(label="Ideal Weight (Pounds)", value=f"{ibw_lbs:.1f} lbs")

# =========================================================================
# TOOL 5: HYDRATION & DAILY WATER CALCULATOR
# =========================================================================
elif app_mode == "5. Hydration & Daily Water Calculator":
    st.title("💧 Fluid Intake & Hydration Suite")
    st.write("Determine daily hydration demands optimized by patient total weight and active workout strain.")

    col1, col2 = st.columns(2)
    with col1:
        h_weight = st.number_input("Current Patient Weight (pounds)", min_value=30.0, value=150.0, step=0.5)
    with col2:
        exercise_time = st.slider("Daily Intense Physical Exercise (minutes)", 0, 180, 30, step=5)

    # Base hydration equation: 0.5 oz of water per pound of bodyweight
    base_ounces = h_weight * 0.5
    # Add exercise modification: ~12 ounces of water for every 30 minutes of heavy sweating
    exercise_ounces = (exercise_time / 30) * 12
    
    total_ounces = base_ounces + exercise_ounces
    total_liters = total_ounces * 0.0295735

    st.subheader("Results")
    w_col1, w_col2 = st.columns(2)
    w_col1.metric(label="Target Fluid Vol (Ounces)", value=f"{total_ounces:.1f} fl oz")
    w_col2.metric(label="Target Fluid Vol (Liters)", value=f"{total_liters:.2f} L")
    st.caption("Target metrics may shift dynamically during periods of extreme high heat indexes or custom clinical restriction protocols (e.g., chronic heart failure or renal pathology).")

# =========================================================================
# TOOL 6: ADVANCED CARDIOVASCULAR PLACEHOLDER
# =========================================================================
elif app_mode == "6. Advanced Clinical Diagnostics (Coming Soon)":
    st.title("🔮 Phase 2: Advanced Clinical Diagnostics")
    st.info("Once you finish refining your general wellness metrics, this module is reserved for parsing advanced blood biomarkers, lipids, and calculating 10-year ASCVD hazard ratios.")
