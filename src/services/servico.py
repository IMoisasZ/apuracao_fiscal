import pandas as pd
import uuid
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

class ApuracaoService:
    @staticmethod
    def executar(livro_empresa: str, livro_contabilidade: str):
        # Leitura das planilhas
        df_livro_empresa = pd.read_excel(livro_empresa)
    
        # ***************** Empresa *****************
        # Renomeando colunas
        df_livro_empresa = df_livro_empresa.rename(columns={
            "Nº NF": "num_nf",
            "Apelido/Nome Abreviado": "nome_abreviado",
            "CPF / CNPJ": "cpf_cnpj",
            "Serviço": "valor_servico"
        })

        # Removndo linhas em branco
        df_livro_empresa.dropna()

        # ***************** Dados para apuração *****************
        # Remover colunas descecessárias
        lista_colunas_para_remover = ['Série','Receb.', 'Fornec.', 'Base Cálc. ICMS ','ICMS','Base Cálc. ICMS ST','ICMS ST','Base Cálc. Serv.','ISS','Valor Total','Valor Fatura','ICMS Abat.','PIS Abat.','COFINS Abat.','Total Abat.','PIS Ret.','COFINS Ret.','CSLL Ret.','IR Ret.','INSS Ret.','ISS Ret.','Outros Ret.','Total Ret.',]
        df_livro_empresa = df_livro_empresa.drop(columns=lista_colunas_para_remover)

        # Renomear colunas
        df_livro_empresa = df_livro_empresa.rename(columns={
            "Nº NF": "num_nf", 
            "Apelido/Nome Abreviado": "nome_abreviado", 
            "CPF / CNPJ": "cpf_cnpj",
            "Serviço": "valor_servico"
        })

        # Criando ID unico
        df_livro_empresa["id"] = df_livro_empresa["num_nf"].astype("str") + "|" + df_livro_empresa["cpf_cnpj"].str.replace("/","", regex=False).str.replace(".","", regex=False).str.replace("-","", regex=False)
        df_livro_empresa = df_livro_empresa.drop(columns=["cpf_cnpj", "num_nf"])
        # Somando valores duplicados
        df_livro_empresa = df_livro_empresa.groupby(by=["id"], as_index=False).sum()

        # ***************** Contabilidade *****************
        # Coleta de dados
        df_contabilidade = pd.read_excel(livro_contabilidade)

        # ***************** Separando colunas para guardar *****************
        df_contabilidade = df_contabilidade.drop(columns=['Cnpj Empresa','Código Empresa','Empresa','Municipio Tomador','Conferido?','#Id','Código Verificador','Data Competência','Emissão RPS','Emissão NFe','Cancelamento','Exclusão','Pagamento','Parcelas','Pagamento Parcelado Antecipado?','CCM/IM Prestador','Município Prestador','Código Indicador Operação de Fornecimento','Tem CPOM','Regime Tributário','NBS','CNAE','CNAE Descrição','Desconto Incondicionado','Serviço Federal','Serviço Municipal','N. Referência','Serviço Dentro do Município','Base de Cálculo ISS','% ISS Dentro do Município','ISS Dentro do Município','% ISS Fora do Município','ISS Fora do Município','Município Devido o ISS','% CSRF','DARF CSRF','Valor CSRF','% PIS','DARF PIS','Valor PIS','% COFINS','DARF COFINS','Valor COFINS','% CSLL','DARF CSLL','Valor CSLL','% IRRF','DARF IRRF','Valor IRRF','Natureza de Rendimento REINF','Base de Cálculo INSS','% INSS','Valor INSS','Código REINF INSS','Código de Classificação Tributária','Código de Classificação Tributária Regular','Base de Cálculo IBS/CBS','Alíquota UF IBS','Redução Alíquota UF IBS','Alíquota Efetiva UF IBS','Alíquota Estadual Regular IBS','Percentual Diferimento Estadual IBS','Alíquota Estadual Compra Gov IBS','Valor Estadual Regular IBS','Total Diferimento Estadual IBS','Valor Estadual Compra Gov IBS','Valor UF IBS','Alíquota Municipal IBS','Redução Alíquota Municipal IBS','Alíquota Efetiva Municipal IBS','Alíquota Municipal Regular IBS','Valor Municipal Regular IBS','Valor Municipal IBS','Valor IBS','Alíquota CBS','Redução Aliquota CBS','Alíquota Efetiva CBS','Alíquota Regular CBS','Percentual Diferimento CBS','Alíquota Compra Gov CBS','Valor Regular CBS','Valor Diferimento CBS','Valor Compra Gov CBS','Valor CBS','Valor Total Reembolsos/Repasses','Valor Serviço + Repasse','Valor Multa','Valor Juros','Valor Líquido','Código de Obra','Código CEI','Data de Cadastro','Usuário de Cadastro','Origem Cadastro','Data Conferência pela Empresa','Usuário Conferência pela Empresa','Data Conferência pela Contabilidade','Usuário Conferência pela Contabilidade','Data Conferência Automática','Usuário Conferência Automática','Centro de Custo','Categoria de Pagamento','Departamento','Permite Crédito de PIS / COFINS','Link para NFSe','Observação','Código do Acumulador','Chave Nota Nacional'
        ])

        # ***************** Renomeando colunas *****************
        df_contabilidade = df_contabilidade.rename(columns={
            "Número NFe": "num_nf",
            "Prestador": "nome_prestador",
            "Cnpj/Cpf Prestador": "cpf_cnpj",
            "Valor NFe": "valor_servico"
        })

        # Criando ID
        df_contabilidade["cpf_cnpj"] = df_contabilidade["cpf_cnpj"].str.replace("/","", regex=False).str.replace(".","", regex=False).str.replace("-","", regex=False)
        df_contabilidade["id"] = df_contabilidade["num_nf"].astype(str)+ "|" + df_contabilidade["cpf_cnpj"]
        df_contabilidade = df_contabilidade.drop(columns=["num_nf", "cpf_cnpj"])

        # Criando apenas uma coluna com ID
        df_id_empresa = df_livro_empresa[["id"]]
        df_id_contabilidade = df_contabilidade[["id"]]

        df_id_unico = pd.concat([df_id_empresa, df_id_contabilidade], ignore_index=True).dropna().drop_duplicates()
        df_id_unico[["nf", "cnpj"]] = df_id_unico["id"].str.split("|", expand=True)

        # Criando o merge id_unico e df_empresa
        df_merged_id_unico_df_empresa = pd.merge(
            left=df_id_unico,
            right=df_livro_empresa,
            left_on="id",
            right_on="id",
            how='outer'
        )

        # Criando o merge e o df_contabilidade
        df_merge_final = pd.merge(
            left=df_merged_id_unico_df_empresa,
            right=df_contabilidade,
            left_on="id",
            right_on="id",
            how='outer'
        )

        df_merge_final = df_merge_final.rename(columns={
            "nome_abreviado": "nome_prestador_empresa",
            "valor_servico_x": "valor_servico_empresa",
            "nome_prestador": "nome_prestador_contabilidade",
            "valor_servico_y": "valor_servico_contabilidade"
        })

        df_merge_final["valor_servico_empresa"] = df_merge_final["valor_servico_empresa"].astype(float)
        df_merge_final["valor_servico_contabilidade"] = df_merge_final["valor_servico_contabilidade"].astype(float)

        lista_campos = ['valor_servico_empresa','valor_servico_contabilidade']
        for campo in lista_campos:
            df_merge_final[campo] = df_merge_final[campo].fillna(0)

        df_merge_final["diferenca_valor_servico"] = df_merge_final["valor_servico_empresa"] - df_merge_final["valor_servico_contabilidade"]

        nome_arquivo = f"{uuid.uuid4()}-apuracao_servico.xlsx"

        with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
            df_merge_final.to_excel(writer, sheet_name="apuraçao_servico", index=False)