import pandas as pd
import numpy as np

import gradio as gr

import os


def obtener_fechas_creacion(archivo):
    stat = os.stat(archivo)
    return pd.to_datetime(stat.st_ctime, unit='s').date()

def contar_archivos_por_dia(carpeta):
    carpeta='../images/'
    archivos = [os.path.join(carpeta, archivo) for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo))]
    fechas_creacion = [obtener_fechas_creacion(archivo) for archivo in archivos]
    conteo_por_dia = pd.Series(fechas_creacion).value_counts().sort_index()
    #print(ccdonteo_por_dia)
    df = pd.DataFrame({'fecha': conteo_por_dia.index, 'y': conteo_por_dia.values})
    df['fecha'] = df['fecha'].astype(str)
    df['x1'] = range(1, len(df) + 1)
    df['x'] = df['fecha']
    return df

demo = gr.Blocks()

with demo:
    gr.Markdown("# Dark room Rembrandt")
    gr.Markdown("Histograma de creación de archivos ")
  

    with gr.Row():
        #carpeta_input = gr.Textbox(label="Ruta de la carpeta", placeholder="Introduce la ruta de la carpeta")
        
        output = gr.BarPlot(
            x="x",
            y="y",
            width=700,
            height=300,
        )
    btn = gr.Button(value="Run")
    btn.click(contar_archivos_por_dia,None ,output)

if __name__ == "__main__":
    demo.launch()
