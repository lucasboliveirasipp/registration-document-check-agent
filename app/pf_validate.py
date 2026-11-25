from .formulario.formulario import Formulario
from .tools import calculate_similarity, only_numbers, remove_accents

    
def compara_subscritor_com_documento(form: Formulario, documentos):
    nome_subscritor = remove_accents(form.subscritor.nome)
    cpf_cnpj = only_numbers(form.subscritor.cpf_cnpj)
    if cpf_cnpj in documentos:        
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), nome_subscritor)
    else:
        return 0

def verifica_nome_assinatura_subscritor_novo(form: Formulario):
    nome_subscritor_formulario = remove_accents(form.subscritor.nome)
    if form.nome_subscritor_novo_atual is not None:
        return calculate_similarity(remove_accents(form.nome_subscritor_novo_atual), nome_subscritor_formulario)        
    else:
        return 0

def compara_novo_titular_com_documento(form: Formulario, documentos):
    nome_novo_titular = remove_accents(form.titular.nome_razao)
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_novo)
    if cpf_cnpj in documentos:
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), nome_novo_titular)
    else:
        return 0
    
def compara_antigo_titular_com_documento(form: Formulario, documentos):
    cedente = remove_accents(form.titular.cedente)
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_cedente)
    if cpf_cnpj in documentos:
        return calculate_similarity(remove_accents(documentos[cpf_cnpj].nome), cedente)
    else:
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