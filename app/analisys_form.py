import streamlit as st
from .novo_pj_validate import valida_representante, valida_subscritor_atual, valida_subscritor_novo, valida_titular_atual, valida_titular_novo
from .pj_validate import compara_antigo_titular_com_documento_empresa, compara_novo_titular_com_documento_empresa, compara_representante_empresa, compara_subscritor_com_documento_empresa
from .novo_pf_validate import valida_nome_subscritor_atual, valida_nome_subscritor_novo, valida_nome_titular_atual, valida_nome_titular_novo
from .pf_validate import compara_antigo_titular_com_documento, compara_novo_titular_com_documento, compara_subscritor_com_documento
from .titulo_capitalizacao.titulo_capitalizacao import TituloCapitalizacao

def show_analisys_pf(formulario, documentos_identificacao):
    if isinstance(formulario, TituloCapitalizacao):
        show_new_analisys_pf(formulario, documentos_identificacao)
    else:
        show_old_analisys_pf(formulario, documentos_identificacao)


def show_analisys_pj(formulario, documentos_identificacao, documentos_empresas):      
    if isinstance(formulario, TituloCapitalizacao):
        show_new_analisys_pj(formulario, documentos_identificacao, documentos_empresas)
    else:
        show_old_analisys_pj(formulario, documentos_identificacao, documentos_empresas)

def show_new_analisys_pf(formulario, documentos_identificacao):    
    if documentos_identificacao and formulario:
        with st.container(border=True):
            if formulario.opcao == 1:
                with st.expander("Validação dos dados do subscritor atual", expanded=True):
                    st.markdown(f"Subscritor: ***{formulario.subscritor.nome_atual}***")
                    st.write(valida_nome_subscritor_atual(formulario, documentos_identificacao))              
            if formulario.opcao == 2:
                with st.expander("Validação dos dados do subscritor atual", expanded=True):
                    st.markdown(f"Subscritor: ***{formulario.subscritor.nome_atual}***")
                    st.write(valida_nome_subscritor_atual(formulario, documentos_identificacao))
                with st.expander("Validação dos dados do novo subscritor", expanded=True):
                    st.markdown(f"Novo Subscritor: ***{formulario.subscritor.nome_novo}***")
                    st.write(valida_nome_subscritor_novo(formulario, documentos_identificacao))
            if formulario.opcao == 3:
                with st.expander("Validação dos dados do titular atual", expanded=True):
                    st.markdown(f"Titular: ***{formulario.titular.nome_atual}***")
                    st.write(valida_nome_titular_atual(formulario, documentos_identificacao))
                with st.expander("Validação dos dados do novo titular", expanded=True):
                    st.markdown(f"Novo Titular: ***{formulario.titular.nome_novo}***")
                    st.write(valida_nome_titular_novo(formulario, documentos_identificacao))
            if formulario.opcao == 4:
                with st.expander("Validação dos dados do subscritor atual", expanded=True):
                    st.markdown(f"Subscritor: ***{formulario.subscritor.nome_atual}***")
                    st.write(valida_nome_subscritor_atual(formulario, documentos_identificacao))
                with st.expander("Validação dos dados do novo subscritor", expanded=True):
                    st.markdown(f"Novo Subscritor: ***{formulario.subscritor.nome_novo}***")
                    st.write(valida_nome_subscritor_novo(formulario, documentos_identificacao))
                with st.expander("Validação dos dados do titular atual", expanded=True):
                    st.markdown(f"Titular: ***{formulario.titular.nome_atual}***")
                    st.write(valida_nome_titular_atual(formulario, documentos_identificacao))
                with st.expander("Validação dos dados do novo titular", expanded=True):
                    st.markdown(f"Novo Titular: ***{formulario.titular.nome_novo}***")
                    st.write(valida_nome_titular_novo(formulario, documentos_identificacao))

