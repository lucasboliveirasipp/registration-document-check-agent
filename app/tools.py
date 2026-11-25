# Carrega variáveis do arquivo .env mais próximo (pasta do projeto)
def _carregar_env():
    from pathlib import Path
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    for pasta in Path(__file__).resolve().parents:
        if (pasta / ".env").exists():
            load_dotenv(pasta / ".env")
            break


_carregar_env()

from openai import AzureOpenAI
import os  
import pdfplumber
import base64
import unidecode
import re
from datetime import datetime
from difflib import SequenceMatcher
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from .titulo_capitalizacao.titular_cap import TitularCap
from .titulo_capitalizacao.assinatura import Assinatura
from .titulo_capitalizacao.enums.tipo_assinatura import TipoAssinatura
from .titulo_capitalizacao.enums.forma_pagamento import FormaPagamento
from .titulo_capitalizacao.enums.tipo_conta import TipoConta
from .titulo_capitalizacao.enums.forma_assinatura import FormaAssinatura
from .titulo_capitalizacao.enums.tipo_documento import TipoDocumento
from .titulo_capitalizacao.subscritor_cap import SubscritorCap
from .titulo_capitalizacao.titulo import Titulo
from .titulo_capitalizacao.titulo_capitalizacao import TituloCapitalizacao
from .formulario.formulario import Formulario
from .formulario.contrato_titular import ContratoTitular
from .formulario.subscritor import Subscritor
from .formulario.titular import Titular
from .formulario.declaracao import Declaracao
from .documentos.planilha import Planilha

os.environ['MODELO_FORMULARIO'] = "model-cap-rec"
os.environ['MODELO_NOVO_FORMULARIO'] = "cap-novo-form-v3"
os.environ['API_VERSION_OPENAI'] = "2024-02-15-preview"

#Instancia do client da OpenAI
client = AzureOpenAI(api_key=os.getenv("API_KEY_OPENAI_AZURE")
                    ,azure_endpoint=os.getenv("ENDPOINT_AZURE_OPENAI")
                    ,api_version=os.getenv("API_VERSION_OPENAI"))

#Instancia do client do DocumentIntelligence
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=os.getenv("ENDPOINT_AZURE"), credential=AzureKeyCredential(os.getenv("KEY_AZURE"))
)

def extrair_texto_di(file_path: str) -> str:
    """
    Extrai texto de um arquivo utilizando Document Intelligence         
    :param file_path: str
    
    :return str texto do documento
    """

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=f.read())
        )

    result: AnalyzeResult = poller.result()

    for page in result.pages:
        texto_completo = []
        for _, line in enumerate(page.lines):
            texto_completo += line.content + "\n "
        return ''.join(texto_completo)

