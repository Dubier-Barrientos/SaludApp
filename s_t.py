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

    st.title("¡Atrévete a escribir tu historia!")
    
    text = st.text_input("¿Tienes algo para contar?")
    tld="es"

    def text_to_speech(text, tld):
        tts = gTTS(text,"es", tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, text

    
    if st.button("convertir"):
        result, output_text = text_to_speech(text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        #if display_output_text:
        st.markdown(f"## Texto en audio:")
        st.write(f" {output_text}")


    st.subheader("¡También puedes traducirla!")
    
    result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            st.write(result.get("GET_TEXT"))
        try:
            os.mkdir("temp")
        except:
            pass
        st.title("Texto a Audio")
        translator = Translator()
    
    text = str(result.get("GET_TEXT"))
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Italiano"),
    )
    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
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
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Italiano"),
    )
    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"
    elif out_lang == "Italiano":
        output_language = "it"   
    
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto",
            "Español",
            "Reino Unido",
            "Estados Unidos",
            "Canada",
            "Australia",
            "Irlanda",
            "Sudáfrica",
        ),
    )

     def text_translate(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    if st.button("Traducir"):
        result, output_text = text_translate(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown(f"## Texto de salida:")
            st.write(f" {output_text}")
    
    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)

    remove_files(7)
    
elif selected_page == "Dibujemos una historia":
    
    #Título de la sección
    st.title("¡Aquí puedes dibujar la historia que te imagines!")

    #Cambiar trazo y color
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    
    st.subheader("Lienzo de Dibujo")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",  # Color de fondo transparente
        stroke_width=stroke_width,  # Grosor de la línea
        stroke_color=stroke_color,  # Color de línea (negro)
        background_color="#FFF",  # Color de fondo blanco
        drawing_mode="freedraw",  # Modo de dibujo libre
        key="canvas",
        height=300  # Altura del lienzo de dibujo
    )
    
    
    if st.button("Guardar Dibujo"):
        image_data = canvas_result.image_data
        if image_data is not None:
            image = Image.fromarray(np.uint8(image_data))
    
            new_size = (300, 300)
            image = image.resize(new_size)
            
            historieta.append(image)
    
            st.image(image, use_column_width=True, caption=f"Imagen {len(historieta)}")
    
            if st.button(f"Borrar Imagen {len(historieta)}"):
                del historieta[-1]
                st.success(f"Imagen {len(historieta) + 1} borrada.")
        else:
            st.warning("No hay dibujo para guardar.")
    
    if st.button("Borrar Todas las Imágenes"):
        historieta.clear()
        st.success("Todas las imágenes borradas.")








            

           


        
    


