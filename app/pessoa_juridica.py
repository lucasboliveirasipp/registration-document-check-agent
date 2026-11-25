import streamlit as st  
from PyPDF2 import PdfReader
from .agent_tools import analisar_formulario, analisar_contrato, analisar_documento_identificacao
from .analisys_form import show_analisys_pj
from .show_form import show_form
from .tools import format_cpf_cnpj, only_numbers

def page_pessoa_juridica():          
    with st.container(border=True):
        id_doc_uploader = st.file_uploader(
            "Documentos de identificação:", type=['pdf', 'png', 'jpeg'],
            accept_multiple_files=True,
            key="pj_doc"
        )
    
        formulario_uploader = st.file_uploader(
            "Formulário:", type=['pdf', 'png', 'jpeg'],
            key="pj_form"
        )

        
        with st.container(border=True):
            contrato_uploader1 = st.file_uploader(
                "1° Documento:", type=['pdf', 'png', 'jpeg'],
                accept_multiple_files=False,
                key="pj_cont1"
            )

            pg_ini_ct1 = 0
            pg_fim_ct1 = 0
            if contrato_uploader1 is not None and contrato_uploader1.name.endswith(".pdf"):
                reader = PdfReader(contrato_uploader1)
                total_paginas = len(reader.pages)                
                pg_ini_ct1, pg_fim_ct1 = st.slider("Selecione a página inicial e final:",
                        min_value=1,
                        max_value=total_paginas,
                        value=(1,total_paginas),
                        step=1,
                        key="l1")
            

            tipo_contrato1 = st.radio("Tipo 1° documento", ["Contrato Social/Ata de assembleia", "Procuração"], horizontal=True, key="tipo_contrato1")
        
        with st.container(border=True):
            contrato_uploader2 = st.file_uploader(
                "2° Documento:", type=['pdf', 'png', 'jpeg'],
                accept_multiple_files=False,
                key="pj_cont2"
            )

            pg_ini_ct2 = 0
            pg_fim_ct2 = 0
            if contrato_uploader2 is not None and contrato_uploader2.name.endswith(".pdf"):
                reader = PdfReader(contrato_uploader2)
                total_paginas = len(reader.pages)                
                pg_ini_ct2, pg_fim_ct2 = st.slider("Selecione a página inicial e final:",
                        min_value=1,
                        max_value=total_paginas,
                        value=(1,total_paginas),
                        step=1,
                        key="l2")
                
            tipo_contrato2 = st.radio("Tipo 2° documento", ["Contrato Social/Ata de assembleia", "Procuração"], horizontal=True, key="tipo_contrato2")
        

        if st.button("Enviar documentos", type="secondary", disabled=False):  
            formulario = {}
            documentos_identificacao = {}
            documentos_empresas = {}
            documento_empresa1 = None
            documento_empresa2 = None
            for doc in id_doc_uploader:
                documento = analisar_documento_identificacao(doc)                            
                documentos_identificacao[only_numbers(documento.cpf)] = documento
                
            if contrato_uploader1:
                documento_empresa1 = analisar_contrato(contrato_uploader1, tipo_contrato1, pg_ini_ct1, pg_fim_ct1)

            if contrato_uploader2:
                documento_empresa2 = analisar_contrato(contrato_uploader2, tipo_contrato2, pg_ini_ct2, pg_fim_ct2)

            if formulario_uploader:
                formulario = analisar_formulario(formulario_uploader)
           
            if documentos_identificacao:
                with st.container(border=True):
                    st.markdown("**Documentos de identificação**")
                    for key in documentos_identificacao:
                        doc = documentos_identificacao[key]                
                        st.markdown(f"**Nome:** {doc.nome.title()}<br>**CPF:** {format_cpf_cnpj(doc.cpf)}<br>**Data de Nascimento:** {doc.data_nascimento}<br>", unsafe_allow_html=True)     

            if documento_empresa1:
                documentos_empresas[only_numbers(documento_empresa1.cnpj)] = documento_empresa1
                with st.container(border=True):
                    st.markdown(f"**Dados do 1° documento ({tipo_contrato1}):**")
                    for r in documento_empresa1.responsaveis:
                        st.markdown(f"**Representante:** {r.nome_responsavel_legal.title()}<br>**CPF:** {format_cpf_cnpj(r.cpf_responsavel_legal)}<br>**Razão Social:** {documento_empresa1.razao_social}<br>**CNPJ:** {format_cpf_cnpj(documento_empresa1.cnpj)}<br>", unsafe_allow_html=True)                    
            
            if documento_empresa2:
                documentos_empresas[only_numbers(documento_empresa2.cnpj)] = documento_empresa2
                with st.container(border=True):
                    st.markdown(f"**Dados do 2° documento ({tipo_contrato2}):**")
                    for r in documento_empresa2.responsaveis:
                        st.markdown(f"**Representante:** {r.nome_responsavel_legal.title()}<br>**CPF:** {format_cpf_cnpj(r.cpf_responsavel_legal)}<br>**Razão Social:** {documento_empresa1.razao_social}<br>**CNPJ:** {format_cpf_cnpj(documento_empresa1.cnpj)}<br>", unsafe_allow_html=True)                    

            show_form(formulario)
            show_analisys_pj(formulario, documentos_identificacao, documentos_empresas)