def extrair_campos_formulario(file_path: str) -> Formulario:    

    """
    Extrai as informações de um arquivo utilizando o um modelo treinado do Document Intelligence       
    :param file_path: str
    
    :return Formulario
    """
        
    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            os.getenv("MODELO_FORMULARIO"), AnalyzeDocumentRequest(bytes_source=f.read())
        )

    modelo = poller.result()

    def get_form_content(form):
        def get_content(param):
            if form.fields.get(param) and form.fields.get(param).get('content') is not None:                
                return form.fields.get(param).get('content')
            else:
                return ""
        return get_content

    def get_form_signature(form):
        def get_signature(param):
            if form.fields.get(param) and form.fields.get(param).get('valueSignature') is not None:
                return form.fields.get(param).get('valueSignature')
            else:
                return "unsigned"
        return get_signature    
    
    if modelo.documents:
         for _, form in enumerate(modelo.documents):
            get = get_form_content(form)
            get_signature = get_form_signature(form)

            opcao = 0
            if get("opcao1") == ':selected:':
                opcao = 1
                #A, B e E
            elif get("opcao2") == ':selected:':
                opcao = 2
                #A, C e D
            elif get("opcao3") == ':selected:':
                opcao = 3
                #A, B, C, D e E
            elif get("opcao4") == ':selected:':
                opcao = 4            

            form = Formulario(opcao=opcao)

            #Bloco A
            for i in range(1, 7):
                if get(f"a_nct_{i}_serie"):
                    form.contratos_titular.append(ContratoTitular(n_serie=only_numbers(get(f"a_nct_{i}_serie")), n_serie_dig=only_numbers(get(f"a_nct_{i}_serie_dig")), n_combinacao=only_numbers(get(f"a_nct_{i}_comb")), n_combinacao_dig=only_numbers(get(f"a_nct_{i}_comb_dig"))))
          
            #Bloco B
            form.subscritor = Subscritor(nome=get("b_nome"), cpf_cnpj=only_numbers(get("b_cpf_cpnj_mf")), filial=get("b_filial"), contr=get("b_contr"), codigo_agencia=get("b_codigo_agencia"), codigo_agencia_dig=get("b_codigo_agencia_dig"), razao=get("b_razao"), conta=get("b_conta"), conta_dig=get("b_conta_dig"))
            
            #Bloco C
            form.titular = Titular(cedente=get("c_tit_cedente"), 
                    cpf_cnpj_cedente=get("c_tit_cpf_cnpj_mf"), 
                    filial_cedente=get("c_tit_filial"), 
                    contr_cedente=get("c_tit_contr"),
                    nome_razao=get("c_ntit_nome_razao"),
                    cpf_cnpj_novo=get("c_ntit_cpf_cnpj_mf"),
                    filial_novo=get("c_ntit_filial"),
                    contr_novo=get("c_ntit_contr"),
                    dt_nasc_const_emp=get("c_ntit_dt_nasc_const_emp"),
                    tipo_doc=get("c_ntit_tipo_doc"),
                    numero_documento=get("c_ntit_n_doc"),
                    orgao_emissor=get("c_ntit_orgao_emissor"),
                    data_emissao=get("c_ntit_dt_emissao"),
                    endereco_completo=get("c_ntit_endereco_completo"),
                    bairro=get("c_ntit_bairro"),
                    cidade=get("c_ntit_cidade"),
                    uf=get("c_ntit_uf"),
                    cep=get("c_ntit_cep"),
                    ddd=get("c_ntit_ddd"),
                    telefone=get("c_ntit_telefone"),
                    profissao_ativ_principal=get("c_ntit_profissao_ativ_principal"))

            #Bloco D
            form.declaracao = Declaracao(nome_novo_titular=get("d_nome_novo_titular"), 
                       nome_antigo_titular=get("d_nome_antigo_titular"),
                       reserva=get("d_reserva_total"),
                       assinatura_novo_titular=get_signature("d_assinatura_novo_titular"),
                       assinatura_antigo_titular=get_signature("d_assinatura_antigo_titular"))                      

            #Bloco E
            form.nome_subscritor_novo_atual = get("e_nome_novo_atual_subscritor")
            form.assinatura_subscritor_novo_atual = get_signature("e_assinatura_subscritor_novo_atual")
            form.nome_subscritor_antigo = get("e_nome_antigo_subscritor")    
            form.assinatura_subscritor_antigo = get_signature("e_assinatura_subscritor_antigo")
           
            #Procurador
            form.assinatura_procurador = get_signature("assinatura_procurador")
                        
    return form
    
def create_completion(messages: str, model: str, temperature=0, max_tokens=1000) :
    """
    Cria uma requisição e retorna o valor em json
    :param messages: str        
    :param model: str
    :param temperature: int
    :param max_tokens: int                
    
    :return json_object
    """
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        response_format={"type": "json_object"},
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return chat_completion.choices[0].message.content


def write_temp_file(file, temp_file_path: str):    
    """
    Escreve o conteúdo de um arquivo binário em um local específico no sistema de arquivos.   
    :param file: UploadedFile        
    :param temp_file_path: str                   
    """
    with open(temp_file_path, "wb") as f:
        f.write(file.getvalue())

