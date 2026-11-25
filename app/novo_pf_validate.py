from .titulo_capitalizacao.enums.tipo_assinatura import TipoAssinatura
from .titulo_capitalizacao.titulo_capitalizacao import TituloCapitalizacao
from .tools import calculate_similarity, only_numbers, remove_accents


#1,2,4
#nome do subscritor atual com nome do documento
def nf_compara_subscritor_com_documento_atual(form: TituloCapitalizacao, documentos):        
    cpf_cnpj = only_numbers(form.subscritor.cpf_cnpj_atual)
    if cpf_cnpj in documentos:        
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), remove_accents(form.subscritor.nome_atual))
    else:
        return 0
    

def nf_verifica_nome_assinatura_subscritor_atual(form: TituloCapitalizacao):    
    assinatura = buscar_assinatura_por_cpf_cnpj(form.assinaturas, only_numbers(form.subscritor.cpf_cnpj_atual), TipoAssinatura.SUBSCRITOR_ATUAL)
    if assinatura is not None:
        return calculate_similarity(remove_accents(form.subscritor.nome_atual), assinatura.nome)        
    else:
        return 0
    

#nome do subscritor novo com nome do documento
def nf_compara_subscritor_com_documento_novo(form: TituloCapitalizacao, documentos):        
    cpf_cnpj = only_numbers(form.subscritor.cpf_cnpj_novo)
    if cpf_cnpj in documentos:        
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), remove_accents(form.subscritor.nome_novo))
    else:
        return 0
    
def nf_verifica_nome_assinatura_subscritor_novo(form: TituloCapitalizacao):    
    assinatura = buscar_assinatura_por_cpf_cnpj(form.assinaturas, only_numbers(form.subscritor.cpf_cnpj_novo), TipoAssinatura.SUBSCRITOR_NOVO)
    if assinatura is not None:
        return calculate_similarity(remove_accents(form.subscritor.nome_novo), assinatura.nome)        
    else:
        return 0


#nome do titular atual com nome do documento
def nf_compara_titular_com_documento_atual(form: TituloCapitalizacao, documentos):    
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_atual)
    if cpf_cnpj in documentos:
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), remove_accents(form.titular.nome_atual))
    else:
        return 0
    
def nf_verifica_assinatura_titular_atual(form: TituloCapitalizacao):    
    assinatura = buscar_assinatura_por_cpf_cnpj(form.assinaturas, only_numbers(form.titular.cpf_cnpj_atual), TipoAssinatura.TITULAR_ATUAL)
    if assinatura is not None:
        return calculate_similarity(remove_accents(form.titular.nome_novo), assinatura.nome)        
    else:
        return 0
    

#nome do novo titular com nome do documento
def nf_compara_titular_com_documento_novo(form: TituloCapitalizacao, documentos):    
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_novo)
    if cpf_cnpj in documentos:        
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), remove_accents(form.titular.nome_novo))
    else:
        return 0
    

def nf_verifica_assinatura_titular_novo(form: TituloCapitalizacao):    
    assinatura = buscar_assinatura_por_cpf_cnpj(form.assinaturas, only_numbers(form.titular.cpf_cnpj_novo), TipoAssinatura.TITULAR_NOVO)
    if assinatura is not None:
        return calculate_similarity(remove_accents(form.titular.nome_novo), assinatura.nome)        
    else:
        return 0


def buscar_assinatura_por_cpf_cnpj(lista_assinaturas, cpf_cnpj_atual, tipo_assinatura):
    return next((assinatura for assinatura in lista_assinaturas if assinatura.cpf_cnpj == cpf_cnpj_atual and assinatura.tipo_assinatura == tipo_assinatura), None)

def valida_nome_subscritor_atual(formulario, documentos_identificacao):
        check_doc_subscritor = nf_compara_subscritor_com_documento_atual(formulario, documentos_identificacao)
        if check_doc_subscritor < 0.90:
            return "O nome ou CPF/CNPJ do subscritor não correspondem aos documentos de identificação."
        elif check_doc_subscritor == 1.0:
            return "O nome e o CPF/CNPJ do subscritor correspondem aos documentos de identificação."
        elif check_doc_subscritor > 0.90:
            return f"O CPF/CNPJ corresponde ao do subscritor, mas o nome apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação."


def valida_nome_subscritor_novo(formulario, documentos_identificacao):    
        check_doc_subscritor = nf_compara_subscritor_com_documento_novo(formulario, documentos_identificacao)
        if check_doc_subscritor < 0.90:
            return "O nome ou CPF/CNPJ do novo subscritor não correspondem aos documentos de identificação."
        elif check_doc_subscritor == 1.0:
            return "O nome e o CPF/CNPJ novo do subscritor correspondem aos documentos de identificação."
        elif check_doc_subscritor > 0.90:
            return f"O CPF/CNPJ corresponde ao do novo subscritor, mas o nome apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação."
        

def valida_nome_titular_atual(formulario, documentos_identificacao):
    check_doc_novo_titular = nf_compara_titular_com_documento_atual(formulario, documentos_identificacao)                                                
    if check_doc_novo_titular < 0.90:
        return "O nome ou CPF/CNPJ do titular não correspondem aos documentos de identificação."
    elif check_doc_novo_titular == 1.0:
        return "O nome e o CPF/CNPJ do titular correspondem aos documentos de identificação."
    elif check_doc_novo_titular > 0.90:                        
        return f"O CPF/CNPJ corresponde ao do novo titular, mas o nome apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos de identificação."
    

def valida_nome_titular_novo(formulario, documentos_identificacao):
    check_doc_novo_titular = nf_compara_titular_com_documento_novo(formulario, documentos_identificacao)                                                
    if check_doc_novo_titular < 0.90:
        return "O nome ou CPF/CNPJ do novo titular não correspondem aos documentos de identificação."
    elif check_doc_novo_titular == 1.0:
        return "O nome e o CPF/CNPJ do novo titular correspondem aos documentos de identificação."
    elif check_doc_novo_titular > 0.90:                        
        return f"O CPF/CNPJ corresponde ao do novo titular, mas o nome apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos de identificação."