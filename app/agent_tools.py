import json
import pandas as pd
import warnings
import os
import tempfile
import re
from .config import create_prompt_comprovante_bancario, create_prompt_doc, create_prompt_doc_identificacao, create_prompt_endereco, create_prompt_image, create_prompt_rec_cartorio, verifica_contrato_ata_prompt, verifica_procuracao, gpt_version
from .tools import create_completion, extract_text_from_pages, extrair_campos_formulario, extrair_campos_novo_formulario, extrair_texto_di, write_temp_file, toBase64
from .documentos.documento_identificacao import DocumentoIdentificacao
from .documentos.documento_empresa import DocumentoEmpresa
from .documentos.comprovante_endereco import ComprovanteEndereco
from .documentos.comprovante_bancario import ComprovanteBancario
from .documentos.responsavel_legal import ResponsavelLegal


temp_dir = tempfile.TemporaryDirectory()

def analisar_documento_identificacao(file) -> DocumentoIdentificacao:
    """
    Extrai um conjunto de informações de um documento de identificação
    :param file: file_uploader         
    """
    campos = ['nome', 'cpf', 'data_nascimento']

    obj_json = json.loads(analisar_texto_documento(file=file, campos=campos))

    return DocumentoIdentificacao(obj_json['nome'], obj_json['cpf'], obj_json['data_nascimento'])

def analisar_contrato(file, opcao, pagina_inicial, pagina_final):
    """
    Extrai um conjunto de informações de um contrato
    :param file: file_uploader         
    """         
                 
    temp_file_path = os.path.join(temp_dir.name, file.name)
    
    write_temp_file(file, temp_file_path)    

    texto = extract_text_from_pages(temp_file_path, pagina_inicial, pagina_final) 

    if opcao == "Procuração":
        campos = ['nome_outorgado', 'cpf_outorgado', 'cnpj_outorgante', 'razao_social_outorgante']
        messagens =  verifica_procuracao(campos, texto)
    else:
        campos = ['nome_responsavel_legal', 'cpf_responsavel_legal', 'cnpj', 'razao_social']        
        messagens =  verifica_contrato_ata_prompt(campos, texto)
    
    obj_json = json.loads(create_completion(messages=messagens, model=gpt_version))

    if opcao == "Procuração":
        responsaveis = [ResponsavelLegal(r["nome_outorgado"], r["cpf_outorgado"]) for r in obj_json["responsaveis"]]
    else:
        responsaveis = [ResponsavelLegal(r["nome_responsavel_legal"], r["cpf_responsavel_legal"]) for r in obj_json["responsaveis"]]

    return DocumentoEmpresa(responsaveis=responsaveis, cnpj=obj_json['cnpj'], razao_social=obj_json['razao_social'])


def analisar_endereco(file):
    """
    Extrai um conjunto de informações de um documento de endereço
    :param file: file_uploader         
    """        
    campos = ['nome', 'endereco', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'cep']
    temp_file_path = os.path.join(temp_dir.name, file.name)
    write_temp_file(file, temp_file_path)        
    texto = extrair_texto_di(temp_file_path) 
    messagens =  create_prompt_endereco(campos, texto)
    
    obj_json = json.loads(create_completion(messages=messagens, model=gpt_version))

    return ComprovanteEndereco(nome=obj_json["nome"], endereco=obj_json["endereco"], rua=obj_json["rua"], numero=obj_json["numero"], complemento=obj_json["complemento"], bairro=obj_json["bairro"], cidade=obj_json["cidade"], cep=obj_json["cep"])

def analisar_comprovante_banc(file):
    """
    Extrai um conjunto de informações de um comprovante bancário
    :param file: file_uploader         
    """                    
    temp_file_path = os.path.join(temp_dir.name, file.name)
    write_temp_file(file, temp_file_path)            
    
    texto = extrair_texto_di(temp_file_path) 

    #remove numeros de cartão de credito no padrão '0000 0000 0000 0000'
    texto = re.sub(r'\d{4}\s\d{4}\s\d{4}\s\d{4}', '', texto)

    messagens =  create_prompt_comprovante_bancario(texto)
    obj_json = json.loads(create_completion(messages=messagens, model=gpt_version))  

    return ComprovanteBancario(
        nome=obj_json["nome"],        
        instituicao=obj_json["instituicao"],        
        agencia=obj_json["agencia"],
        conta=obj_json["conta"])

