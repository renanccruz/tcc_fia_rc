import pandas as pd
import sweetviz as sv

# /*
# 1 - Importar os dados
# 2 - Tratar o dataset
# 3 - Coletar os dados tratados
#
# 4 - 3 arquivos contendo os dados tratados do dataset
##

def main():
    df_importacoes_por_regiao = pd.read_csv("data/tempo_medio_importacao_regiao.csv", encoding="cp1252", delimiter=";", quoting=3)
    df_quantidade_di_de = pd.read_csv("data/quantidade_di_de.csv", encoding="utf-8", delimiter=";", quoting=3)

    #Tratando o dataframe di_du
    df_quantidade_di_de['ano de desembaraço'] = df_quantidade_di_de['mês de desembaraço'].apply(lambda ano: str(ano)[0:4])
    df_quantidade_di_de['mês de desembaraço'] = df_quantidade_di_de['mês de desembaraço'].apply(lambda ano: pd.to_numeric(str(ano)[4:6]))
    df_quantidade_di_de['trimestre de desembaraço'] = df_quantidade_di_de['mês de desembaraço'].apply(lambda mes: (mes - 1) // 3 + 1 if 1 <= mes <= 12 else None)
    df_quantidade_di_de = pd.DataFrame(df_quantidade_di_de.groupby(['código ua local de despacho', 'ano de desembaraço', 'trimestre de desembaraço']).sum())
    df_quantidade_di_de = df_quantidade_di_de.reset_index()

    #Tratando o dataframe de importacoes
    df_importacoes_por_regiao['TRIMESTRE DESEMB'] = df_importacoes_por_regiao['TRIMESTRE DESEMB'].apply(lambda trimestre: str(trimestre)[4])

    #Convertendo os tipos de dados para string
    df_importacoes_por_regiao['TRIMESTRE DESEMB'] = df_importacoes_por_regiao['TRIMESTRE DESEMB'].astype(str)
    df_importacoes_por_regiao['ANO DESEMB'] = df_importacoes_por_regiao['ANO DESEMB'].astype(str)
    df_quantidade_di_de['trimestre de desembaraço'] = df_quantidade_di_de['trimestre de desembaraço'].astype(str)

    print(df_importacoes_por_regiao.head(5))
    print(df_quantidade_di_de.head(10))

    df_correlacionado = pd.merge(df_importacoes_por_regiao, df_quantidade_di_de, how='inner', left_on=['UA LOCAL DESPACHO', 'ANO DESEMB', 'TRIMESTRE DESEMB'], right_on=['código ua local de despacho', 'ano de desembaraço', 'trimestre de desembaraço'])

    df_correlacionado = df_correlacionado.reset_index()

    report = sv.analyze(df_correlacionado)
    report.show_html()

    print(df_correlacionado.loc[100])


if __name__ == "__main__":
    main()
