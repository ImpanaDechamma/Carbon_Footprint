import streamlit as st
import requests
import pandas as pd
import datetime

st.title("🌍 Carbon Footprint Dashboard")

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []

if "time_history" not in st.session_state:
    st.session_state.time_history = []

st.subheader("📊 Future Prediction")

if st.button("Predict Future Emission"):
    try:
        response = requests.get("http://127.0.0.1:5000/predict")

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            st.subheader("🔮 Prediction Result")
            st.dataframe(df)

            if st.session_state.result:
                current = st.session_state.result.get("carbon_emission", 0)
                future_avg = df["carbon_emission"].mean()

                st.subheader("📊 Comparison")

                st.write(f"Current Emission: {current}")
                st.write(f"Average Future Emission: {future_avg}")

                if future_avg > current:
                    st.warning("⚠️ Emissions may increase in future!")
                else:
                    st.success("✅ Emissions are expected to decrease.")

        else:
            st.error("Error fetching prediction")

    except:
        st.error("Backend not running!")

st.subheader("🧾 Input-based Calculation")

energy = st.number_input("Enter Energy (kWh):", min_value=0.0)

if st.button("Calculate Carbon Footprint"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict_input",
            json={"energy_kwh": energy}
        )

        if response.status_code == 200:
            result = response.json()
            st.session_state.result = result

            carbon = result.get("carbon_emission", 0)

            # store history
            st.session_state.history.append(carbon)
            st.session_state.time_history.append(datetime.datetime.now())

        else:
            st.error("Error in calculation")

    except:
        st.error("Backend not running!")

if st.session_state.result:
    result = st.session_state.result

    st.subheader("🌱 Carbon Footprint Result")

    carbon_value = result.get("carbon_emission", 0)

    st.metric("Carbon Emission (kg CO2)", carbon_value)

    if carbon_value > 50:
        st.error("⚠️ High Carbon Emission!")
    else:
        st.success("✅ Emission is under control")

    st.subheader("💡 Suggestions to Reduce Emission")

    if carbon_value > 80:
        st.warning("Reduce server load, optimize CPU usage, and use energy-efficient hardware.")
    elif carbon_value > 40:
        st.info("Consider optimizing applications and reducing unnecessary processes.")
    else:
        st.success("Great! Your system is energy efficient.")

    data = pd.DataFrame({
        "Server": ["S1"],
        "Energy (kWh)": [energy],
        "Carbon (kg CO2)": [carbon_value]
    })

    st.subheader("📊 Server Data")
    st.dataframe(data)

st.subheader("📈 Emission Trend")

if len(st.session_state.history) > 0:
    chart_data = pd.DataFrame({
        "Time": st.session_state.time_history,
        "Carbon": st.session_state.history
    })

    chart_data = chart_data.set_index("Time")

    st.line_chart(chart_data)
else:
    st.info("No data yet. Enter values and calculate.")

if st.button("Reset Data"):
    st.session_state.history = []
    st.session_state.time_history = []
    st.session_state.result = None
    st.success("Data reset!")