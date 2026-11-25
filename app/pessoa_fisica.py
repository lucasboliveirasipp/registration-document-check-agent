import json
import streamlit as st  
from .agent_tools import analisar_formulario, analisar_documento_identificacao, analisar_rec_cartorio
from .analisys_form import show_analisys_pf
from .show_form import show_form
from .tools import format_cpf_cnpj, only_numbers

def page_pessoa_fisica():    
    with st.container(border=True):
        id_doc_uploader = st.file_uploader(
            "Documentos de identificação:", type=['pdf', 'png', 'jpeg'],
            accept_multiple_files=True,
            key="pf_doc"
        )

        formulario_uploader = st.file_uploader(
            "Formulário:", type=['pdf', 'png', 'jpeg'],
            key="pf_form"
        )

        rec_cart = st.checkbox("Reconhecimento em cartório")

        if rec_cart:
            reconhecimento_uploader = st.file_uploader(
                "Reconhecimento em cartório:", type=['pdf', 'png', 'jpeg'],
                key="pf_rc"
            )

        if st.button("Enviar documentos", type="secondary", disabled=False):    
            formulario = {}
            documentos_identificacao = {}    
            reconhecimento_cart_response = []

            for doc in id_doc_uploader:
                documento = analisar_documento_identificacao(doc)                
                documentos_identificacao[only_numbers(documento.cpf)] = documento
            
            if formulario_uploader:
                formulario = analisar_formulario(formulario_uploader)                               

            if rec_cart and reconhecimento_uploader: 
                reconhecimento_cart_response = analisar_rec_cartorio(reconhecimento_uploader)                       

            if documentos_identificacao:
                with st.container(border=True):
                    st.markdown("**Documentos de identificação**")
                    for key in documentos_identificacao:
                        doc = documentos_identificacao[key]                
                        st.markdown(f"**Nome:** {doc.nome.title()}<br>**CPF:** {format_cpf_cnpj(doc.cpf)}<br>**Data de Nascimento:** {doc.data_nascimento}<br>", unsafe_allow_html=True)     
                                                                
            if reconhecimento_cart_response:
                with st.container(border=True):
                    st.markdown("**Dados do reconhecimento em cartório**")                    
                    firma = json.loads(reconhecimento_cart_response)                    

                    if firma['nomes'] is None:
                        firma['nomes'] = ["Não identificado."]

                    if firma['cartorio'] is None:
                        firma['cartorio'] = "Não identificado."
                        
                    if firma['escrevente'] is None:                    
                        firma['escrevente'] = "Não identificado."
                    
                    if firma['codigo_autenticacao'] is None:
                        firma['codigo_autenticacao'] = ["Não identificado."]     

                    st.write("**Autenticações:**")                    
                    for x in firma['nomes']:                        
                        st.markdown(" - "+x.title())
                    st.write(f"**Cartório:** {firma['cartorio']}")
                    st.write(f"**Escrevente:** {firma['escrevente']}")
                    st.write("**Códigos de autenticação:**")
                    for x in firma['codigo_autenticacao']:                        
                        st.markdown(" - "+x)

            show_form(formulario)
            show_analisys_pf(formulario, documentos_identificacao)
            
