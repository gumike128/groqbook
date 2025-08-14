import streamlit as st
from groq import Groq
import json
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ['GROQ_API_KEY']

if 'api_key' not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY

if 'groq' not in st.session_state:
    if GROQ_API_KEY:
        st.session_state.groq = Groq()

class GenerationStatistics:
    def __init__(self, input_time=0,output_time=0,input_tokens=0,output_tokens=0,total_time=0,model_name="llama3-8b-8192"):
        self.input_time = input_time
        self.output_time = output_time
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_time = total_time
        self.model_name = model_name

    def get_input_speed(self):
        if self.input_time != 0:
            return self.input_tokens / self.input_time
        else:
            return 0
    
    def get_output_speed(self):
        if self.output_time != 0:
            return self.output_tokens / self.output_time
        else:
            return 0
    
    def add(self, other):
        if not isinstance(other, GenerationStatistics):
            raise TypeError("Možno pridať iba objekty typu GenerationStatistics")
        
        self.input_time += other.input_time
        self.output_time += other.output_time
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.total_time += other.total_time

    def __str__(self):
        return (f"\n## {self.get_output_speed():.2f} T/s ⚡\nCelkový čas generovania: {self.total_time:.2f}s  Model: {self.model_name}\n\n"
                f"| Metrika          | Vstup          | Výstup          | Celkom          |\n"
                f"|------------------|----------------|-----------------|-----------------|\n"
                f"| Rýchlosť (T/s)   | {self.get_input_speed():.2f}           | {self.get_output_speed():.2f}           | {(self.input_tokens + self.output_tokens) / self.total_time if self.total_time != 0 else 0:.2f}           |\n"
                f"| Tokeny           | {self.input_tokens}           | {self.output_tokens}           | {self.input_tokens + self.output_tokens}           |\n"
                f"| Čas inferencie (s)| {self.input_time:.2f}           | {self.output_time:.2f}           | {self.total_time:.2f}           |")

class Book:
    def __init__(self, structure):
        self.structure = structure
        self.contents = {title: "" for title in self.flatten_structure(structure)}
        self.placeholders = {title: st.empty() for title in self.flatten_structure(structure)}

        st.markdown("## Generujem nasledujúcu štruktúru knihy:")
        toc_columns = st.columns(4)
        self.display_toc(self.structure, toc_columns)
        st.markdown("---")

    def flatten_structure(self, structure):
        sections = []
        for title, content in structure.items():
            sections.append(title)
            if isinstance(content, dict):
                sections.extend(self.flatten_structure(content))
        return sections

    def update_content(self, title, new_content):
        try:
            self.contents[title] += new_content
            self.display_content(title)
        except TypeError:
            pass

    def display_content(self, title):
        if self.contents[title].strip():
            self.placeholders[title].markdown(f"## {title}\n{self.contents[title]}")

    def display_structure(self, structure=None, level=1):
        if structure is None:
            structure = self.structure
        
        for title, content in structure.items():
            if self.contents[title].strip():
                st.markdown(f"{'#' * level} {title}")
                self.placeholders[title].markdown(self.contents[title])
            if isinstance(content, dict):
                self.display_structure(content, level + 1)

    def display_toc(self, structure, columns, level=1, col_index=0):
        for title, content in structure.items():
            with columns[col_index % len(columns)]:
                st.markdown(f"{' ' * (level-1) * 2}- {title}")
            col_index += 1
            if isinstance(content, dict):
                col_index = self.display_toc(content, columns, level + 1, col_index)
        return col_index

    def get_markdown_content(self, structure=None, level=1):
        if structure is None:
            structure = self.structure
        
        markdown_content = ""
        for title, content in structure.items():
            if self.contents[title].strip():
                markdown_content += f"{'#' * level} {title}\n{self.contents[title]}\n\n"
            if isinstance(content, dict):
                markdown_content += self.get_markdown_content(content, level + 1)
        return markdown_content

def create_markdown_file(content: str) -> BytesIO:
    markdown_file = BytesIO()
    markdown_file.write(content.encode('utf-8'))
    markdown_file.seek(0)
    return markdown_file

def generate_book_structure(prompt: str):
    completion = st.session_state.groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "Write in JSON format:\n\n{\"Názov sekcie\":\"Popis sekcie\",\n\"Názov sekcie\":{\"Názov podsekcie\":\"Popis podsekcie\"}}"
            },
            {
                "role": "user",
                "content": f"Napíš komplexnú štruktúru knihy bez úvodu a záveru (predhovor, poznámka autora, zhrnutie) pre rozsiahlu (>300 strán) knihu na tému:\n\n<subject>{prompt}</subject>\nGeneruj štruktúru v slovenčine."
            }
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    usage = completion.usage
    statistics_to_return = GenerationStatistics(input_time=usage.prompt_time, output_time=usage.completion_time, input_tokens=usage.prompt_tokens, output_tokens=usage.completion_tokens, total_time=usage.total_time,model_name="llama3-70b-8192")

    return statistics_to_return, completion.choices[0].message.content