def extract_text(file, temp_dir) -> str:
    """
    Extrai o texto de um arquivo e retorna uma str
    :param file: UploadedFile        
    :param temp_file_path: str     

    :return texto str
    """
    texto = []
    with pdfplumber.open(os.path.join(temp_dir.name, file.name)) as pdf:
        all_text = ''
        for page in pdf.pages:
            all_text += page.extract_text()
        if all_text == '':
            return texto
        texto.append((file.name, all_text))
        return texto

def toBase64(path) -> str:
    """
    Converte um arquivo binário em uma string codificada em Base64.
    :param path: str

    :return texto str       
    """
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode('utf-8')
  

def remove_accents(value) -> str:
    """
    Remove os acentos de uma string.
    :param path: str

    :return texto str       
    """
    return unidecode.unidecode(value)

def compare_name(name1, name2) -> bool:
    """
    Compara dois nomes, ignorando acentos e diferenças de maiúsculas/minúsculas.
    :param name1: str
    :param name2: str

    :return bool
    """
    name1 = remove_accents(name1.lower())
    name2 = remove_accents(name2.lower())
    return name1 == name2

def only_numbers(val):
    """
    Remove todos os caracteres não numéricos de uma string.
    
    :param val: A string de entrada que pode conter caracteres não numéricos.
    
    :return: Uma string contendo apenas os números da entrada. Se o valor de entrada não for uma string, retorna uma string vazia.
    """
    if val is None or not isinstance(val, str):
        return val
        
    return re.sub(r'\D', '', val)

def calculate_similarity(a, b) -> float:
    """
    Calcula a similaridade entre duas strings utilizando a razão de similaridade do algoritmo SequenceMatcher.
    :param a: str
    :param b: str

    Um valor de ponto flutuante entre 0 e 1, onde 1 indica que as strings são idênticas e 0 indica que não possuem similaridade.
    :return float
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def format_cpf_cnpj(doc: str):
    """
    Formata um cpf ou cnpj
    :param doc: str    
    :return str
    """
    documento = only_numbers(doc)

    if len(documento) >= 11 and len(documento) < 14:        
        return f"{documento[:3]}.{documento[3:6]}.{documento[6:9]}-{documento[9:]}"
    elif len(documento) >= 14:           
        return f"{documento[:2]}.{documento[2:5]}.{documento[5:8]}/{documento[8:12]}-{documento[12:]}"
    else:
        return documento
    

def dict_to_planilhas(data):
        planilhas = [
            Planilha(
                nome_razao_social=data['nome_razao_social'][i],
                cpf_cnpj=data['cpf_cnpj'][i],
                cep=data['cep'][i],
                endereco=data['endereco'][i],
                numero=data['numero'][i],
                complemento=data['complemento'][i],
                bairro=data['bairro'][i],
                cidade=data['cidade'][i],
                estado=data['estado'][i],
                banco=data['banco'][i],
                agencia=data['agencia'][i],
                digito_agencia=data['digito_agencia'][i],
                numero_conta=data['numero_conta'][i],
                digito_conta=data['digito_conta'][i],
                data_nascimento=converter_data(data['data_nascimento'][i])
            )
            for i in range(len(data['cpf_cnpj']))
        ]

        return planilhas 

def converter_data(data_original):                              
    data_obj = datetime.strptime(data_original, '%Y-%m-%d %H:%M:%S')    
    return data_obj.strftime('%d/%m/%Y')
    

def calculate_similarity_without_accents(a, b) -> float:
    a = remove_accents(a)
    b = remove_accents(b)
    """
    Calcula a similaridade entre duas strings sem acentuação utilizando a razão de similaridade do algoritmo SequenceMatcher.
    :param a: str
    :param b: str

    Um valor de ponto flutuante entre 0 e 1, onde 1 indica que as strings são idênticas e 0 indica que não possuem similaridade.
    :return float
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()



