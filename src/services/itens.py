import pandas as pd
import uuid
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from src.utils.formatacao_planilha import FormatacaoPlanilha
class ApuracaoItens:
    @staticmethod
    def executar(livro_empresa, livro_icms_contabilidade, livro_ipi_contabilidade):
        # Leitura das planilhas
        df_empresa = pd.read_excel(livro_empresa, header=1)
        df_contabilidade_icms = pd.read_excel(livro_icms_contabilidade, header=6)
        df_contabilidade_ipi = pd.read_excel(livro_ipi_contabilidade, header=6)

        # ***************** Empresa *****************
        # Renomeando as colunas
        df_empresa = df_empresa.rename(columns={
            "Número": "nf_empresa",
            "Tributado": "vl_icms_empresa",
            "Tributado.1": "vl_ipi_empresa",
            "Nat. Op.": "cfop_empresa",
            "Valor Contábil": "vl_cont_empresa",
        })

        # Remover colunas desnecessárias
        delete_columns_empresa = ["Espécie", 
                          "Série", 
                          "Emissão", 
                          "Entrada", 
                          "Cód Emitente", 
                          "UF", 
                          "Incidência",
                          "%",
                          "Base Cálc.",
                          "Isento",
                          "Outros",
                          "Incidência.1",
                          "%.1",
                          "Base Cálc..1",
                          "Observação Substituição Tributária",
                          "Isento.1",
                          "Outros.1",
                          "Observação"]
        df_empresa = df_empresa.drop(columns=delete_columns_empresa)

        # Remover linhas em braco
        df_empresa = df_empresa.dropna()

        # Formatação dos dados
        df_empresa["nf_empresa"] = df_empresa["nf_empresa"].astype("int")
        df_empresa["cfop_empresa"] = df_empresa["cfop_empresa"].astype("int")

        # Criando ID unico
        df_empresa["id_unico_empresa"] = df_empresa["nf_empresa"].astype("str") + "|" + df_empresa["cfop_empresa"].astype('str')

        # Somando os valores cujo os ID's unicos sejam iguais
        df_empresa = df_empresa.groupby("id_unico_empresa", as_index=False).sum(numeric_only=True)

        # Preenchendo valores em branco com 0
        df_empresa = df_empresa.fillna(0)

        # Gerando os totais dos dados da empresa
        qtde_nf_empresa = (df_empresa["nf_empresa"]).dropna().drop_duplicates().count()
        valor_contabil_total_empresa = df_empresa['vl_cont_empresa'].sum()
        valor_icms_total_empresa = df_empresa['vl_icms_empresa'].sum()
        valor_ipi_total_empresa = df_empresa['vl_ipi_empresa'].sum()

        # ***************** Contabilidade ICMS *****************
        df_contabilidade_icms = df_contabilidade_icms.rename(columns={
            "Número": "nf_icms_contabilidade",
            "Natureza": "cfop_icms_contabilidade",
            "Valor ICMS": "vl_icms_contabilidade",
            "Vlr Contábil": "vl_cont_icms_contabilidade"
        })

        # Remover colunas desnecessárias
        df_contabilidade_icms = df_contabilidade_icms.drop(columns=['Nr Lcto', 
                                          'Pessoa', 
                                          'Data Lcto', 
                                          'Esp', 
                                          'Série',
                                          'Base ICMS', 
                                          'Isentas ICMS', 
                                          'Outras ICMS'])
        
        # Remover linhas em branco
        df_contabilidade_icms = df_contabilidade_icms.dropna()

        # Limpeza dos dados onde apareça a palavra 'Natureza'
        df_contabilidade_icms = df_contabilidade_icms[df_contabilidade_icms['cfop_icms_contabilidade'] != 'Natureza']

        # Formatação dos dados
        colunas_icms_float = ['vl_icms_contabilidade', 'vl_cont_icms_contabilidade']
        colunas_icms_int = ['cfop_icms_contabilidade','nf_icms_contabilidade']
        for col in colunas_icms_int:
            df_contabilidade_icms[col] = df_contabilidade_icms[col].astype('int')

        for col in colunas_icms_float:
            df_contabilidade_icms[col] = df_contabilidade_icms[col].astype('float')

        # Separando apenas os CFOP's menores ou iguais a 4000
        filtro = df_contabilidade_icms.query('cfop_icms_contabilidade <= 4000')
        df_contabilidade_icms = filtro

        # Criando a coluna ID unico
        df_contabilidade_icms['id_unico_ICMS'] = df_contabilidade_icms['nf_icms_contabilidade'].astype('str') + "|" + df_contabilidade_icms['cfop_icms_contabilidade'].astype('str')

        # Gerando os totais dos dados da contabilidade icms
        qtde_nf_icms_contabilidade = (df_contabilidade_icms['nf_icms_contabilidade']).dropna().drop_duplicates().count()
        valor_contabil_total_icms_contabilidade = df_contabilidade_icms['vl_cont_icms_contabilidade'].sum()
        valor_icms_total_contabilidade = df_contabilidade_icms['vl_icms_contabilidade'].sum()
        valor_icms_total_contabilidade

        # ***************** Contabilidade IPI *****************
        # Renomeando as colunas
        df_contabilidade_ipi = df_contabilidade_ipi.rename(columns={
            "Número": "nf_ipi_contabilidade",
            "Natureza": "cfop_ipi_contabilidade",
            "Valor IPI": "vl_ipi_contabilidade",
            "Vlr Contabil": "vl_cont_ipi_contabilidade"
        })

        # Removendo as colunas desnecessárias
        df_contabilidade_ipi = df_contabilidade_ipi.drop(columns=['Nr Lcto', 
                                        'Fornecedor', 
                                        'Data Lcto', 
                                        'Esp', 
                                        'Série',
                                        'Base IPI', 
                                        'Isentas IPI', 
                                        'Outras IPI'])

        # Removendo linhas em branco
        df_contabilidade_ipi = df_contabilidade_ipi.dropna()

        # Limpeza dos dados onde apareça a palavra 'Natureza'
        df_contabilidade_ipi = df_contabilidade_ipi[df_contabilidade_ipi['cfop_ipi_contabilidade'] != 'Natureza']

        # Formatação dos dados
        colunas_ipi_float = ['vl_ipi_contabilidade', 'vl_cont_ipi_contabilidade']
        colunas_ipi_int = ['cfop_ipi_contabilidade', 'nf_ipi_contabilidade']
        for col in colunas_ipi_int:
            df_contabilidade_ipi[col] = df_contabilidade_ipi[col].astype('int')

        for col in colunas_ipi_float:
            df_contabilidade_ipi[col] = df_contabilidade_ipi[col].astype('float')

        # Separando apenas os CFOP's menores ou iguais a 4000
        filtro = df_contabilidade_ipi.query('cfop_ipi_contabilidade <= 4000')
        df_contabilidade_ipi = filtro
        df_contabilidade_ipi['id_unico_IPI'] = df_contabilidade_ipi['nf_ipi_contabilidade'].astype('str') + "|" + df_contabilidade_ipi['cfop_ipi_contabilidade'].astype('str')

        # Gerando os totais dos dados da contabilidade ipi
        valor_ipi_total_contabilidade = df_contabilidade_ipi['vl_ipi_contabilidade'].sum()

        # Criando o dataframe com a lista mestre com todas as NF's dos 3 dataframes
        lista_mestre = pd.concat([
            df_empresa['id_unico_empresa'],
            df_contabilidade_icms['id_unico_ICMS'],
            df_contabilidade_ipi['id_unico_IPI']
        ]).dropna().drop_duplicates()

        df_mestre = pd.DataFrame({'id_unico': lista_mestre})
        df_mestre = df_mestre.fillna(0)
        df_mestre[['nf', 'cfop']] = df_mestre['id_unico'].str.split('|', expand=True)

        # Unindo as bases
        df_mestre_e_empresa = pd.merge(
        df_mestre,          
        df_empresa,       
        left_on='id_unico', 
        right_on='id_unico_empresa',
        how='outer')

        # (Base Mestre + Base empresa) + Base ICMS contabilidade
        df_mestre_e_empresa_e_contabilidade_icms = pd.merge(
        df_mestre_e_empresa,
        df_contabilidade_icms,
        left_on='id_unico',
        right_on='id_unico_ICMS',
        how='outer')

        # (Base Mestre + Base empresa + Base ICMS contabilidade + Base IPI contabilidade)
        df_unido = pd.merge(
        df_mestre_e_empresa_e_contabilidade_icms,
        df_contabilidade_ipi,
        left_on='id_unico',
        right_on='id_unico_IPI',
        how='outer')

        df_unido['cfop'] = pd.to_numeric(df_unido['cfop'], errors='coerce').astype('Int64')
        df_unido['nf'] = pd.to_numeric(df_unido['nf'], errors='coerce').astype('Int64')
        df_unido['nf_icms_contabilidade'] = pd.to_numeric(df_unido['nf_icms_contabilidade'], errors='coerce').astype('Int64')
        df_unido['cfop_icms_contabilidade'] = pd.to_numeric(df_unido['cfop_icms_contabilidade'], errors='coerce').astype('Int64')

        df_unido = df_unido.fillna(0)
        df_unido['dif_vl_contabil'] = (df_unido['vl_cont_empresa'] - df_unido['vl_cont_icms_contabilidade']).round(2)
        df_unido['dif_vl_icms'] = (df_unido['vl_icms_empresa'] - df_unido['vl_icms_contabilidade']).round(2)
        df_unido['dif_vl_ipi'] = (df_unido['vl_ipi_empresa'] - df_unido['vl_ipi_contabilidade']).round(2)

        cols_dif = ['dif_vl_contabil', 'dif_vl_icms', 'dif_vl_ipi','dif_vl_ipi']
        df_unido['status'] = 'Valor Divergente'
        df_unido.loc[df_unido[cols_dif].eq(0).all(axis=1), 'status'] = 'OK'
        df_unido = df_unido.sort_values(by=['nf', 'cfop'])

        cols_desejadas = ['nf','cfop','vl_cont_empresa','vl_icms_empresa','vl_ipi_empresa', 'vl_cont_icms_contabilidade', 'vl_icms_contabilidade', 'vl_ipi_contabilidade', 'dif_vl_contabil', 'dif_vl_icms', 'dif_vl_ipi','status']
        cols_existentes = [col for col in cols_desejadas if col in df_unido.columns]
        df_export_excel = df_unido[cols_existentes]

        # Resumo
        df_resumo = pd.DataFrame({
            'Qtde Nfs Empresa': [qtde_nf_empresa],
            'Qtde Nfs Contabilidade': [qtde_nf_icms_contabilidade],
            'Diferença qtde Nfs': [qtde_nf_empresa - qtde_nf_icms_contabilidade],
            
            'Valor Total Contabil Empresa': [valor_contabil_total_empresa],
            'Valor Total Contabil Contabilidade': [valor_contabil_total_icms_contabilidade],
            'Diferença valor total Contabil': [valor_contabil_total_empresa - valor_contabil_total_icms_contabilidade],
            
            'Valor Total ICMS Empresa': [valor_icms_total_empresa],
            'Valor Total ICMS Contabilidade': [valor_icms_total_contabilidade],
            'Diferença Valor total ICMS': [valor_icms_total_empresa - valor_icms_total_contabilidade],
            
            'Valor Total IPI Empresa': [valor_ipi_total_empresa],
            'Valor Total IPI Contabilidade': [valor_ipi_total_contabilidade],
            'Diferença Valor total IPI': [valor_ipi_total_empresa - valor_ipi_total_contabilidade]
        })
        nome_arquivo = f"{uuid.uuid4()}-apuracao_itens.xlsx"

        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            df_export_excel.to_excel(writer, sheet_name='apuracao', index=False)
            df_resumo.to_excel(writer, sheet_name='resumo', index=False)

        FormatacaoPlanilha.formatar(nome_arquivo)