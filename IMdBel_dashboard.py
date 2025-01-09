import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# Carregar dados
columns_to_load = ['tconst', 'titleType', 'primaryTitle', 'genres', 'startYear']  # Não inclui 'averageRating' aqui
general_titles_df = pd.read_csv(r'c:\Users\isabe\OneDrive\Documentos\python_work\mentoria\2° mês\Projeto IMdB\title.basics.tsv', sep='\t', usecols=columns_to_load)
ratings_df = pd.read_csv(r'c:\Users\isabe\OneDrive\Documentos\python_work\mentoria\2° mês\Projeto IMdB\title.ratings.tsv', sep='\t', usecols=['tconst', 'averageRating'])

# Separando apenas os dados que são filmes
movies_df = general_titles_df.loc[general_titles_df['titleType'] == 'movie']

# Mesclando os dados
final_movies_df = pd.merge(movies_df, ratings_df, how='left', on='tconst')

# Renomeando as colunas
final_movies_df_renamed = final_movies_df[['primaryTitle', 'averageRating', 'startYear', 'genres']].rename(columns={
    'primaryTitle': 'Título do Filme',
    'averageRating': 'Avaliação',
    'startYear': 'Ano de Lançamento',
    'genres': 'Gêneros'
})

final_movies_df_renamed['Ano de Lançamento'] = pd.to_numeric(final_movies_df_renamed['Ano de Lançamento'], errors = 'coerce').astype('Int64')

# Garantir que a coluna 'averageRating' seja numérica e lidar com erros
final_movies_df_renamed['Avaliação'] = pd.to_numeric(final_movies_df_renamed['Avaliação'], errors='coerce').fillna(0)

st.title('Dashboard de Filmes IMdB')

# Primeira parte: Top 10 Filmes Mais Bem Avaliados
st.header("Top 10 Filmes Mais Bem Avaliados de Todos os Anos")
top_10_movies_all_years = final_movies_df_renamed.nlargest(10, 'Avaliação')
st.write(top_10_movies_all_years[['Título do Filme', 'Avaliação']])

# Gráfico de Top 10 Filmes de Todos os Anos
fig1_all_years = px.bar(top_10_movies_all_years, x='Título do Filme', y='Avaliação', title='Top 10 Filmes Mais Bem Avaliados de Todos os Anos')
st.plotly_chart(fig1_all_years)

# Filtrando os melhores filmes por ano
year_selected = st.selectbox('Selecione um ano:', final_movies_df_renamed['Ano de Lançamento'].unique())

# Filtrando os filmes do ano selecionado
movies_filtered = final_movies_df_renamed[final_movies_df_renamed['Ano de Lançamento'] == year_selected]

# Selecionando os 10 filmes mais bem avaliados do ano filtrado
top_10_movies = movies_filtered.nlargest(10, 'Avaliação')

# Exibindo os 10 filmes mais bem avaliados
st.write(top_10_movies[['Título do Filme', 'Avaliação']])

# Gráfico de Top 10 Filmes
fig1 = px.bar(top_10_movies, x='Título do Filme', y='Avaliação', title=f'Top 10 Filmes Mais Bem Avaliados de {year_selected}')
st.plotly_chart(fig1)

# Segunda parte: Contagem de Filmes por Gênero
st.header("Contagem de Filmes por Gênero")
genre = st.selectbox('Selecione um Gênero:', final_movies_df_renamed['Gêneros'].unique())

# Filtro de gênero
filtered_df = final_movies_df_renamed[final_movies_df_renamed['Gêneros'].str.contains(genre, na=False)]

# Contagem de filmes por Gênero
genre_count = filtered_df['Gêneros'].value_counts().reset_index()
genre_count.columns = ['Gêneros', 'Quantidade de Filmes']

# Exibindo a Tabela com os Filmes Filtrados
st.write("Filmes do Gênero Selecionado:")
st.dataframe(final_movies_df_renamed.reset_index(drop=True))  # Exibição interativa

# Exibindo a contagem de filmes por gênero
st.write("Contagem de Filmes por Gênero:")
st.dataframe(genre_count.reset_index(drop=True), use_container_width=True)

# Gráfico de Contagem de Filmes por Gênero
fig2 = px.bar(genre_count, x='Gêneros', y='Quantidade de Filmes', title='Contagem de Filmes por Gênero', height=400)
st.plotly_chart(fig2)

# Lançamentos de Filmes por Ano
st.header("Lançamentos de Filmes por Ano")

# Permitindo que a pessoa usuária selecione o ano
start_year = st.slider('Escolha o ano inicial: ', min_value=1900, max_value=2050, value=2000)
end_year = st.slider('Escolha o ano final: ', min_value=1900, max_value=2050, value=2020)
filtered_movies_by_year_df = final_movies_df_renamed[(final_movies_df_renamed['Ano de Lançamento'] >= start_year) & (final_movies_df_renamed['Ano de Lançamento'] <= end_year)]
yearly_releases = filtered_movies_by_year_df['Ano de Lançamento'].value_counts().sort_index()

# Gráfico de Lançamentos de Filmes por Ano
plt.figure(figsize=(10, 6))
yearly_releases.plot(kind='bar', color='lightcoral')
plt.xlabel('Ano')
plt.ylabel('Número de Lançamentos')
plt.title('Lançamentos de Filmes por Ano')
plt.xticks(rotation=45)
st.pyplot(plt)
