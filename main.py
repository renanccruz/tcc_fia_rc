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
    #Tratando o dataframe de importacoes
    df_importacoes_por_regiao['TRIMESTRE DESEMB'] = df_importacoes_por_regiao['TRIMESTRE DESEMB'].apply(lambda trimestre: str(trimestre)[4])


    print(df_importacoes_por_regiao.head(5))
    print(df_quantidade_di_de.head(10))

    report = sv.analyze(df_quantidade_di_de)
    report = sv.analyze(df_importacoes_por_regiao)
    report.show_html()


if __name__ == "__main__":
    main()