def show_old_analisys_pf(formulario, documentos_identificacao):
    if documentos_identificacao and formulario:
        with st.container(border=True):
            if formulario.opcao == 1:
                with st.expander("Validação dos dados do subscritor (bloco B)", expanded=True):
                    check_doc_subscritor = compara_subscritor_com_documento(formulario, documentos_identificacao)
                    if check_doc_subscritor < 0.90:
                        st.write("O nome ou CPF/CNPJ do subscritor não correspondem aos documentos de identificação.")
                    elif check_doc_subscritor == 1.0:
                        st.write("O nome e o CPF/CNPJ do subscritor correspondem aos documentos de identificação.")
                    elif check_doc_subscritor > 0.90:
                        st.write(f"O CPF/CNPJ corresponde ao do subscritor, mas o nome apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação.")

            if formulario.opcao == 2:
                with st.expander("Validação dos dados do novo titular (bloco C)", expanded=True):
                    check_doc_novo_titular = compara_novo_titular_com_documento(formulario, documentos_identificacao)                                                
                    if check_doc_novo_titular < 0.90:
                        st.write("O nome ou CPF/CNPJ do titular não correspondem aos documentos de identificação.")
                    elif check_doc_novo_titular == 1.0:
                        st.write("O nome e o CPF/CNPJ do titular correspondem aos documentos de identificação.")
                    elif check_doc_novo_titular > 0.90:                        
                        st.write(f"O CPF/CNPJ corresponde ao do novo titular, mas o nome apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos de identificação.")
                    
                with st.expander("Validação dos dados do cedente (bloco C)", expanded=True):
                    check_doc_cedente = compara_antigo_titular_com_documento(formulario, documentos_identificacao)                                                
                    if check_doc_cedente < 0.90:
                        st.write("O nome ou CPF/CNPJ do cedente (antigo titular) não correspondem aos documentos de identificação.")
                    elif check_doc_cedente == 1.0:
                        st.write("O nome e o CPF/CNPJ do cedente (antigo titular) correspondem aos documentos de identificação.")
                    elif check_doc_cedente > 0.90:                        
                        st.write(f"O CPF/CNPJ corresponde ao do cedente (antigo titular), mas o nome apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação.")                           

            if formulario.opcao == 3:
                with st.expander("Validação dos dados do subscritor (bloco B)", expanded=True):
                    check_doc_subscritor = compara_subscritor_com_documento(formulario, documentos_identificacao)                            
                    if check_doc_subscritor < 0.90:
                        st.write("O nome ou CPF/CNPJ do subscritor não correspondem aos documentos de identificação.")
                    elif check_doc_subscritor == 1.0:
                        st.write("O nome e o CPF/CNPJ do subscritor correspondem aos documentos de identificação.")
                    elif check_doc_subscritor > 0.90:                        
                        st.write(f"O CPF/CNPJ corresponde ao do subscritor, mas o nome apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação.")                         

                with st.expander("Validação dos dados do novo titular (bloco C)", expanded=True):
                    check_doc_novo_titular = compara_novo_titular_com_documento(formulario, documentos_identificacao)                                                
                    if check_doc_novo_titular < 0.90:
                        st.write("O nome ou CPF/CNPJ do titular não correspondem aos documentos de identificação.")
                    elif check_doc_novo_titular == 1.0:
                        st.write("O nome e o CPF/CNPJ do titular correspondem aos documentos de identificação.")
                    elif check_doc_novo_titular > 0.90:                        
                        st.write(f"O CPF/CNPJ corresponde ao do novo titular, mas o nome apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos de identificação.")
                    
                with st.expander("Validação dos dados do cedente (bloco C)", expanded=True):
                    check_doc_cedente = compara_antigo_titular_com_documento(formulario, documentos_identificacao)                                                
                    if check_doc_cedente < 0.90:
                        st.write("O nome ou CPF/CNPJ do cedente (antigo titular) não correspondem aos documentos de identificação.")
                    elif check_doc_cedente == 1.0:
                        st.write("O nome e o CPF/CNPJ do cedente (antigo titular) correspondem aos documentos de identificação.")
                    elif check_doc_cedente > 0.90:                        
                        st.write(f"O CPF/CNPJ corresponde ao do cedente (antigo titular), mas o nome apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação.")                           

