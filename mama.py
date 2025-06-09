#!/usr/bin/env python3
# Archivo: mama.py

import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import os

# Constantes
dias_semana = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
HORA_INICIO = time(8, 30)
HORA_FIN = time(17, 0)
INTERVALO = timedelta(minutes=30)
ARCHIVO_RESERVAS = 'bookings.csv'

# Crear archivo de reservas si no existe
if not os.path.exists(ARCHIVO_RESERVAS):
    df_init = pd.DataFrame(columns=['fecha', 'hora', 'nombre', 'email', 'timestamp'])
    df_init.to_csv(ARCHIVO_RESERVAS, index=False)

# Cargar reservas existentes
reservas = pd.read_csv(ARCHIVO_RESERVAS, parse_dates=['fecha'])

st.title("Reserva tu cita")

# Selector de fecha
ohoy = date.today()
fecha_seleccionada = st.date_input(
    "Selecciona la fecha (lunes a viernes)",
    min_value=ohoy
)

# Validar día de la semana
weekday = fecha_seleccionada.weekday()
if weekday not in dias_semana:
    st.error("Por favor, elige un día entre lunes y viernes.")
    st.stop()
else:
    st.write(f"Has seleccionado: {dias_semana[weekday]} {fecha_seleccionada.strftime('%d/%m/%Y')}")

# Generar franjas horarias
tiempos = []
actual = datetime.combine(fecha_seleccionada, HORA_INICIO)
fin = datetime.combine(fecha_seleccionada, HORA_FIN)
while actual < fin:
    tiempos.append(actual.time().strftime('%H:%M'))
    actual += INTERVALO

# Filtrar horarios ya reservados
ocupados = reservas[reservas['fecha'] == pd.Timestamp(fecha_seleccionada)]['hora'].astype(str).tolist()
disponibles = [t for t in tiempos if t not in ocupados]

if not disponibles:
    st.warning("No hay horarios disponibles para este día.")
    st.stop()

horario = st.selectbox("Selecciona el horario", disponibles)

# Datos del cliente
nombre = st.text_input("Tu nombre")
email = st.text_input("Tu email")

if st.button("Reservar cita"):
    if not nombre or not email:
        st.error("Por favor, completa tu nombre y email.")
    else:
        nueva = {
            'fecha': fecha_seleccionada,
            'hora': horario,
            'nombre': nombre,
            'email': email,
            'timestamp': datetime.now()
        }
        # Añadir nueva reserva y guardar
        nueva_df = pd.DataFrame([nueva])
        reservas = pd.concat([reservas, nueva_df], ignore_index=True)
        reservas.to_csv(ARCHIVO_RESERVAS, index=False)
        st.success(f"Cita reservada para el {fecha_seleccionada.strftime('%d/%m/%Y')} a las {horario}.")
        st.balloons()
