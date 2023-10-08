import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
import numpy as np
import os
import time
import glob
import os
from gtts import gTTS
from googletrans import Translator

try:
    os.mkdir("temp")
except:
    pass

historieta = []

st.set_page_config(
    page_title="Creación de Historieta",
    page_icon="✏️",
    layout="wide"
)

selected_page = st.sidebar.radio("Selecciona una opción:", ["Historia a audio", "Dibujemos una historia"])

if selected_page == "Historia a audio":

    st.markdown("<h1 style='text-align: center; color: blue;'>¡Atrévete a contar tu historia!</h1>", unsafe_allow_html=True)
    
    image_writing = Image.open('gatito_escribiendo.gif')
    #.image(image_writing)

    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(image_writing)

    # Texto de entrada del usuario
    text = st.text_input("¿Tienes algo para contar?")
    tld = "es"
    
    # Función para convertir texto a audio
    def text_to_speech(text, tld):
        tts = gTTS(text, "es", tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, text
    
    # Botón para convertir texto a audio
    if st.button("Convertir a Audio"):
        result, output_text = text_to_speech(text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

    st.markdown(
        """
        <style>
            .divider {
                margin-top: 20px;
                margin-bottom: 20px;
                border-top: 2px solid #888;
            }
        </style>
        <div class="divider"></div>
        """
    )
    
    st.subheader("¡También puedes traducirlo!")
    
    # Resultado de la traducción
    result = text
    
    # Crea un directorio temporal para almacenar archivos de audio
    try:
        os.mkdir("temp")
    except:
        pass
    
    translator = Translator()
    
    # Idioma de entrada y salida
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés", "Italiano"),
    )
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengalí":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"
    elif in_lang == "Italiano":
        input_language = "it"
    
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés", "Italiano"),
    )
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengalí":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    elif out_lang == "Italiano":
        output_language = "it"

    display_output_text = st.checkbox("Mostrar el texto")
    
    # Botón para traducir el texto
    if st.button("Traducir"):
        translation = translator.translate(result, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = result[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
    
        # Muestra el audio traducido
        st.markdown(f"## Tú audio traducido:")
        st.audio(f"temp/{my_file_name}.mp3", format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown(f"## Texto de salida:")
            st.write(trans_text)
    
    
    # Función para eliminar archivos antiguos
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted", f)
    
    remove_files(7)
    
elif selected_page == "Dibujemos una historia":
    
    #Título de la sección
    st.title("¡Aquí puedes dibujar la historia que te imagines!")

    image_drawing = Image.open('gatito_dibujo.gif')
    #st.image(image_drawing)
    
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(image_drawing)

    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:",
        ("freedraw", "line", "rect", "circle", "transform", "point"),
    )
    if drawing_mode == "point":
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    #Cambiar trazo y color
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    
    
    st.subheader("Lienzo de Dibujo")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)", 
        stroke_width=stroke_width, 
        stroke_color=stroke_color,  
        background_color=bg_color, 
        update_streamlit=True,
        drawing_mode=drawing_mode, 
        key="canvas",
        height=300,
    )
    
    
    if st.button("Guardar imagen"):
        image_data = canvas_result.image_data
        if image_data is not None:
            image = Image.fromarray(np.uint8(image_data))
    
            # Guardar la imagen como PNG
            image.save("canvas_image.png", "PNG")
            
            # Mostrar un enlace para descargar la imagen
            st.markdown("Ya puedes descargar tu imagen:")
            st.download_button(label="Descargar", data=open("canvas_image.png", "rb").read(), file_name="canvas_image.png", key="download-button")
        else:
            st.warning("No hay dibujo para guardar.")


        






            

           


        
    


