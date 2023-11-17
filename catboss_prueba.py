import streamlit as st
import pandas as pd
import pickle
from catboost import Pool
import random

# Cargar el modelo desde el archivo .pickle
with open(r'modelo_catboost.pickle', 'rb') as file:
    loaded_model = pickle.load(file)

# Función para predecir la probabilidad
def predecir_probabilidad(datos):
    # Crear un DataFrame con los datos ingresados
    nuevos_datos = pd.DataFrame([datos])
    # st.dataframe(nuevos_datos)
    # Realizar la predicción de probabilidad
    pool_nuevos_datos = Pool(data=nuevos_datos, cat_features=cat_features)
    probabilidad = loaded_model.predict_proba(pool_nuevos_datos)[:, 1]
    return probabilidad[0]

# Lista de características categóricas
cat_features = ['NOMBRE_PRODUCTO', 'DESCRIPCION_FORMA_PAGO', 'MARCA_SINIESTROS',
                'GENERO FINAL', 'DEDUCIBLE FINAL', 'BONUS MALUS FINAL', 'TIPO_SUCURSAL',
                'MARCA_FINAL', 'DEPARTAMENTO_FINAL', 'COMISION']


df = pd.read_excel("X.xlsx")
columns = df.columns.tolist()

lista_nombre_producto = df['NOMBRE_PRODUCTO'].unique().tolist()
lista_descripcion_forma_pago = df['DESCRIPCION_FORMA_PAGO'].unique().tolist()
lista_marca_siniestros = df['MARCA_SINIESTROS'].unique().tolist()
lista_genero = df['GENERO FINAL'].unique().tolist()
lista_deducible = df['DEDUCIBLE FINAL'].unique().tolist()
lista_bonus_malus = df['BONUS MALUS FINAL'].unique().tolist()
lista_tipo_sucursal = df['TIPO_SUCURSAL'].unique().tolist()
lista_marca_final = df['MARCA_FINAL'].unique().tolist()
lista_departamento_final = df['DEPARTAMENTO_FINAL'].unique().tolist()
lista_comision = df['COMISION'].unique().tolist()



# Configurar la aplicación Streamlit
def main():
    st.title("Aplicación de Predicción de Probabilidad de Retención")
    
    st.sidebar.markdown("## Bienvenido a ProbaRetain")
    st.sidebar.markdown(":smile: Ingrese los datos del cliente para predecir la probabilidad de retención de la póliza de seguro de automóvil en la compañía de seguros")
    

    cols = st.columns([0.2 for x in range(5)])
    
    # Capturar los datos de entrada
    nombre_producto = cols[0].selectbox("NOMBRE_PRODUCTO:", lista_nombre_producto, index=random.randint(0, len(lista_nombre_producto)-1))
    comision = cols[1].selectbox("COMISION:", lista_comision, index=random.randint(0, len(lista_comision)-1))
    forma_pago = cols[2].selectbox("DESCRIPCION_FORMA_PAGO:", lista_descripcion_forma_pago, index=random.randint(0, len(lista_descripcion_forma_pago)-1))
    valor_asegurado = cols[3].number_input("VALOR_ASEGURADO:", value=random.randint(0, 1000000000))
    modelo = cols[4].text_input("MODELO:", value=random.randint(2000, 2023))
    
    cantidad_renovacion = cols[0].number_input("CANTIDAD_RENOVACION:", value=0, disabled=True)
    marca_siniestros = cols[1].selectbox("MARCA_SINIESTROS:", lista_marca_siniestros, index=random.randint(0, len(lista_marca_siniestros)-1))
    genero = cols[2].selectbox("GENERO FINAL:", lista_genero, index=random.randint(0, len(lista_genero)-1))
    edad = cols[3].number_input("EDAD FINAL:", value=random.randint(18, 100))
    deducible = cols[4].selectbox("DEDUCIBLE FINAL:", lista_deducible, index=random.randint(0, len(lista_deducible)-1))
    
    bonus_malus = cols[0].selectbox("BONUS MALUS FINAL:", lista_bonus_malus, index=random.randint(0, len(lista_bonus_malus)-1))
    score = cols[1].number_input("SCORE:", value=random.randint(162, 250))
    prima = cols[2].number_input("Prima:", value=random.randint(241000, 5738000))
    incremento = cols[3].number_input("Incremento:", value=random.randint(-52, 174)/100)
    tipo_sucursal = cols[4].selectbox("TIPO_SUCURSAL:", lista_tipo_sucursal, index=random.randint(0, len(lista_tipo_sucursal)-1))
    
    marca_final = cols[0].selectbox("MARCA_FINAL:", lista_marca_final, index=random.randint(0, len(lista_marca_final)-1))
    departamento = cols[1].selectbox("DEPARTAMENTO_FINAL:", lista_departamento_final, index=random.randint(0, len(lista_departamento_final)-1))

    # Crear un diccionario con los datos ingresados
    datos_ingresados = {
        'NOMBRE_PRODUCTO': nombre_producto,
        'COMISION': comision,
        'DESCRIPCION_FORMA_PAGO': forma_pago,
        'VALOR_ASEGURADO': valor_asegurado,
        'MODELO': modelo,
        'CANTIDAD_RENOVACION': cantidad_renovacion,
        'MARCA_SINIESTROS': marca_siniestros,
        'GENERO FINAL': genero,
        'EDAD FINAL': edad,
        'DEDUCIBLE FINAL': deducible,
        'BONUS MALUS FINAL': bonus_malus,
        'SCORE': score,
        'Prima': prima,
        'Incremento': incremento,
        'TIPO_SUCURSAL': tipo_sucursal,
        'MARCA_FINAL': marca_final,
        'DEPARTAMENTO_FINAL': departamento
    }
    
    df = pd.DataFrame([datos_ingresados])
    st.dataframe(df, use_container_width=True)

    # Realizar la predicción al hacer clic en el botón
    if st.button("Predecir Probabilidad", key='predict', help="Predecir la probabilidad de retención", type="primary"):
        probabilidad_retencion = predecir_probabilidad(datos_ingresados)
        st.success(f"La probabilidad de retención es: {probabilidad_retencion:.2%}")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="ProbaRetain", page_icon=":bar_chart:", initial_sidebar_state="expanded")
    main()
