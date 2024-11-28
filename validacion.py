# validacion.py
import pandas as pd
from historial import crearHistorial, guardarHistorial

def validar(df_corregido, indices):

    try:

        df = df_corregido
        historial = pd.DataFrame()

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

                        # No hace falta verificar

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


                # Si es una respuesta por duplicado no se guarda en el historial, pues no es la acción
                if lista_errores[0] != "Entrada creada por duplicado" or lista_errores[0] != "Salida creada por duplicado":
                    
                    try:
                        # Se va agregando nuevas filas y cambios
                        nuevo_historial = crearHistorial(df.at[i, 'rut'], lista_errores)
                    except Exception as e:
                        print(f"Error al crear historial: {e}")
                    
                    historial = pd.concat([historial, nuevo_historial], ignore_index=True)

                df.at[i, 'Error'] = "Correciones revertidas"
        
        guardarHistorial(historial)
        
        return df
    
    except Exception as e:
        print(f"Error en el proceso de correcion: {e}")
    