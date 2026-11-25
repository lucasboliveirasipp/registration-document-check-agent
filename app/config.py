gpt_version = "gpt-4o-mini"

def verifica_contrato_ata_prompt(campos: list, texto: str):
    system = f"Você é um assistente de IA especialista em extração de informações de contratos."

    prompt = f"""Identifique os responsáveis pela administração.
             Extraia os seguintes *campos*: {campos}. Caso não encontre as informações correspondentes aos campos solicitados, responda *""* .
             Contrato: {texto}.
             Retorne as informações em JSON neste formato
             
             
             {{
                razao_social: (razao social da empresa),
                cnpj: (cnpj da empresa),
                responsaveis: [
                    {{
                        nome_responsavel_legal: (nome do responsavel legal),
                        cpf_responsavel_legal: (cpf do responsavel legal)
                    }}
                    ]
            }}
            """


    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages

def verifica_procuracao(campos: list, texto: str):
    system = f"Você é responsável por verificar e extrair informações solicitadas de um *texto* enviado pelo usuário." \
             f"A informação deve ser retornada num json com os *campos* indicados pelo usuário." \
             f"Caso não encontre as informações correspondentes aos campos solicitados, responda *None* ."

    prompt = f"""Dado o texto a seguir, extraia os seguintes *campos*: {campos}.
             Os resultados devem ser retornados em formato JSON, correspondendo exatamente aos campos solicitados.
             Este aqui é o *texto*: {texto}.
             
             Retorne as informações em JSON neste formato
             
             
             {{
                razao_social: (razao social da empresa),
                cnpj: (cnpj da empresa),
                responsaveis: [
                    {{
                        nome_outorgado: (nome do outorgado),
                        cpf_outorgado: (cpf do outorgado)
                    }}
                    ]
            }}
            """

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages


def verifica_contrato_prompt(campos: list, texto: str):
    system = f"Você é responsável por verificar e extrair informações solicitadas de um *texto* enviado pelo usuário." \
             f"A informação deve ser retornada num json com os *campos* indicados pelo usuário." \
             f"Caso não encontre as informações correspondentes aos campos solicitados, responda *None* ."

    prompt = f"Dado o texto a seguir, verifique e extraia os seguintes *campos*: {campos}." \
             f"Retorne as palavras chaves em formato json." \
             f"Utilize as informações contidas no texto e busque as informações do responsável pela administração ou responsável legal." \
             f"Este aqui é o *texto*: {texto}."

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages

def create_prompt_doc(campos: list, texto: str):
    system = f"Você é responsável por extrair informações solicitadas de um *texto* enviado pelo usuário." \
             f"A informação deve ser retornada num json com os *campos* indicados pelo usuário." \
             f"Caso não encontre as informações correspondentes aos campos solicitados, responda *None* ."

    prompt = f"Dado o texto a seguir, extraia os seguintes *campos*: {campos}." \
             f"Retorne as palavras chaves em formato json." \
             f"Pegue as informações contidas no texto." \
             f"Este aqui é o *texto*: {texto}."

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages

def create_prompt_rec_cartorio(campos: list, texto: str):
    system = f"Você é responsável por verificar o reconhecimento das firmas e extrair informações solicitadas de um *texto* enviado pelo usuário." \
             f"As informações devem ser retornadas num json com os *campos* indicados pelo usuário." \
             f"Caso não encontre as informações correspondentes aos campos solicitados, responda *None* ."

    prompt = f"Dado o texto a seguir, extraia os seguintes *campos*: {campos}." \
             f"Retorne as palavras chaves em formato json." \
             f"Pegue as informações contidas no texto." \
             f"Este aqui é o *texto*: {texto}."

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages

def create_prompt_endereco(campos: list, texto: str):
    system = f"Você é responsável por extrair informações de endereço solicitadas de um *texto* enviado pelo usuário." \
             f"As informações retornadas devem ser do endereço do cliente." \
             f"A informação deve ser retornada num json com os *campos* indicados pelo usuário." \
             f"Caso não encontre as informações correspondentes aos campos solicitados, responda *None* ."

    prompt = f"Dado o texto a seguir, extraia os seguintes *campos*: {campos}." \
             f"Retorne as palavras chaves em formato json." \
             f"Pegue as informações contidas no texto." \
             f"Este aqui é o *texto*: {texto}."
    

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages

def create_prompt_image(img_base64: str):
    system = f"Você é responsável por extrair informações solicitadas de uma *imagem* enviada pelo usuário." \
                 f"A informação deve ser retornada num json "

    prompt = f"Dada a imagem a seguir, extraia os seguintes *campos*: ['nome', 'numero_de_identidade', 'rg', 'cpf', 'data_de_nascimento','cpf', 'data_emissão_rg', 'data_nascimento', 'orgao_emissor', 'orgao_expedidor']."


    messages=[{"role": "system", "content": system},
                  {"role": "user", "content":
                      [
                          {"type": "text", "text": prompt},
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}

                      ]
                   },
                  ]
    return messages

def create_prompt_doc_identificacao(img_base64: str, campos: list):
    system = f"Você é responsável por extrair informações solicitadas de uma *imagem* enviada pelo usuário." \
             f"Retorne as palavras chaves em formato json." \
             f"Caso não encontre as informações correspondentes aos campos solicitados, responda *None* "    

    prompt = f"Dada a imagem a seguir, extraia os seguintes *campos*: {campos}." \
             f"a data de nascimento deve vir no padrão dd/MM/yyyy"

    messages=[{"role": "system", "content": system},
                  {"role": "user", "content":
                      [
                          {"type": "text", "text": prompt},
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}

                      ]
                   },
                  ]
    return messages

def create_prompt_comprovante_bancario(texto: str):
    system = f"Você é um assistente de IA especialista em extração de informações bancarias."           

    prompt = f"Identifique os dados bancarios e retorne as informações solicitadas em JSON, ignorando numeros de cartões de credito."\
             f"Extraia os seguintes 'nome', 'instituicao', 'agencia', 'conta'. Caso não encontre as informações correspondentes aos campos solicitados, responda *None* ." \
             f"Comprovante bancario: {texto}."

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return messages
