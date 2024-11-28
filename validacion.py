# validacion.py
import pandas as pd
from historial import crearHistorial

def validar(df_corregido, selected_rows):

    # Combina las columnas que quieres usar como identificadores
    cols_identificadores = ["Codigo", "entrada/salida", "rut", "hora", "minuto", "mes", "día", "año", "Error"]

    # Filtra el DataFrame para obtener las filas que coincidan
    indices = []
    for _, selected_row in selected_rows.iterrows():
        mask = (df_corregido[cols_identificadores] == selected_row[cols_identificadores]).all(axis=1)
        indices.extend(df_corregido[mask].index.tolist())

    print("Indices: ", indices)

    try:

        df = df_corregido

        for i in indices:

            # Acceder a los valores actuales en la columna 'Error'
            errores = df.loc[i, 'Error']

            if (errores != "Ok"):        
                lista_errores = errores.split(", ")

                for error in lista_errores:
                    if error == "Entrada duplicada":
                        print("Se revierte ENTRADA DUPLICADA")

                        # Verificar si existe la fila siguiente y eliminarla
                        if i + 1 in df.index and df.at[i + 1, 'Error'] == "Salida creada por duplicado":
                            print(f"Eliminando fila {i + 1} (Salida que sigue a la Entrada duplicada)")
                            df.drop(index=i + 1, inplace=True)

                            # Si la fila siguiente está en `indices`, eliminarla de la lista
                            if i + 1 in indices:
                                indices.remove(i + 1)
    
                    elif error == "Salida duplicada":
                        print("Se revierte SALIDA DUPLICADA")

                        # Verificar si existe la fila anterior y eliminarla
                        if i - 1 in df.index and df.at[i - 1, 'Error'] == "Salida creada por duplicado":
                            print(f"Eliminando fila {i - 1} (Salida que sigue a la Entrada duplicada)")
                            df.drop(index=i - 1, inplace=True)

                        # Si la fila anterior está en `indices`, eliminarla de la lista
                        if i - 1 in indices:
                            indices.remove(i - 1)

                    elif error == "Salida automatica corregida":
                        print("Se revierte correcion SALIDA AUTOMATICA")

                        df.at[i, 'hora'] = "00"
                        df.at[i, 'minuto'] = "00"
                        df.at[i, 'Hora'] = "00:00"      
                        df.at[i, "día"] += 1
                        
                    elif error == "Salida invertida a entrada":
                        print("Se revierte SALIDA INVERTIDA A ENTRADA")

                        df.at[i, 'entrada/salida'] = 3
                    
                    elif error == "Entrada invertida a salida":
                        print("Se revierte ENTRADA INVERTIDA A SALIDA")

                        df.at[i, 'entrada/salida'] = 1
                    
                    elif error == "Entrada creada por duplicado":
                        print("Se eliminara ENTRADA CREADA POR DUPLICADO")

                        # Si la fila siguiente no está en `indices`, agregarla a la lista
                        if i + 1 not in indices:
                            indices.add(i + 1)

                    elif error == "Salida creada por duplicado":
                        print("Se eliminara SALIDA CREADA POR DUPLICADO")

                        # Si la fila anterior no está en `indices`, agregarla a la lista
                        if i - 1 not in indices:
                            indices.add(i - 1)

                df.at[i, 'Error'] = "Correciones revertidas"

    
        crearHistorial(df_corregido, indices)               
        
        return df
    
    except Exception as e:
        print(f"Error en el proceso de correcion: {e}")
    