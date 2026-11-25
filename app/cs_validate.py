from .documentos.documento_identificacao import DocumentoIdentificacao
from .documentos.comprovante_bancario import ComprovanteBancario
from .documentos.comprovante_endereco import ComprovanteEndereco
from .documentos.planilha import Planilha
from .tools import calculate_similarity, only_numbers, remove_accents, calculate_similarity_without_accents

    
def verificar_planilha_doc_identificacao(linha_planilha, documentos: DocumentoIdentificacao):  
    response = {}
    response["cpf_cnpj"] = False
    response["DocumentoIdentificacao"] = None   
    response["nome"] = 0 
    response["data_nascimento"] = 0
    if linha_planilha.cpf_cnpj in documentos:
        response["cpf_cnpj"] = True
        response["DocumentoIdentificacao"] = documentos[linha_planilha.cpf_cnpj]
        
        l_nome = remove_accents(linha_planilha.nome_razao_social)
        d_nome = remove_accents(documentos[linha_planilha.cpf_cnpj].nome)
        response["nome"] = calculate_similarity(l_nome, d_nome)        

        dt_nasc_planilha = linha_planilha.data_nascimento
        dt_nasc_documento = documentos[linha_planilha.cpf_cnpj].data_nascimento
        response["data_nascimento"] = calculate_similarity(dt_nasc_planilha, dt_nasc_documento)
    return response


def verificar_planilha_comp_bancario(linha_planilha: Planilha, comprovantes):  
    response = {}    
    response["nome"] = 0
    response["agencia"] = 0
    response["conta"] = 0
    response["ComprovanteBancario"] = None    

    for comp in comprovantes:        
        calc_nome = calculate_similarity_without_accents(comp.nome, linha_planilha.nome_razao_social)
        if calc_nome > 0.90:   
            response["nome"] = calc_nome   
            response["agencia"] = calculate_similarity(only_numbers(comp.agencia), (linha_planilha.agencia + linha_planilha.digito_agencia))
            response["conta"] = calculate_similarity(only_numbers(comp.conta), (linha_planilha.numero_conta + linha_planilha.digito_conta))
            response["ComprovanteBancario"] = comp
            break

    return response


def verificar_planilha_endereco(linha_planilha: Planilha, enderecos: ComprovanteEndereco):  
    response = {}
    response["nome"] = 0
    response["endereco_rua"] = 0
    response["cep"] = 0
    response["numero"] = 0
    response["complemento"] = 0
    response["bairro"] = 0
    response["cidade"] = 0
    response["ComprovanteEndereco"] = None
    
    for end in enderecos:
        nome_calc = calculate_similarity_without_accents(end.nome, linha_planilha.nome_razao_social)
        if nome_calc > 0.9:
            response["ComprovanteEndereco"] = end            
            response["nome"] = nome_calc
            response["endereco_rua"] = calculate_similarity_without_accents(linha_planilha.endereco, end.rua)            
            response["numero"] = calculate_similarity(linha_planilha.numero, end.numero)
            response["complemento"] = calculate_similarity_without_accents(linha_planilha.complemento, end.complemento)
            response["bairro"] = calculate_similarity_without_accents(linha_planilha.bairro, end.bairro)            
            response["cidade"] = calculate_similarity_without_accents(linha_planilha.cidade, end.cidade)     
            response["cep"] = calculate_similarity(only_numbers(linha_planilha.cep), only_numbers(end.cep))   

            notas = response["nome"]+response["endereco_rua"]+response["numero"]+response["complemento"]+response["bairro"]+response["cidade"]+response["cep"]
            response["analise"] = notas/7            
            break

    return response



def emoji_nota(val):    
    if val == 1:
        return "✅"
    elif val > 0.9:
        return "❔"
    else:
        return "❌"
    