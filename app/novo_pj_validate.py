from .documentos.documento_identificacao import DocumentoIdentificacao
from .documentos.documento_empresa import DocumentoEmpresa
from .titulo_capitalizacao.titulo_capitalizacao import TituloCapitalizacao
from .tools import calculate_similarity, only_numbers, remove_accents

def nf_verifica_subscritor(form: TituloCapitalizacao, doc_emp, doc_iden, atual: bool):        
    cpf_cnpj = only_numbers(form.subscritor.cpf_cnpj_atual if atual else form.subscritor.cpf_cnpj_novo)  
    nome = remove_accents(form.subscritor.nome_atual if atual else form.subscritor.nome_novo)    
    if cpf_cnpj in doc_emp.keys():
        return calculate_similarity(remove_accents(doc_emp[cpf_cnpj].razao_social), nome)
    elif cpf_cnpj in doc_iden.keys():
        return calculate_similarity(remove_accents(doc_iden[cpf_cnpj].nome), nome)          
    return 0

def nf_verifica_titular(form: TituloCapitalizacao, doc_emp : DocumentoEmpresa, doc_iden: DocumentoIdentificacao, atual: bool):        
    cpf_cnpj = only_numbers(form.titular.cpf_cnpj_atual if atual else form.titular.cpf_cnpj_novo)
    nome = remove_accents(form.titular.nome_atual if atual else form.titular.nome_novo)
    if cpf_cnpj in doc_emp.keys():
        return calculate_similarity(remove_accents(doc_emp[cpf_cnpj].razao_social), nome)
    elif cpf_cnpj in doc_iden.keys():
        return calculate_similarity(remove_accents(doc_iden[cpf_cnpj].nome), nome)              
    return 0

def nf_compara_representante(cpf_representante, nome_representante, documentos: DocumentoIdentificacao):    
    if cpf_representante in documentos.keys():            
        return calculate_similarity(remove_accents(documentos[cpf_representante].nome), remove_accents(nome_representante))
    return 0
    
def buscar_assinatura_por_cpf_cnpj(lista_assinaturas, cpf_cnpj_atual, tipo_assinatura):
    return next((assinatura for assinatura in lista_assinaturas if assinatura.cpf_cnpj == cpf_cnpj_atual and assinatura.tipo_assinatura == tipo_assinatura), None)

def valida_subscritor_atual(formulario, documentos_empresas, documentos_identificacao):
    check_doc_subscritor = nf_verifica_subscritor(formulario, documentos_empresas, documentos_identificacao, atual=True)    
    if check_doc_subscritor < 0.90:
        return "O nome/razão social ou CPF/CNPJ do subscritor não correspondem aos documentos de identificação."
    elif check_doc_subscritor == 1.0:
        return "O nome/razão social e o CPF/CNPJ do subscritor correspondem aos documentos de identificação."
    elif check_doc_subscritor > 0.90:
        return f"O CPF/CNPJ corresponde ao do subscritor, mas o nome/razão social apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação."

def valida_subscritor_novo(formulario, documentos_empresas, documentos_identificacao):
    check_doc_subscritor = nf_verifica_subscritor(formulario, documentos_empresas, documentos_identificacao, atual=False)
    if check_doc_subscritor < 0.90:
        return "O nome/razão social ou CPF/CNPJ do novo subscritor não correspondem aos documentos de identificação."
    elif check_doc_subscritor == 1.0:
        return "O nome/razão social e o CPF/CNPJ do novo subscritor correspondem aos documentos de identificação."
    elif check_doc_subscritor > 0.90:
        return f"O CPF/CNPJ corresponde ao do novo subscritor, mas o nome/razão social apresenta "+ "{:.2%}".format(check_doc_subscritor)+" de similaridade com os documentos de identificação."

    
def valida_titular_novo(formulario, documentos_empresas, documentos_identificacao):
    check_doc_novo_titular = nf_verifica_titular(formulario, documentos_empresas, documentos_identificacao, atual=False)                                                        
    if check_doc_novo_titular < 0.90:
        return "O nome/razão social ou CPF/CNPJ do novo titular não correspondem aos documentos da empresa."
    elif check_doc_novo_titular == 1.0:
        return "O nome/razão social e o CPF/CNPJ do novo titular correspondem aos documentos da empresa."
    elif check_doc_novo_titular > 0.90:                        
        return f"O CPF/CNPJ corresponde ao do novo titular, mas o nome/razão social apresenta "+ "{:.2%}".format(check_doc_novo_titular)+" de similaridade com os documentos da empresa."

def valida_titular_atual(formulario, documentos_empresas, documentos_identificacao):
    check_doc_cedente = nf_verifica_titular(formulario, documentos_empresas, documentos_identificacao, atual=True)    
    if check_doc_cedente < 0.90:
        return "O nome/razão social ou CPF/CNPJ do titular não correspondem aos documentos da empresa."
    elif check_doc_cedente == 1.0:
        return "O nome/razão social e o CPF/CNPJ do titular correspondem aos documentos da empresa."
    elif check_doc_cedente > 0.90:                        
        return f"O CPF/CNPJ corresponde ao do titular, mas o nome/razão social apresenta "+ "{:.2%}".format(check_doc_cedente)+" de similaridade com os documentos de identificação."
    
def valida_representante(documentos_identificacao, doc_emp):       
    check_doc_representante = nf_compara_representante(doc_emp.cpf_responsavel_legal, doc_emp.nome_responsavel_legal, documentos_identificacao)
    if check_doc_representante < 0.90:
        return "O nome ou CPF do representante legal não correspondem aos documentos de identificação."
    elif check_doc_representante == 1.0:
        return "O nome e o CPF do representante legal correspondem aos documentos de identificação."
    elif check_doc_representante > 0.90:                        
        return f"O CPF corresponde ao do representante legal, mas o nome apresenta "+ "{:.2%}".format(check_doc_representante)+" de similaridade com os documentos de identificação."
