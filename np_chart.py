import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_np_chart():
    # 1. Ingestão de Dados
    url = "https://raw.githubusercontent.com/factorialmap/hitoshi_kume_database/refs/heads/main/data_104_np.csv"
    print(f"Baixando dados de: {url}")
    
    try:
        df = pd.read_csv(url)
        print("Dados carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return

    # 2. Cálculos Estatísticos
    # Verificando se n é constante
    if df['sub_group_size'].nunique() == 1:
        n = df['sub_group_size'].iloc[0]
        print(f"Tamanho do subgrupo constante: n = {n}")
    else:
        print("Aviso: Tamanho do subgrupo varia. Usando tamanho médio para cálculos.")
        n = df['sub_group_size'].mean()

    # Cálculos
    sum_np = df['number_of_defective_units'].sum()
    sum_n = df['sub_group_size'].sum()
    
    # p_bar (proporção média)
    p_bar = sum_np / sum_n
    
    # Linha Central (CL)
    cl = n * p_bar
    
    # Desvio Padrão (sigma)
    sigma_np = np.sqrt(n * p_bar * (1 - p_bar))
    
    # Limites de Controle
    ucl = cl + 3 * sigma_np
    lcl = max(0, cl - 3 * sigma_np)

    print(f"\nEstatísticas Calculadas:")
    print(f"Proporção média (p_bar): {p_bar:.4f}")
    print(f"Linha Central (CL): {cl:.4f}")
    print(f"Limite Superior (UCL): {ucl:.4f}")
    print(f"Limite Inferior (LCL): {lcl:.4f}")

    # 3. Visualização
    plt.figure(figsize=(14, 7))
    
    # Plotando os dados
    plt.plot(df['sub_group'], df['number_of_defective_units'], 
             marker='o', linestyle='-', color='#1f77b4', label='Defeituosos (np)')

    # Plotando as linhas de controle
    plt.axhline(ucl, color='#d62728', linestyle='--', linewidth=1.5, label=f'UCL ({ucl:.2f})')
    plt.axhline(cl, color='#2ca02c', linestyle='-', linewidth=1.5, label=f'CL ({cl:.2f})')
    plt.axhline(lcl, color='#d62728', linestyle='--', linewidth=1.5, label=f'LCL ({lcl:.2f})')

    # Destacando pontos fora de controle
    outliers = df[(df['number_of_defective_units'] > ucl) | (df['number_of_defective_units'] < lcl)]
    if not outliers.empty:
        plt.scatter(outliers['sub_group'], outliers['number_of_defective_units'], 
                    color='red', s=100, zorder=5, label='Fora de Controle')
        for _, row in outliers.iterrows():
            plt.annotate(f"{row['number_of_defective_units']}", 
                         (row['sub_group'], row['number_of_defective_units']),
                         textcoords="offset points", xytext=(0,10), ha='center', color='red', fontweight='bold')

    # Estilização do gráfico
    plt.title('Gráfico de Controle np - Número de Itens Defeituosos', fontsize=16)
    plt.xlabel('Subgrupo', fontsize=12)
    plt.ylabel('Número de Defeituosos', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Adicionando texto com estatísticas no gráfico
    stats_text = (f"n = {n}\n"
                  f"CL = {cl:.2f}\n"
                  f"UCL = {ucl:.2f}\n"
                  f"LCL = {lcl:.2f}")
    plt.text(1.02, 0.5, stats_text, transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()

    # Salvando o gráfico
    output_file = 'np_control_chart.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nGráfico gerado e salvo como: {output_file}")

if __name__ == "__main__":
    create_np_chart()