def show_new_analisys_pj(formulario, documentos_identificacao, documentos_empresas):    
    if documentos_identificacao and documentos_empresas and formulario:
        with st.container(border=True):

            #Alteração de conta e forma de pagamento
            if formulario.opcao == 1:
                with st.expander("Validação dos dados do subscritor", expanded=True):
                    st.markdown(f"Subscritor: ***{formulario.subscritor.nome_atual}***")
                    st.write(valida_subscritor_atual(formulario, documentos_empresas, documentos_identificacao))
        
                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            st.write(valida_representante(documentos_identificacao, r))
            #Transferência de subscritor
            if formulario.opcao == 2:
                with st.expander("Validação dos dados do subscritor", expanded=True):
                    st.markdown(f"Subscritor: ***{formulario.subscritor.nome_atual}***")
                    st.write(valida_subscritor_atual(formulario, documentos_empresas, documentos_identificacao))

                with st.expander("Validação dos dados do novo subscritor", expanded=True):
                    st.markdown(f"Novo Subscritor: ***{formulario.subscritor.nome_novo}***")
                    st.write(valida_subscritor_novo(formulario, documentos_empresas, documentos_identificacao))

                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            st.write(valida_representante(documentos_identificacao, r))
          
            #Transferência de titular
            if formulario.opcao == 3:                
                with st.expander("Validação dos dados do titular", expanded=True):
                    st.markdown(f"Titular: ***{formulario.titular.nome_atual}***")
                    st.write(valida_titular_atual(formulario, documentos_empresas, documentos_identificacao))
                
                with st.expander("Validação dos dados do novo titular", expanded=True):
                    st.markdown(f"Novo Titular: ***{formulario.titular.nome_novo}***")
                    st.write(valida_titular_novo(formulario, documentos_empresas, documentos_identificacao))

                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            st.write(valida_representante(documentos_identificacao, r))
                            
            #Transferência de titular e subscritor
            if formulario.opcao == 4:
                with st.expander("Validação dos dados do titular", expanded=True):
                    st.markdown(f"Titular: ***{formulario.titular.nome_atual}***")
                    st.write(valida_titular_atual(formulario, documentos_empresas, documentos_identificacao))
                
                with st.expander("Validação dos dados do novo titular", expanded=True):
                    st.markdown(f"Novo Titular: ***{formulario.titular.nome_novo}***")
                    st.write(valida_titular_novo(formulario, documentos_empresas, documentos_identificacao))                   

                with st.expander("Validação dos dados do subscritor", expanded=True):
                    st.markdown(f"Subscritor: ***{formulario.subscritor.nome_atual}***")
                    st.write(valida_subscritor_atual(formulario, documentos_empresas, documentos_identificacao))

                with st.expander("Validação dos dados do novo subscritor", expanded=True):
                    st.markdown(f"Novo Subscritor: ***{formulario.subscritor.nome_novo}***")
                    st.write(valida_subscritor_novo(formulario, documentos_empresas, documentos_identificacao))

                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            st.write(valida_representante(documentos_identificacao, r))