def analisar_planilha(file):
    warnings.simplefilter(action='ignore', category=UserWarning)
    xls = pd.ExcelFile(file)
    df_clean = pd.read_excel(file, sheet_name=xls.sheet_names[0], header=1, dtype=str)
    dicionario_completo = df_clean.to_dict()   
    dicionario = {key.strip(): value for key, value in dicionario_completo.items()}

    def convertNan(val):
        return {k: ("" if pd.isna(v) else v) for k, v in val.items()}

    novo_dicionario = {
        'nome_razao_social': dicionario['Nome ou Razão Social'],
        'cpf_cnpj': convertNan(dicionario['Nº do CPF ou CNPJ']),
        'cep': convertNan(dicionario['CEP']),
        'endereco': dicionario['Endereço (Rua / Avenida)'],
        'numero': convertNan(dicionario['Nº']),
        'complemento': convertNan(dicionario['Complemento']),
        'bairro': dicionario['Bairro'],
        'cidade': dicionario['Cidade'],
        'estado': dicionario['Estado'],
        'banco': dicionario['Banco'],
        'agencia': dicionario['Agência Bancária'],
        'digito_agencia': convertNan(dicionario['Dígito da Agência']),
        'numero_conta': dicionario['Nº da Conta'],
        'digito_conta': convertNan(dicionario['Dígito da Conta']),
        'data_nascimento': dicionario['Data de Nascimento']
    }

    return novo_dicionario

def analisar_rec_cartorio(file):  
    """
    Extrai um conjunto de informações de um arquivo de firma reconhecida
    :param file: file_uploader         
    """        
    campos = ['nomes', 'cartorio', 'escrevente', 'codigo_autenticacao']                    
    temp_file_path = os.path.join(temp_dir.name, file.name)
    write_temp_file(file, temp_file_path)        
    texto = extrair_texto_di(temp_file_path)   
    messagens =  create_prompt_rec_cartorio(campos, texto)
    return create_completion(messages=messagens, model=gpt_version)

def analisar_formulario(file):
    """
    Extrai um conjunto de informações de um formulário
    :param file: file_uploader        
    """     
    temp_file_path = os.path.join(temp_dir.name, file.name)
    write_temp_file(file, temp_file_path)  

    texto = extrair_texto_di(temp_file_path)
    
    if "Agência Origem" not in texto:        
        return extrair_campos_novo_formulario(temp_file_path)     
    else:        
        return extrair_campos_formulario(temp_file_path)     
    

def analisar_texto_documento(file, campos: list):
    """
    Extrai um conjunto de informações de um arquivo
    :param file: file_uploader         
    :param campos: list 
    """     
    temp_file_path = os.path.join(temp_dir.name, file.name)

    write_temp_file(file, temp_file_path)        
    texto = extrair_texto_di(temp_file_path)       

    messagens = create_prompt_doc(campos, texto)

    return create_completion(messages=messagens, model=gpt_version)

def analisar_imagem(image):
    """
    Extrai informações de uma imagem
    :param image: file_uploader             
    """     
    temp_file_path = os.path.join(temp_dir.name, image.name)

    write_temp_file(image, temp_file_path)

    img_base64 = toBase64(temp_file_path)

    messages =  create_prompt_image(img_base64)

    return create_completion(messages=messages, model=gpt_version)


def analisar_imagem_documento(image, campos: list):
    """
    Extrai informações de uma imagem
    :param image: file_uploader         
    :param campos: list 
    """     
    temp_file_path = os.path.join(temp_dir.name, image.name)

    write_temp_file(image, temp_file_path)

    img_base64 = toBase64(temp_file_path)

    messages =  create_prompt_doc_identificacao(img_base64, campos)

    return create_completion(messages=messages, model=gpt_version)
