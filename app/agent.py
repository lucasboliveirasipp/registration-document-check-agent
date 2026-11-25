import streamlit as st
from .pessoa_fisica import page_pessoa_fisica
from .pessoa_juridica import page_pessoa_juridica
from .cessionario import page_cessionario
                        
def build_page(is_authenticated: bool):
    print("Passo 3")
    if is_authenticated:  

        option = st.selectbox("Tipo análise:", ("Pessoa Física", "Pessoa Jurídica", "Cessionário"))        

        if option == "Cessionário":                            
            page_cessionario()
        elif option == "Pessoa Jurídica":                
            page_pessoa_juridica()
        else:
             page_pessoa_fisica()

    else:  
        st.error("Você não está autenticado. Por favor, faça login para acessar esta página.")