def show_old_analisys_pj(formulario, documentos_identificacao, documentos_empresas):    
    if documentos_identificacao and documentos_empresas and formulario:
        with st.container(border=True):
            if formulario.opcao == 1:
                with st.expander("Validação dos dados do subscritor (bloco B)", expanded=True):                            
                    check_doc_subscritor, tipo = compara_subscritor_com_documento_empresa(formulario, documentos_empresas, documentos_identificacao)
                    if tipo == "PF":
                        if check_doc_subscritor < 0.90:
                            st.write("O nome ou CPF/CNPJ do subscritor não correspondem aos documentos de identificação.")
                        elif check_doc_subscritor == 1.0:
                            st.write("O nome e o CPF/CNPJ do subscritor correspondem aos documentos de identificação.")
                        elif check_doc_subscritor > 0.90:
                            st.write(f"O CPF/CNPJ corresponde ao do subscritor, mas o nome apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação.")
                    else:
                        if check_doc_subscritor < 0.90:
                            st.write("A razão social ou CNPJ do subscritor não correspondem aos documentos da empresa.")
                        elif check_doc_subscritor == 1.0:
                            st.write("A razão social e o CNPJ do subscritor correspondem aos documentos da empresa.")
                        elif check_doc_subscritor > 0.90:                        
                            st.write(f"O CNPJ corresponde ao do subscritor, mas a razão social apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos da empresa.")                                            
        
                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():                            
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            check_doc_representante = compara_representante_empresa(r.cpf_responsavel_legal, r.nome_responsavel_legal, documentos_identificacao)
                            if check_doc_representante < 0.90:
                                st.write("O nome ou CPF do representante legal não correspondem aos documentos de identificação.")
                            elif check_doc_representante == 1.0:
                                st.write("O nome e o CPF do representante legal correspondem aos documentos de identificação.")
                            elif check_doc_representante > 0.90:                        
                                st.write(f"O CPF corresponde ao do representante legal, mas o nome apresenta "+ "{:.2%}".format(check_doc_representante)+" de similaridade com os documentos de identificação.")

            if formulario.opcao == 2:
                with st.expander("Validação dos dados do novo titular (bloco C)", expanded=True):
                            check_doc_novo_titular, tipo = compara_novo_titular_com_documento_empresa(formulario, documentos_empresas, documentos_identificacao)  
                            if tipo == "PF":
                                if check_doc_novo_titular < 0.90:
                                    st.write("O nome ou CPF/CNPJ do novo titular não correspondem aos documentos de identificação.")
                                elif check_doc_novo_titular == 1.0:
                                    st.write("O nome e o CPF/CNPJ do novo titular correspondem aos documentos de identificação.")
                                elif check_doc_novo_titular > 0.90:                        
                                    st.write(f"O CPF/CNPJ corresponde ao do novo titular, mas o nome apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos de identificação.")
                            else:
                                if check_doc_novo_titular < 0.90:
                                    st.write("A razão social ou o CNPJ do titular não correspondem aos documentos da empresa.")
                                elif check_doc_novo_titular == 1.0:
                                    st.write("A razão social e o CNPJ do titular correspondem aos documentos da empresa.")
                                elif check_doc_novo_titular > 0.90:                        
                                    st.write(f"O CNPJ corresponde ao do novo titular, mas a razão social apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos da empresa.")                                     
                            
                with st.expander("Validação dos dados do cedente (bloco C)", expanded=True):
                    check_doc_cedente, tipo = compara_antigo_titular_com_documento_empresa(formulario, documentos_empresas, documentos_identificacao)                        
                    if tipo == "PF":
                        if check_doc_cedente < 0.90:
                            st.write("O nome ou CPF/CNPJ do cedente (antigo titular) não correspondem aos documentos de identificação.")
                        elif check_doc_cedente == 1.0:
                            st.write("O nome e o CPF/CNPJ do cedente (antigo titular) correspondem aos documentos de identificação.")
                        elif check_doc_cedente > 0.90:                        
                            st.write(f"O CPF/CNPJ corresponde ao do cedente (antigo titular), mas o nome apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação.")                           
                    else:
                        if check_doc_cedente < 0.90:
                            st.write("A razão social ou o CNPJ do cedente (antigo titular) não correspondem aos documentos da empresa.")
                        elif check_doc_cedente == 1.0:
                            st.write("A razão social e o CNPJ do cedente (antigo titular) correspondem aos documentos da empresa.")
                        elif check_doc_cedente > 0.90:                        
                            st.write(f"O CNPJ corresponde ao do cedente (antigo titular), mas o nome apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação.")                                

                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():                            
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            check_doc_representante = compara_representante_empresa(r.cpf_responsavel_legal, r.nome_responsavel_legal, documentos_identificacao)
                            if check_doc_representante < 0.90:
                                st.write("O nome ou CPF do representante legal não correspondem aos documentos de identificação.")
                            elif check_doc_representante == 1.0:
                                st.write("O nome e o CPF do representante legal correspondem aos documentos de identificação.")
                            elif check_doc_representante > 0.90:                        
                                st.write(f"O CPF corresponde ao do representante legal, mas o nome apresenta "+ "{:.2%}".format(check_doc_representante)+" de similaridade com os documentos de identificação.")

            if formulario.opcao == 3:
                with st.expander("Validação dos dados do subscritor (bloco B)", expanded=True):                            
                    check_doc_subscritor, tipo = compara_subscritor_com_documento_empresa(formulario, documentos_empresas, documentos_identificacao)
                    if tipo == "PF":
                        if check_doc_subscritor < 0.90:
                            st.write("O nome ou CPF/CNPJ do subscritor não correspondem aos documentos de identificação.")
                        elif check_doc_subscritor == 1.0:
                            st.write("O nome e o CPF/CNPJ do subscritor correspondem aos documentos de identificação.")
                        elif check_doc_subscritor > 0.90:
                            st.write(f"O CPF/CNPJ corresponde ao do subscritor, mas o nome apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação.")
                    else:
                        if check_doc_subscritor < 0.90:
                            st.write("A razão social ou CNPJ do subscritor não correspondem aos documentos da empresa.")
                        elif check_doc_subscritor == 1.0:
                            st.write("A razão social e o CNPJ do subscritor correspondem aos documentos da empresa.")
                        elif check_doc_subscritor > 0.90:                        
                            st.write(f"O CNPJ corresponde ao do subscritor, mas a razão social apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos da empresa.")                                            
            
                with st.expander("Validação dos dados do novo titular (bloco C)", expanded=True):
                    check_doc_novo_titular, tipo = compara_novo_titular_com_documento_empresa(formulario, documentos_empresas, documentos_identificacao)  
                    if tipo == "PF":
                        if check_doc_novo_titular < 0.90:
                            st.write("O nome ou CPF/CNPJ do novo titular não correspondem aos documentos de identificação.")
                        elif check_doc_novo_titular == 1.0:
                            st.write("O nome e o CPF/CNPJ do novo titular correspondem aos documentos de identificação.")
                        elif check_doc_novo_titular > 0.90:                        
                            st.write(f"O CPF/CNPJ corresponde ao do novo titular, mas o nome apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos de identificação.")
                    else:
                        if check_doc_novo_titular < 0.90:
                            st.write("A razão social ou o CNPJ do novo titular não correspondem aos documentos da empresa.")
                        elif check_doc_novo_titular == 1.0:
                            st.write("A razão social e o CNPJ do novo titular correspondem aos documentos da empresa.")
                        elif check_doc_novo_titular > 0.90:                        
                            st.write(f"O CNPJ corresponde ao do novo titular, mas a razão social apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos da empresa.")                                     
                            
                with st.expander("Validação dos dados do cedente (bloco C)", expanded=True):
                    check_doc_cedente, tipo = compara_antigo_titular_com_documento_empresa(formulario, documentos_empresas, documentos_identificacao)                        
                    if tipo == "PF":
                        if check_doc_cedente < 0.90:
                            st.write("O nome ou CPF/CNPJ do cedente (antigo titular) não correspondem aos documentos de identificação.")
                        elif check_doc_cedente == 1.0:
                            st.write("O nome e o CPF/CNPJ do cedente (antigo titular) correspondem aos documentos de identificação.")
                        elif check_doc_cedente > 0.90:                        
                            st.write(f"O CPF/CNPJ corresponde ao do cedente (antigo titular), mas o nome apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação.")                           
                    else:
                        if check_doc_cedente < 0.90:
                            st.write("A razão social ou o CNPJ do cedente (antigo titular) não correspondem aos documentos da empresa.")
                        elif check_doc_cedente == 1.0:
                            st.write("A razão social e o CNPJ do cedente (antigo titular) correspondem aos documentos da empresa.")
                        elif check_doc_cedente > 0.90:                        
                            st.write(f"O CNPJ corresponde ao do cedente (antigo titular), mas o nome apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação.")                                



                with st.expander("Validação dos dados do representante legal", expanded=True):                
                    for key in documentos_empresas.keys():                            
                        for r in documentos_empresas[key].responsaveis:
                            st.markdown(f"Representante: ***{r.nome_responsavel_legal}***")
                            check_doc_representante = compara_representante_empresa(r.cpf_responsavel_legal, r.nome_responsavel_legal, documentos_identificacao)
                            if check_doc_representante < 0.90:
                                st.write("O nome ou CPF do representante legal não correspondem aos documentos de identificação.")
                            elif check_doc_representante == 1.0:
                                st.write("O nome e o CPF do representante legal correspondem aos documentos de identificação.")
                            elif check_doc_representante > 0.90:                        
                                st.write(f"O CPF corresponde ao do representante legal, mas o nome apresenta "+ "{:.2%}".format(check_doc_representante)+" de similaridade com os documentos de identificação.")