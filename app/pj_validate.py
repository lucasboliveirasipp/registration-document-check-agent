from .formulario.formulario import Formulario
from .documentos.documento_empresa import DocumentoEmpresa
from .documentos.documento_identificacao import DocumentoIdentificacao
from .tools import calculate_similarity, only_numbers, remove_accents

def compara_subscritor_com_documento_empresa(form: Formulario, documento : DocumentoEmpresa, doc_iden: DocumentoIdentificacao):
    nome_subscritor = remove_accents(form.subscritor.nome)
    cpf_cnpj = only_numbers(form.subscritor.cpf_cnpj)
    if cpf_cnpj in documento.keys():
        return (calculate_similarity(remove_accents(documento[cpf_cnpj].razao_social), nome_subscritor), "PJ")
    elif cpf_cnpj in doc_iden.keys():
        return (calculate_similarity(remove_accents(doc_iden[cpf_cnpj].nome), nome_subscritor), "PF")
    return 0

def compara_representante_empresa(cpf_representante, nome_representante, documentos: DocumentoIdentificacao):
    cpf_representante = only_numbers(cpf_representante)      
    if cpf_representante in documentos.keys():
        return calculate_similarity(remove_accents(documentos[cpf_representante].nome), remove_accents(nome_representante))
    return 0

def verifica_nome_assinatura_subscritor_novo(form: Formulario):
    nome_subscritor_formulario = remove_accents(form.subscritor.nome)
    nome_subscritor_novo_atual = remove_accents(form.nome_subscritor_novo_atual)
    if form.nome_subscritor_novo_atual is not None:
        return calculate_similarity(nome_subscritor_novo_atual, nome_subscritor_formulario)        
    else:
        return 0

def compara_novo_titular_com_documento_empresa(form: Formulario, documentos : DocumentoEmpresa, doc_iden: DocumentoIdentificacao):
    nome_novo_titular = remove_accents(form.titular.nome_razao)
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_novo)
    
    if cpf_cnpj in documentos.keys():
        nome_novo_titular_empresa = remove_accents(documentos[cpf_cnpj].razao_social)
        return (calculate_similarity(nome_novo_titular, nome_novo_titular_empresa), "PJ")
    elif cpf_cnpj in doc_iden.keys():
        return (calculate_similarity(remove_accents(doc_iden[cpf_cnpj].nome), nome_novo_titular), "PF")
    return 0
        
    
def compara_antigo_titular_com_documento_empresa(form: Formulario, documentos : DocumentoEmpresa, doc_iden: DocumentoIdentificacao):
    cedente = remove_accents(form.titular.cedente)
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_cedente)
    if cpf_cnpj in documentos.keys():
        nome_antigo_titular_empresa = remove_accents(documentos[cpf_cnpj].razao_social)    
        return (calculate_similarity(cedente, nome_antigo_titular_empresa), "PJ")
    elif cpf_cnpj in doc_iden.keys():
        return (calculate_similarity(remove_accents(doc_iden[cpf_cnpj].nome), cedente), "PF")
    return 0

def verifica_assinatura_novo_titular(form: Formulario):
    nome_titular_formulario = remove_accents(form.titular.nome_razao)
    if form.titular.nome_razao is not None:
        return calculate_similarity(remove_accents(form.declaracao.nome_novo_titular), nome_titular_formulario)        
    else:
        return 0


def verifica_assinatura_antigo_titular(form: Formulario):
    nome_titular_formulario = remove_accents(form.titular.cedente)    
    if form.titular.cedente is not None:
        return calculate_similarity(remove_accents(form.declaracao.nome_antigo_titular), nome_titular_formulario)        
    else:
        return 0