import streamlit as st
import pandas as pd   
from .titulo_capitalizacao.enums.forma_pagamento import FormaPagamento
from .titulo_capitalizacao.titulo_capitalizacao import TituloCapitalizacao
from .tools import format_cpf_cnpj 


def show_form(formulario):
    if isinstance(formulario, TituloCapitalizacao):
        show_new_form(formulario)
    else:
        show_old_form(formulario)

def show_new_form(formulario):
    if formulario:
        with st.container(border=True):
            st.markdown(f"**Formulário**")
            with st.container(border=True):
                st.markdown(f"**{formulario.tipo_alteracao()}**")

            with st.container(border=True):                             
                st.markdown("**Dados do Título**")                
                data = { 
                    "Quantidade": [titulo.quantidade for titulo in formulario.titulos], 
                    "Série": [titulo.serie for titulo in formulario.titulos], 
                    "Titulo Inicial": [titulo.titulo_inicial for titulo in formulario.titulos], 
                    "Titulo Final": [titulo.titulo_final for titulo in formulario.titulos] }
                df = pd.DataFrame(data)                                
                st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

            if formulario.opcao in [1,2,4]:
                with st.container(border=True):
                    st.markdown("**Transferência de Subscritor**")                    
                    col1, col2 = st.columns(2)
                    with col1:                         
                        st.markdown(f"**Nome do Atual Subscritor:**<br>"+
                                f"**CPF/CNPJ:** <br>"+                                
                                f"**Grau Parentesco Novo Subscritor:**<br><br>"+
                                f"**Nome do Novo Subscritor:**<br>"+
                                f"**CPF/CNPJ:**<br>"+
                                f"**CEP:**<br>"+
                                f"**Endereço Novo Subscritor:**<br>"+
                                f"**Bairro:**<br>"+
                                f"**Cidade:**<br>"+
                                f"**UF:**<br>", unsafe_allow_html=True)                
                    with col2:
                        st.markdown(formulario.subscritor.nome_atual+"<br>"+
                                    formulario.subscritor.cpf_cnpj_atual+"<br>"+
                                    formulario.subscritor.grau_parentesco_novo+"<br><br>"+
                                    formulario.subscritor.nome_novo+"<br>"+
                                    formulario.subscritor.cpf_cnpj_novo+"<br>"+
                                    formulario.subscritor.cep_novo+"<br>"+
                                    formulario.subscritor.endereco_novo+"<br>"+
                                    formulario.subscritor.bairro_novo+"<br>"+
                                    formulario.subscritor.cidade_novo+"<br>"+
                                    formulario.subscritor.uf_novo, unsafe_allow_html=True)
                                                 
            if formulario.opcao in [1,3,4]:
                with st.container(border=True):
                    st.markdown("**Transferência de Titular**")                    
                    col1, col2 = st.columns(2)
                    with col1:                         
                        st.markdown(f"**Nome do Atual Titular:**<br>"+
                                f"**CPF/CNPJ:** <br>"+                                
                                f"**Grau Parentesco Novo Titular:**<br><br>"+
                                f"**Nome do Novo Titular:**<br>"+
                                f"**CPF/CNPJ:**<br>"+
                                f"**CEP:**<br>"+
                                f"**Endereço Novo Titular:**<br>"+
                                f"**Bairro:**<br>"+
                                f"**Cidade:**<br>"+
                                f"**UF:**<br>", unsafe_allow_html=True)                
                    with col2:
                        st.markdown(formulario.titular.nome_atual+"<br>"+
                                    formulario.titular.cpf_cnpj_atual+"<br>"+
                                    formulario.titular.grau_parentesco_novo+"<br><br>"+
                                    formulario.titular.nome_novo+"<br>"+
                                    formulario.titular.cpf_cnpj_novo+"<br>"+
                                    formulario.titular.cep_novo+"<br>"+
                                    formulario.titular.endereco_novo+"<br>"+
                                    formulario.titular.bairro_novo+"<br>"+
                                    formulario.titular.cidade_novo+"<br>"+
                                    formulario.titular.uf_novo, unsafe_allow_html=True) 
                           
            if formulario.opcao in [1,2,4]:
                with st.container(border=True):
                    st.markdown("**Alteração da Forma de Pagamento (Conta Acme)**")                    
                    col1, col2 = st.columns(2) 
                    with col1:
                        if  formulario.forma_pagamento == FormaPagamento.CONTA.value:
                            st.markdown(f"**Forma de pagamento:**<br>"+
                                        f"**Agencia:** <br>"+                                
                                        f"**Conta:**<br><br>"+
                                        f"**Tipo da conta:**<br>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"**Forma de pagamento:**", unsafe_allow_html=True)
                    with col2:
                        if  formulario.forma_pagamento == FormaPagamento.CONTA.value:
                            st.markdown(formulario.forma_pagamento+"<br>"+
                                        formulario.agencia+"<br>"+
                                        formulario.conta+"<br><br>"+
                                        formulario.tipo_conta+"<br>", unsafe_allow_html=True) 
                        else:
                            st.markdown(formulario.forma_pagamento, unsafe_allow_html=True) 

            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Local:** {formulario.local}", unsafe_allow_html=True) 
                with col2: 
                    st.markdown(f"**Data:** {formulario.data}", unsafe_allow_html=True) 


            with st.container(border=True):
                st.markdown("**Dados das assinaturas**")                
                data = { 
                    "Nome": [assinatura.nome for assinatura in formulario.assinaturas], 
                    "CPF/CNPJ": [assinatura.cpf_cnpj for assinatura in formulario.assinaturas], 
                    "Tipo Assinatura": [assinatura.tipo_assinatura for assinatura in formulario.assinaturas], 
                    "Assinado": [assinatura.assinatura for assinatura in formulario.assinaturas] }
                df = pd.DataFrame(data)                                
                st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

def show_old_form(formulario):
    if formulario:
        with st.container(border=True):
            st.markdown(f"**Formulário**")
            with st.container(border=True):
                st.markdown(f"**{formulario.tipo_alteracao()}**")

            with st.container(border=True):                              
                x = 0                  
                st.markdown("**A. N° Contr. Tit.**")
                for i in formulario.contratos_titular:
                    x+=1
                    st.markdown(f"**{x}. Série:** {i.numero_serie()}, **Combinação:** {i.numero_combinacao()}", unsafe_allow_html=True)                        

            if formulario.opcao in [1,3,4]:
                with st.container(border=True):
                    st.markdown("**B. Novo Subscritor ou atual**")
                    st.markdown(f"**Nome:** {formulario.subscritor.nome.title()}<br>"+
                                f"**CPF/CNPJ:** {format_cpf_cnpj(formulario.subscritor.cpf_cnpj)}<br>"+
                                f"**Código Agência:** {formulario.subscritor.codigo_agencia}-{formulario.subscritor.codigo_agencia_dig}<br>"+
                                f"**Razão:** {formulario.subscritor.razao}<br>"+
                                f"**Conta:** {formulario.subscritor.conta}-{formulario.subscritor.conta_dig}", unsafe_allow_html=True)
                    
            if formulario.opcao in [2,3]:
                with st.container(border=True):
                    st.markdown("**C. Titular**")
                    st.markdown(f"**Cedente:** {formulario.titular.cedente.title()}<br>"+
                                f"**CPF/CNPJ:** {format_cpf_cnpj(formulario.titular.cpf_cnpj_cedente)}<br>", unsafe_allow_html=True)
                    st.markdown("**C. Dados Novo Titular**")
                    st.markdown(f"**Nome Completo ou Razão Social:** {formulario.titular.nome_razao.title()}<br>"+
                                f"**CPF/CNPJ:** {format_cpf_cnpj(formulario.titular.cpf_cnpj_novo)}<br>"+
                                f"**Dt. Nasc./Const. Emp.:** {formulario.titular.data_nasc_const_emp}<br>"+
                                f"**Tipo Doc:** {formulario.titular.tipo_doc}<br>"+
                                f"**N° Documento:** {formulario.titular.numero_documento}<br>"+
                                f"**Orgão Emissor:** {formulario.titular.orgao_emissor}<br>"+
                                f"**Data Emissão:** {formulario.titular.data_emissao}<br>"+
                                f"**Endereço Completo:** {formulario.titular.endereco_completo}<br>"+
                                f"**Bairro:** {formulario.titular.bairro}<br>"+
                                f"**Cidade:** {formulario.titular.cidade}<br>"+
                                f"**CEP:** {formulario.titular.cep}<br>"+
                                f"**UF:** {formulario.titular.uf} <br>"+
                                f"**Telefone:** {formulario.titular.ddd} {formulario.titular.telefone}<br>"+
                                f"**Profissão/Ativ. Principal:** {formulario.titular.profissao_ativ_principal}", unsafe_allow_html=True)
                    
            if formulario.opcao in [2,3]:
                with st.container(border=True):
                    st.markdown("**D. Declaração**")
                    st.markdown(f"**Cessionário (Novo Titular):** {formulario.declaracao.nome_novo_titular.title()}<br>**Assinatura:** {formulario.declaracao.novo_titular_assinou()}", unsafe_allow_html=True)
                    st.markdown(f"**Cedente (Antigo Titular):** {formulario.declaracao.nome_antigo_titular.title()}<br>**Assinatura:** {formulario.declaracao.antigo_titular_assinou()}", unsafe_allow_html=True)
                    st.markdown(f"**Reserva:** {formulario.declaracao.reserva}", unsafe_allow_html=True)

            if formulario.opcao in [1,3,4]:
                with st.container(border=True):
                    st.markdown("**E. Assinaturas**")
                    if formulario.nome_subscritor_novo_atual:
                        st.markdown(f"**Nome:** {formulario.nome_subscritor_novo_atual.title()}<br>**Assinatura:** {formulario.novo_atual_subscritor_assinou()}", unsafe_allow_html=True)
                    if formulario.nome_subscritor_antigo:
                        st.markdown(f"**Nome:** {formulario.nome_subscritor_antigo.title()}<br>**Assinatura:** {formulario.antigo_subscritor_assinou()}", unsafe_allow_html=True)
                    if not formulario.nome_subscritor_novo_atual and not formulario.nome_subscritor_antigo:
                        st.markdown(f"**Sem assinaturas**", unsafe_allow_html=True)