def extrair_campos_novo_formulario(file_path: str) -> TituloCapitalizacao:    

    """
    Extrai as informações de um arquivo utilizando o um modelo treinado do Document Intelligence       
    :param file_path: str
    
    :return Formulario
    """
        
    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            os.getenv("MODELO_NOVO_FORMULARIO"), AnalyzeDocumentRequest(bytes_source=f.read())
        )

    modelo = poller.result()

    def get_form_content(form):
        def get_content(param):
            if form.fields.get(param) and form.fields.get(param).get('content') is not None:                
                return form.fields.get(param).get('content')
            else:
                return ""
        return get_content
    
    def get_form_table(form):
        def get_table(param):
            if form.fields.get(param) and form.fields.get(param).get('valueArray') is not None:                
                return form.fields.get(param).get('valueArray')
            else:
                return ""
        return get_table

    def get_form_signature(form):
        def get_signature(param):
            if form.fields.get(param) and form.fields.get(param).get('valueSignature') is not None:
                return form.fields.get(param).get('valueSignature')
            else:
                return "unsigned"
        return get_signature    
        
    def get_form_vo(valueObject):
        def get_vo_value(param):        
            if valueObject.get("valueObject") and valueObject.get("valueObject").get(param).get("content") is not None:                
                return valueObject.get("valueObject").get(param).get("content")
            else:
                return ""
        return get_vo_value
    
    if modelo.documents:
         for _, form in enumerate(modelo.documents):
            get = get_form_content(form)
            get_signature = get_form_signature(form)
            get_table = get_form_table(form)
            

            opcao = 0
            if get("opcao1") == ':selected:':
                opcao = 1
            elif get("opcao2") == ':selected:':
                opcao = 2
            elif get("opcao3") == ':selected:':
                opcao = 3
            elif get("opcao4") == ':selected:':
                opcao = 4            

            formulario = TituloCapitalizacao(opcao=opcao)            

            table = get_table("tb_titulos")
            titulos = []
            for x in table:
                get_vo = get_form_vo(x)                
                titulos.append(Titulo(quantidade=get_vo("Quantidade"), serie=get_vo("Série"), titulo_inicial=get_vo("Título Inicial"), titulo_final=get_vo("Título Final")))

            formulario.titulos = titulos

            formulario.forma_pagamento = FormaPagamento.BOLETO.value if get("fp_ck_boleto") == ':selected:' else FormaPagamento.CONTA.value                           
            formulario.agencia = get("fp_agencia")
            formulario.conta = get("fp_conta")
            formulario.tipo_conta = TipoConta.CORRENTE.value if get("fa_ck_assinatura_fisica") == ':selected:' else TipoConta.POUPANCA.value

            formulario.titular = TitularCap(nome_atual=get("at_nome"),
                          cpf_cnpj_atual=get("at_cpf_cnpj"),
                          grau_parentesco_novo=get("at_grau_parentesco"),
                          nome_novo=get("nt_nome"),
                          cpf_cnpj_novo=get("nt_cpf_cnpj"),
                          cep_novo=get("nt_cep"),
                          endereco_novo=get("nt_endereco"),
                          bairro_novo=get("nt_bairro"),
                          cidade_novo=get("nt_cidade"),
                          uf_novo=get("nt_uf"))
                        
            formulario.subscritor = SubscritorCap(nome_atual=get("as_nome"),
                          cpf_cnpj_atual=get("as_cpf_cnpj"),
                          grau_parentesco_novo=get("as_grau_parentesco"),
                          nome_novo=get("ns_nome"),
                          cpf_cnpj_novo=get("ns_cpf_cnpj"),
                          cep_novo=get("ns_cep"),
                          endereco_novo=get("ns_endereco"),
                          bairro_novo=get("ns_bairro"),
                          cidade_novo=get("ns_cidade"),
                          uf_novo=get("ns_uf"))
            
            formulario.local = get("local")
            formulario.data = get("data")
            
            formulario.forma_assinatura = FormaAssinatura.FISICA.value if get("fa_ck_assinatura_fisica") == ':selected:' else FormaAssinatura.DIGITAL.value
            
            at_ck_cpf = get("at_ck_cpf")
            at_ck_cnpj = get("at_ck_cnpj")
            nt_ck_cpf = get("nt_ck_cpf")
            nt_ck_cnpj = get("nt_ck_cnpj")  

            if at_ck_cpf or at_ck_cnpj:
                formulario.tipo_documento_titular = TipoDocumento.CPF if at_ck_cpf == ':selected:' else TipoDocumento.CNPJ

            if nt_ck_cpf or nt_ck_cnpj:
                formulario.tipo_documento_subscritor = TipoDocumento.CPF if nt_ck_cpf == ':selected:' else TipoDocumento.CNPJ
            
            assinaturas = []
            if get("at_ass_nome_1"):
                assinaturas.append(Assinatura(nome=get("at_ass_nome_1"), cpf_cnpj=get("at_ass_cpf_cnpj_1"), assinatura="", tipo_assinatura=TipoAssinatura.TITULAR_ATUAL.value))
            if get("at_ass_nome_2"):
                assinaturas.append(Assinatura(nome=get("at_ass_nome_2"), cpf_cnpj=get("at_ass_cpf_cnpj_2"), assinatura="", tipo_assinatura=TipoAssinatura.TITULAR_ATUAL.value))
            if get("nt_ass_nome_1"):
                assinaturas.append(Assinatura(nome=get("nt_ass_nome_1"), cpf_cnpj=get("nt_ass_cpf_cnpj_1"), assinatura="", tipo_assinatura=TipoAssinatura.TITULAR_NOVO.value))
            if get("nt_ass_nome_2"):
                assinaturas.append(Assinatura(nome=get("nt_ass_nome_2"), cpf_cnpj=get("nt_ass_cpf_cnpj_2"), assinatura="", tipo_assinatura=TipoAssinatura.TITULAR_NOVO.value))
            if get("as_ass_nome_1"):
                assinaturas.append(Assinatura(nome=get("as_ass_nome_1"), cpf_cnpj=get("as_ass_cpf_cnpj_1"), assinatura="", tipo_assinatura=TipoAssinatura.SUBSCRITOR_ATUAL.value))
            if get("as_ass_nome_2"):
                assinaturas.append(Assinatura(nome=get("as_ass_nome_2"), cpf_cnpj=get("as_ass_cpf_cnpj_2"), assinatura="", tipo_assinatura=TipoAssinatura.SUBSCRITOR_ATUAL.value))
            if get("ns_ass_nome_1"):
                assinaturas.append(Assinatura(nome=get("ns_ass_nome_1"), cpf_cnpj=get("ns_ass_cpf_cnpj_1"), assinatura="", tipo_assinatura=TipoAssinatura.SUBSCRITOR_NOVO.value))
            if get("ns_ass_nome_2"):
                assinaturas.append(Assinatura(nome=get("ns_ass_nome_2"), cpf_cnpj=get("ns_ass_cpf_cnpj_2"), assinatura="", tipo_assinatura=TipoAssinatura.SUBSCRITOR_NOVO.value))
            if get("gerente_ass_nome"):
                assinaturas.append(Assinatura(nome=get("gerente_ass_nome"), cpf_cnpj=get("gerente_ass_cpf_cnpj"), assinatura="", tipo_assinatura=TipoAssinatura.GERENTE.value))

            formulario.assinaturas = assinaturas
                
        
    return formulario

def extract_text_from_pages(file_path: str, pagina_inicial=None, pagina_final=None) -> str:
    """
    Extrai texto das paginas informadas de arquivo utilizando Document Intelligence       
    :param file_path: str
    
    :return str texto do documento
    """

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=f.read())
        )

    result: AnalyzeResult = poller.result()

    if pagina_inicial is None or pagina_inicial == 0:
        pagina_inicial = 1
    if pagina_final is None or pagina_final == 0:
        pagina_final = len(result.pages)
    
    if pagina_final > len(result.pages): 
        raise ValueError(f"A página final é maior que o número de páginas no documento ({len(result.pages)} páginas).")     
    if pagina_inicial > pagina_final: 
        raise ValueError("A página inicial é maior que a página final.")

    texto_completo = []
    for page in result.pages[pagina_inicial - 1:pagina_final]:
        for _, line in enumerate(page.lines):
            texto_completo += line.content + "\n "
    return ''.join(texto_completo)


