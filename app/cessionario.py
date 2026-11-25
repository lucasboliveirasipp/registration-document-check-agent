import pandas as pd    
import streamlit as st 
from .cs_validate import emoji_nota, verificar_planilha_comp_bancario, verificar_planilha_doc_identificacao, verificar_planilha_endereco
from .agent_tools import analisar_comprovante_banc, analisar_endereco, analisar_documento_identificacao, analisar_planilha
from .tools import converter_data, dict_to_planilhas, format_cpf_cnpj, only_numbers
 

def page_cessionario():   

    with st.container(border=True):
        id_doc_uploader = st.file_uploader(
            "Documentos de identificação:", type=['pdf', 'png', 'jpeg'],
            accept_multiple_files=True,
            key="pf_doc"
        )

        endereco_uploader = st.file_uploader(
            "Comprovante de endereço:", type=['pdf', 'png', 'jpeg'],
            accept_multiple_files=True,
            key="c_end"
        )

        comprovante_banc_uploader = st.file_uploader(
            "Comprovante Bancário:", type=['pdf', 'png', 'jpeg'],
            accept_multiple_files=True,
            key="c_banc"
        )

        planilha_uploader = st.file_uploader(
            "Planilha:", type=['xls', 'xlsx'],
            accept_multiple_files=False,
            key="c_plan"
        )

        if st.button("Enviar documentos", type="secondary", disabled=False):    
            documentos_identificacao = {}            
            comp_bancario = []
            enderecos = []
            planilha_dict = {}

            for doc in id_doc_uploader:
                documento = analisar_documento_identificacao(doc)                
                documentos_identificacao[only_numbers(documento.cpf)] = documento

            for end in endereco_uploader:
                enderecos.append(analisar_endereco(end))

            for comp in comprovante_banc_uploader:                
                comp_bancario.append(analisar_comprovante_banc(comp))

            if planilha_uploader:                
                planilha_dict = analisar_planilha(planilha_uploader)               
          
            if documentos_identificacao:
                    with st.container(border=True):
                        st.markdown("**Documentos de identificação**")
                        for key in documentos_identificacao:
                            doc = documentos_identificacao[key]                
                            st.markdown(f"**Nome:** {doc.nome.title()}<br>**CPF:** {format_cpf_cnpj(doc.cpf)}<br>**Data de Nascimento:** {doc.data_nascimento}<br>", unsafe_allow_html=True)                

            if enderecos:
                with st.container(border=True):
                    st.write("Dados do endereço:")
                    for endereco in enderecos:
                        st.markdown(
                            f"**Nome:** {endereco.nome.title()}<br>"
                            f"**Endereço:** {endereco.endereco}<br>"
                            f"**Rua:** {endereco.rua}<br>"
                            f"**Número:** {endereco.numero}<br>"
                            f"**Complemento:** {endereco.complemento}<br>"
                            f"**Bairro:** {endereco.bairro}<br>"
                            f"**Cidade:** {endereco.cidade}<br>"
                            f"**CEP:** {endereco.cep}<br>",
                            unsafe_allow_html=True
                        )

            if comp_bancario:
                with st.container(border=True):
                    st.write("Dados do comprovante bancário:")
                    for comprovante in comp_bancario:
                        st.markdown(
                            f"**Nome:** {comprovante.nome.title()}<br>"                            
                            f"**Instituição Bancária:** {comprovante.instituicao}<br>"                        
                            f"**Agência:** {comprovante.agencia}<br>"
                            f"**Conta:** {comprovante.conta}<br>",
                            unsafe_allow_html=True
                        )   

            if planilha_dict:
                with st.container(border=True):
                    st.write("Planilha:")                    
                    df = pd.DataFrame(planilha_dict)
                    df.columns = [
                        "Nome ou Razão Social",
                        "Nº do CPF ou CNPJ",
                        "CEP",
                        "Endereço",
                        "Nº",                        
                        "Complemento",
                        "Bairro",
                        "Cidade",
                        "Estado",
                        "Banco",
                        "Agência Bancária",
                        "Dígito da Agência",
                        "Nº da Conta",
                        "Dígito da Conta",
                        "Data de Nascimento"
                    ]                                        
                    df['Data de Nascimento'] = df['Data de Nascimento'].apply(converter_data)
                    st.table(df)
                  

            if planilha_dict and documentos_identificacao:                                               
                planilhas = dict_to_planilhas(planilha_dict)                        
                for linha in planilhas:
                    with st.expander(f"Validação da documentação: {linha.nome_razao_social.title()}", expanded=True):
                        doc = verificar_planilha_doc_identificacao(linha, documentos_identificacao)   
                        with st.container(border=True):
                            st.markdown(f"**Documento de identificação**")
                            if doc["DocumentoIdentificacao"] is not None:
                                data = {
                                    '': ["CPF", "Nome", "Data de nascimento"],
                                    "Planilha": [format_cpf_cnpj(linha.cpf_cnpj), linha.nome_razao_social.title(), linha.data_nascimento],
                                    "Documento de identificação": [format_cpf_cnpj(only_numbers(doc["DocumentoIdentificacao"].cpf)), doc["DocumentoIdentificacao"].nome.title(), doc["DocumentoIdentificacao"].data_nascimento],
                                    'Comparação': ["100%", "{:.0%}".format(doc['nome']), "{:.0%}".format(doc['data_nascimento'])],
                                    'Situação': [emoji_nota(1), emoji_nota(doc['nome']), emoji_nota(doc['data_nascimento'])]
                                }
                                df = pd.DataFrame(data)
                                st.table(df)

                                if doc['nome'] == 1 and doc['data_nascimento'] == 1:
                                    st.markdown(f"Todas as informações da planilha estão em conformidade com os documentos de identificação.")
                                elif doc['nome'] > 0.90 and doc['data_nascimento'] > 0.90:
                                    st.markdown(f"Algumas informações da planilha não correspondem aos dados do documento de identificação.")
                                else:
                                    st.markdown(f"As informações da planilha não estão em conformidade com o documento de identificação.")
                            else:                                
                                st.markdown(f"Não foram encontrados documentos de identificação que correspondam ao CPF {format_cpf_cnpj(linha.cpf_cnpj)} presente na planilha.")                        

                        banc = verificar_planilha_comp_bancario(linha, comp_bancario)  
                        with st.container(border=True):                          
                            st.markdown(f"**Comprovante bancário**")
                            if banc["ComprovanteBancario"] is not None:
                                data = {
                                    '': ["Nome", "Agência", "Conta"],
                                    "Planilha": [linha.nome_razao_social.title(), linha.agencia+( "-"+linha.digito_agencia if linha.digito_agencia != "" else ""), linha.numero_conta+( "-"+linha.digito_conta if linha.digito_conta != "" else "")],
                                    "Comprovante Bancário": [banc["ComprovanteBancario"].nome, banc["ComprovanteBancario"].agencia, banc["ComprovanteBancario"].conta],
                                    'Comparação': ["{:.0%}".format(banc['nome']), "{:.0%}".format(banc['agencia']), "{:.0%}".format(banc['conta'])],
                                    'Status': [emoji_nota(banc['nome']), emoji_nota(banc['agencia']), emoji_nota(banc['conta'])]
                                }
                                df = pd.DataFrame(data)
                                st.table(df)
                                if banc['nome'] == 1 and banc['agencia'] == 1 and banc['conta'] == 1:
                                    st.markdown(f"Todas as informações da planilha estão em conformidade com comprovante bancário.")
                                elif banc['nome'] > 0.90 and banc['agencia'] > 0.90 and banc['conta'] > 0.90:
                                    st.markdown(f"Algumas informações da planilha não correspondem aos dados do comprovante bancário.")
                                else:
                                    st.markdown(f"As informações da planilha não estão em conformidade com o comprovante bancário.")
                            else:                                
                                st.markdown(f"Não foram encontrados comprovantes bancários em nome de {linha.nome_razao_social.title()}.")
                                    
                        end = verificar_planilha_endereco(linha, enderecos)
                        with st.container(border=True):
                            st.markdown(f"**Comprovante de endereço**")
                            if end["ComprovanteEndereco"] is not None:
                                data = {
                                    "": ["Nome", "Rua", "Número", "Complemento", "Bairro", "Cidade", "CEP"],
                                    "Planilha": [linha.nome_razao_social.title(), linha.endereco, linha.numero, linha.complemento, linha.bairro, linha.cidade, only_numbers(linha.cep)],
                                    "Comprovante de Endereço": [end["ComprovanteEndereco"].nome.title(), end["ComprovanteEndereco"].rua, end["ComprovanteEndereco"].numero, end["ComprovanteEndereco"].complemento, end["ComprovanteEndereco"].bairro, end["ComprovanteEndereco"].cidade, only_numbers(end["ComprovanteEndereco"].cep)],
                                    'Comparação': [
                                        "{:.0%}".format(end['nome']), 
                                        "{:.0%}".format(end['endereco_rua']), 
                                        "{:.0%}".format(end['numero']), 
                                        "{:.0%}".format(end['complemento']), 
                                        "{:.0%}".format(end['bairro']), 
                                        "{:.0%}".format(end['cidade']), 
                                        "{:.0%}".format(end['cep'])
                                        ],
                                    'Status': [
                                        emoji_nota(end['nome']), 
                                        emoji_nota(end['endereco_rua']), 
                                        emoji_nota(end['numero']), 
                                        emoji_nota(end['complemento']), 
                                        emoji_nota(end['bairro']), 
                                        emoji_nota(end['cidade']), 
                                        emoji_nota(end['cep'])
                                        ],                                    
                                }
                                df = pd.DataFrame(data)
                                st.table(df)
                                
                                if end['analise'] == 1:
                                    st.markdown(f"Todas as informações da planilha estão em conformidade com comprovante de endereço.")
                                elif end['analise'] > 0.90:
                                    st.markdown(f"Algumas informações da planilha não correspondem aos dados do comprovante de endereço.")
                                else:
                                    st.markdown(f"As informações da planilha não estão em conformidade com o comprovante de endereço.")
                            else:                                
                                st.markdown(f"Não foram encontrados comprovantes de endereço em nome de {linha.nome_razao_social.title()}.")

