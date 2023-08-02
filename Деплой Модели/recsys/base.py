from typing import List, Set, Optional, Any

import pandas as pd
import numpy as np
from .utils import parse

class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        # self.distance = pd.read_csv(distance_filepath, index_col='movie_id')
        self.distance = pd.read_csv(distance_filepath, index_col=0)
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title'].values

    def get_ratings(self) -> List[str]:
        return self.movies['vote_average'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist()
                  for item in sublist]
        return set(genres)

    def recommendation(self, title: str, top_k: int = 5, movies: Optional[pd.DataFrame] = None) -> List[str]:

        if title not in self.movies['title'].values:
            raise ValueError(f"Нет такого '{title}'.")
        if movies is None:
            movies = self.movies

        movie_id = self.movies.index[self.movies['title']== title].item()  # это id фильма

        movie_ids = movies['movie_id'].astype(int) # все id отфильтрованных фильмов в списке
        
        print(f"movie_ids {movie_ids} movie_ids {movie_ids.shape}\n")
        valid_columns = list(movie_ids)

        distMatrix = self.distance.copy()

        valid_columns = [col for col in movie_ids if col in distMatrix.columns]
        distMatrixFiltred = distMatrix.loc[:, valid_columns]
        print(f"distMatrixFiltred {distMatrixFiltred} distMatrixFiltred {distMatrixFiltred.shape}\n")

        distancesRow = distMatrixFiltred.loc[movie_id].values #  строка по выбранному фильму
        ############
        row = distMatrixFiltred.loc[movie_id]
        similarity_scores = [(column, value) for column, value in row.items()]

        # print(f"similarity_scores {similarity_scores}")

        similarity_scores = sorted(similarity_scores, key=lambda x: x[1],
                                    reverse=True) # Сортировка в убывающем порядке
        topIndexs = [score[0] for score in similarity_scores[1:top_k+1]] # индексы похожих фильмов
        print(f"topIndexs {topIndexs}")
        topMovies = movies.loc[topIndexs, 'title'].values.tolist()
       
        return topMovies

    def filter_movies(self, genres: Optional[str] = None, rating: Optional[float] = None) -> pd.DataFrame:
        filtered_movies = self.movies.copy()
        if genres:
            filtered_movies["genresstr"] = filtered_movies["genres"].apply(
                lambda x: f'"{x}"')

            filtered_movies["OneTwo"] = filtered_movies["genresstr"].apply(
                lambda x: 1 if genres in x else 0)
            filtered_movies = filtered_movies[filtered_movies["OneTwo"] == 1]

        if rating is not None:
            filtered_movies = filtered_movies[filtered_movies['vote_average'] >= rating] 

        return filtered_movies
    
      