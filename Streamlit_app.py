import streamlit as st

# Titre de l'application
st.title("Dashboard des Accidents de Voiture")
import pandas as pd
import numpy as np
import plotly as pt

# Simuler des données
np.random.seed(0)
dates = pd.date_range('2015-01-01', periods=2000, freq='D')
data = {
    'Date': dates,
    'Accidents': np.random.poisson(2, size=len(dates)),
    'Weather_Condition': np.random.choice(['Clear', 'Rainy', 'Snowy', 'Foggy'], size=len(dates)),
    'Weekend': (dates.weekday >= 5).astype(int)
}
df = pd.DataFrame(data)

# Convertir 'Date' en index datetime
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Ajouter des colonnes pour l'année, le mois, et le jour de la semaine
df['Year'] = df.index.year
df['Month'] = df.index.month
df['Weekday'] = df.index.weekday

print(df.head())

# Sélectionner l'année
selected_year = st.selectbox('Sélectionner l\'année:', df['Year'].unique())

# Filtrer les données en fonction de l'année sélectionnée
filtered_df = df[df['Year'] == selected_year]

import plotly.express as px

# Graphique de tendance mensuelle
st.subheader('Nombre mensuel d\'accidents')
monthly_accidents = filtered_df.resample('M')['Accidents'].sum()
fig_monthly_trend = px.line(monthly_accidents, x=monthly_accidents.index, y='Accidents', title='Nombre mensuel d\'accidents')
st.plotly_chart(fig_monthly_trend)

st.subheader('Accidents par condition météorologique')
weather_condition_pivot = filtered_df.pivot_table(values='Accidents', index='Weather_Condition', aggfunc='mean')
fig_weather_condition = px.bar(weather_condition_pivot, x=weather_condition_pivot.index, y='Accidents', title='Accidents par condition météorologique')
st.plotly_chart(fig_weather_condition)

# Graphique des accidents par jour de la semaine
st.subheader('Accidents par jour de la semaine')
weekday_accidents = filtered_df.groupby('Weekday')['Accidents'].mean()
fig_weekday_accidents = px.bar(weekday_accidents, x=weekday_accidents.index, y='Accidents', title='Accidents par jour de la semaine')
fig_weekday_accidents.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        ticktext=['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    )
)
st.plotly_chart(fig_weekday_accidents)

# Détecter les jours avec un nombre anormalement élevé d'accidents
daily_mean = df['Accidents'].mean()
daily_std = df['Accidents'].std()
anomalies = df[df['Accidents'] > daily_mean + 3 * daily_std]
st.subheader('Jours avec un nombre anormalement élevé d\'accidents')
st.write(anomalies)

#sns.scatterplot(data=df,x="sepal_length",y="petal_length", hue = "Weather_Condition", size="petal_length", markers="+")


