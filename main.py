from PyPDF2 import PdfReader
from gtts import gTTS
from googletrans import Translator
import streamlit as st
import os
import base64

translator = Translator()

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<p class="big-font">PDF to Audiobook Converter</p>""", unsafe_allow_html=True)
st.image('pdf_to_mp3.jpg')
st.markdown("""
<b>Directions: </b><ul>
<li>Select Language.</li>
<li>Upload PDF.</li>
<li>Save mp3 file of translation.</li>
""", unsafe_allow_html=True)

language_select = st.multiselect('Language:', options=['en', 'es', 'de', 'fr'])
pdf_file = st.file_uploader('Upload PDF', type='pdf')


# Open the PDF file
def analyze_pdf(pdf_file):
    st.write('Converting PDF to text . . .')
    pdf = PdfReader(pdf_file)
    extracted_text = []

    # Loop through all the pages
    for page in range(len(pdf.pages)):
        page = pdf.pages[page]

        # Extract the text from the page
        text = page.extract_text()
        st.write(language_select)
        st.write(language_select[0])
        translation = translator.translate(text, dest=language_select[0])
        extracted_text.append(translation.text)
    text_str = ' '.join(extracted_text)
    text_to_speech(text_str)


# Create HTML link to download mp3 file
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


# Convert text to speech
def text_to_speech(pdf_text):
    st.write('Converting text to audio . . .')
    voice_obj = gTTS(text=pdf_text, lang=language_select[0], tld='co.uk', slow=False)
    file_name = f"{pdf_file.name}_to_audio.mp3"
    voice_obj.save(file_name)
    st.audio(file_name, format='audio/ogg')
    st.markdown(get_binary_file_downloader_html(file_name, 'Audiobook'), unsafe_allow_html=True)


if __name__ == '__main__':
    if pdf_file is not None:
        analyze_pdf(pdf_file)

st.write('Author: [Tyler Gargula](https://tylergargula.dev) | Technical SEO & Software Developer')