def generate_section(prompt: str):
    stream = st.session_state.groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "Si expert na písanie kníh. Vygeneruj dlhú, komplexnú, štruktúrovanú kapitolu pre danú sekciu. Generuj obsah v slovenčine."
            },
            {
                "role": "user",
                "content": f"Vygeneruj dlhú, komplexnú, štruktúrovanú kapitolu pre nasledujúcu sekciu:\n\n<section_title>{prompt}</section_title>\nGeneruj obsah v slovenčine."
            }
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in stream:
        tokens = chunk.choices[0].delta.content
        if tokens:
            yield tokens
        if x_groq := chunk.x_groq:
            if not x_groq.usage:
                continue
            usage = x_groq.usage
            statistics_to_return = GenerationStatistics(input_time=usage.prompt_time, output_time=usage.completion_time, input_tokens=usage.prompt_tokens, output_tokens=usage.completion_tokens, total_time=usage.total_time,model_name="llama3-8b-8192")
            yield statistics_to_return

if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

if 'button_text' not in st.session_state:
    st.session_state.button_text = "Generovať knihu"

if 'statistics_text' not in st.session_state:
    st.session_state.statistics_text = ""

st.write("""
# Groqbook: Generuj celé knihy v slovenčine pomocou Llama3 (8b a 70b) na Groq
"""
)

def disable():
    st.session_state.button_disabled = True

def enable():
    st.session_state.button_disabled = False

def empty_st():
    st.empty()

try:
    if st.button('Ukonči generovanie a stiahni knihu'):
        if "book" in st.session_state:
            markdown_file = create_markdown_file(st.session_state.book.get_markdown_content())
            st.download_button(
                label='Potvrdiť stiahnutie',
                data=markdown_file,
                file_name='vygenerovana_kniha.txt',
                mime='text/plain'
            )
        else:
            raise ValueError("Najskôr vygeneruj obsah knihy, až potom môžeš stiahnuť súbor.")

    with st.form("groqform"):
        topic_text = st.text_input("O čom má byť kniha?", "")

        submitted = st.form_submit_button(st.session_state.button_text,on_click=disable,disabled=st.session_state.button_disabled)
        
        placeholder = st.empty()
        def display_statistics():
            with placeholder.container():
                if st.session_state.statistics_text:
                    if "Generujem štruktúru na pozadí" not in st.session_state.statistics_text:
                        st.markdown(st.session_state.statistics_text+"\n\n---\n")
                    else:
                        st.markdown(st.session_state.statistics_text)
                else:
                    placeholder.empty()

        if submitted:
            if len(topic_text)<10:
                raise ValueError("Téma knihy musí mať aspoň 10 znakov.")

            st.session_state.button_disabled = True
            st.session_state.statistics_text = "Generujem štruktúru na pozadí...."
            display_statistics()

            if not GROQ_API_KEY:
                st.session_state.groq = Groq(api_key=groq_input_key)

            large_model_generation_statistics, book_structure = generate_book_structure(topic_text)

            total_generation_statistics = GenerationStatistics(model_name="llama3-8b-8192")

            try:
                book_structure_json = json.loads(book_structure)
                book = Book(book_structure_json)
                
                if 'book' not in st.session_state:
                    st.session_state.book = book

                print(json.dumps(book_structure_json, indent=2))
                st.session_state.book.display_structure()

                def stream_section_content(sections):
                    for title, content in sections.items():
                        if isinstance(content, str):
                            content_stream = generate_section(title+": "+content)
                            for chunk in content_stream:
                                chunk_data = chunk
                                if (type(chunk_data)==GenerationStatistics):
                                    total_generation_statistics.add(chunk_data)
                                    st.session_state.statistics_text = str(total_generation_statistics)
                                    display_statistics()
                                elif chunk!=None:
                                    st.session_state.book.update_content(title, chunk)
                        elif isinstance(content, dict):
                            stream_section_content(content)

                stream_section_content(book_structure_json)
            
            except json.JSONDecodeError:
                st.error("Nepodarilo sa dekódovať štruktúru knihy. Skús to znova.")

            enable()

except Exception as e:
    st.session_state.button_disabled = False
    st.error(e)

    if st.button("Vyčistiť"):
        st.rerun()
