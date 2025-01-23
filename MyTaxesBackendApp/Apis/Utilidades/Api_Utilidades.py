import os
from pydub import AudioSegment
import speech_recognition as sr
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..Seguridad.obtener_datos_token import obtener_datos_token
from ..Seguridad.Validaciones import validacionpeticion
from word2number_es import w2n
import time
from datetime import datetime
from MyTaxesBackendApp.Serializadores.MesesSerializers import *
# Configurar FFmpeg para pydub
# AudioSegment.ffmpeg = "D:\\Programas\\ffmpeg\\bin\\ffmpeg.exe"  # Ruta de FFmpeg
# AudioSegment.ffmpeg = "/usr/bin/ffmpeg"

if os.name == 'nt':  # 'nt' es para Windows
    AudioSegment.ffmpeg = "D:\\Programas\\ffmpeg\\bin\\ffmpeg.exe"  # Ruta para Windows
else:
    AudioSegment.ffmpeg = "/usr/bin/ffmpeg"  # Ruta para otros sistemas operativos (Linux, macOS)
@api_view(['POST'])
def upload_audio(request):
    token_sesion, usuario, id_user = obtener_datos_token(request)
    resp = validacionpeticion(token_sesion)
    numero_palabras = {
    "cero": "0",
    "uno": "1",
    "dos": "2",
    "tres": "3",
    "cuatro": "4",
    "cinco": "5",
    "seis": "6",
    "siete": "7",
    "ocho": "8",
    "nueve": "9"
}
    if resp is True:
        if 'audio' not in request.FILES:
            return Response({"error": "No se encontró el archivo 'audio' en la solicitud"}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = request.FILES['audio']
        
        if not audio_file.name.endswith(('.m4a', '.wav', '.mp3', '.ogg', '.flac')):
            return Response({"error": "Formato de archivo no soportado. Use M4A, WAV, MP3, OGG o FLAC."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Crear la carpeta Temp si no existe
            temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Ruta para el archivo original m4a
            original_file_path = os.path.join(temp_dir, audio_file.name)
            
            # Guardar el archivo m4a
            with open(original_file_path, "wb+") as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Convertir m4a a wav usando pydub
            if audio_file.name.endswith('.m4a'):
                audio = AudioSegment.from_file(original_file_path, format='m4a')
                wav_file_path = original_file_path.replace('.m4a', '.wav')
                audio.export(wav_file_path, format="wav")
            else:
                wav_file_path = original_file_path

            # Transcribir el audio
            recognizer = sr.Recognizer()
            # with sr.AudioFile(wav_file_path) as source:
            #     audio = recognizer.record(source)
            #     try:
            #         transcription = recognizer.recognize_google(audio, language='es-ES')  # Cambiar idioma si es necesario
            #         transcription=transcription.replace('.', '')
            #         transcription=transcription.replace(',', '')
            #         words = transcription.split()
            #         print(words)
            #         for i, word in enumerate(words):
            #             try:
                            
            #                 words[i] = str(w2n.word_to_num(word))
            #             except ValueError:
            #                 print(f"Palabra no convertible: {word}")
                    
            #         # Unir las palabras convertidas en la transcripción final
            #         transcription = "".join(words)
            #         print("Transcripción modificada:", transcription)
            #     except sr.UnknownValueError:
            #         transcription = "No se pudo entender el audio"
            #     except sr.RequestError as e:
            #         transcription = f"Error con el servicio de reconocimiento: {str(e)}"

            with sr.AudioFile(wav_file_path) as source:
                audio = recognizer.record(source)
                try:
                    transcription = recognizer.recognize_google(audio, language='es-ES')  # Cambiar idioma si es necesario
                    transcription=transcription.replace('.', '')
                    transcription=transcription.replace(',', '')
                    words = transcription.split()
                    converted_numbers = []
                    temp_group = []
                    
                    
                    for word in words:
                        if word in numero_palabras:
                            # Si es un dígito individual (0-9), lo agregamos como está
                            if temp_group:
                                # Procesar cualquier número acumulado en el grupo
                                try:
                                    converted_numbers.append(str(w2n.word_to_num(" ".join(temp_group))))
                                except ValueError:
                                    converted_numbers.extend(temp_group)
                                temp_group = []
                            converted_numbers.append(numero_palabras[word])
                        else:
                            # Acumular palabras que podrían formar un número compuesto
                            temp_group.append(word)

                    # Procesar el último grupo si existe
                    if temp_group:
                        try:
                            converted_numbers.append(str(w2n.word_to_num(" ".join(temp_group))))
                        except ValueError:
                            converted_numbers.extend(temp_group)
                                        




                    transcription = "".join(converted_numbers)
                    
                except sr.UnknownValueError:
                    transcription = "No se pudo entender el audio"
                except sr.RequestError as e:
                    transcription = f"Error con el servicio de reconocimiento: {str(e)}"

            
            
            return Response({
                'mensaje': 'Archivo subido y transcrito exitosamente',
                'transcripcion': transcription
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al procesar el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({'mensaje': 'Token no válido'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def prueba_transcripcion(request):
    token_sesion, usuario, id_user = obtener_datos_token(request)
    resp = validacionpeticion(token_sesion)
    
    if resp is True:
        try:
            # Ruta del archivo de audio
            original_file_path = r'D:\Trabajos\Proyectos\MyTaxes\Backend\MyTaxesBackendProjects\MyTaxesBackendApp\Temp\audio-recording.m4a'
            
            # Convertir el archivo m4a a wav
            audio = AudioSegment.from_file(original_file_path, format='m4a')
            wav_file_path = original_file_path.replace('.m4a', '.wav')
            audio.export(wav_file_path, format="wav")

            # Transcribir el audio
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file_path) as source:
                audio = recognizer.record(source)
                try:
                    transcription = recognizer.recognize_google(audio, language='es-ES')  # Cambiar idioma si es necesario
                    
                    
                    # Convertir las palabras a números usando word2number
                    words = transcription.split()
                    
                    
                    for i, word in enumerate(words):
                        try:
                            # print(f"Intentando convertir: {word}")
                            # print(w2n.word_to_num(word))
                            # print(w2n.word_to_num(word))
                            words[i] = str(w2n.word_to_num(word))
                        except ValueError:
                            # print(f"Palabra no convertible: {word}")
                            pass
                    
                    # Unir las palabras convertidas en la transcripción final
                    transcription = "".join(words)
                    
                    
                except sr.UnknownValueError:
                    transcription = "No se pudo entender el audio"
                except sr.RequestError as e:
                    transcription = f"Error con el servicio de reconocimiento: {str(e)}"

            return Response({
                'mensaje': 'Archivo subido y transcrito exitosamente',
                'transcripcion': transcription
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al procesar el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response({'mensaje': 'Token no válido'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def registromeses(request):

    data_list = []
    data_errores=''
    n=1
    while n < 13:
        if n==1: nombremes='Enero'
        if n==2: nombremes='Febrero'
        if n==3: nombremes='Marzo'
        if n==4: nombremes='Abril'
        if n==5: nombremes='Mayo'
        if n==6: nombremes='Junio'
        if n==7: nombremes= 'Julio'
        if n==8: nombremes='Agosto'
        if n==9: nombremes='Septiembre'
        if n==10: nombremes='Octubre'
        if n==11: nombremes='Noviembre'
        if n==12: nombremes='Diciembre'

        datasave={
            "id":  0,
            "numero_mes": n,
            "nombre_mes":nombremes,
            "fecha_registro": datetime.now()
            
        }
        data_list.append(datasave)
        
        meses_serializer=MesesSerializers(data=datasave)
        n=n+1
        if meses_serializer.is_valid():
            meses_serializer.save()
        else:
            return Response({'error':meses_serializer.errors},status= status.HTTP_400_BAD_REQUEST)