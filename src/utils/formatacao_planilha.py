from openpyxl import load_workbook
from openpyxl.styles import PatternFill

class FormatacaoPlanilha:
    def formatar(nome_arquivo):
        # 2. Abre o arquivo salvo com o openpyxl para aplicar as cores de fundo
        wb = load_workbook(nome_arquivo)
        ws = wb.active

        # Define as cores de preenchimento (Verde Claro e Vermelho Claro em formato Hexadecimal)
        fill_verde = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid") # Verde claro (suave)
        fill_vermelho = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid") # Vermelho claro (suave)

        # Descobre qual é o número da coluna 'Classificacao'
        coluna_classificacao_idx = None
        for col_idx, cell in enumerate(ws[1], 1):
            if cell.value == 'status':
                coluna_classificacao_idx = col_idx
                break

        # Se encontrou a coluna, percorre as linhas da tabela aplicando a cor correspondente
        if coluna_classificacao_idx:
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=coluna_classificacao_idx)
                if cell.value == 'OK':
                    cell.fill = fill_verde
                elif cell.value == 'Valor Divergente':
                    cell.fill = fill_vermelho

        # Salva o arquivo final com as cores aplicadas
        wb.save(nome_arquivo)