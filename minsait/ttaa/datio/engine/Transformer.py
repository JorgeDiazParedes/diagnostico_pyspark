import pyspark.sql.functions as f
from pyspark.sql import SparkSession, WindowSpec, Window, DataFrame, Column

from minsait.ttaa.datio.common.Constants import *
from minsait.ttaa.datio.common.naming.PlayerInput import *
from minsait.ttaa.datio.common.naming.PlayerOutput import *
from minsait.ttaa.datio.utils.Writer import Writer


class Transformer(Writer):
    def __init__(self, spark: SparkSession):
        self.spark: SparkSession = spark
        df: DataFrame = self.read_input()
        df.printSchema()
        df = self.clean_data(df)

        if AGE_PARAMS == 1:
            df = df.filter(age.column() < 23)

        df = self.column_selection(df)
        df = self.add_player_cat(df)
        df = self.add_potential_vs_overall(df)
        df = self.filter_column(df)

        # for show 100 records after your transformations and show the DataFrame schema
        df.show(n=100, truncate=False)
        df.printSchema()

        # Uncomment when you want write your final output
        self.write(df)

    def read_input(self) -> DataFrame:
        """
        :return: a DataFrame readed from csv file
        """
        return self.spark.read \
            .option(INFER_SCHEMA, True) \
            .option(HEADER, True) \
            .csv(INPUT_PATH)

    def clean_data(self, df: DataFrame) -> DataFrame:
        """
        :param df: is a DataFrame with players information
        :return: a DataFrame with filter transformation applied
        column team_position != null && column short_name != null && column overall != null
        """
        df = df.filter(
            (short_name.column().isNotNull()) &
            (short_name.column().isNotNull()) &
            (overall.column().isNotNull()) &
            (team_position.column().isNotNull())
        )
        return df

    def column_selection(self, df: DataFrame) -> DataFrame:
        """
        :param df: is a DataFrame with players information
        :return: a DataFrame with just 5 columns...
        """
        df = df.select(
            short_name.column(),
            long_name.column(),
            age.column(),
            height_cm.column(),
            weight_kg.column(),
            nationality.column(),
            club_name.column(),
            overall.column(),
            potential.column(),
            team_position.column()
        )
        return df

    def add_player_cat(self, df: DataFrame) -> DataFrame:
        """
        :param df: is a DataFrame with players information (must have team_position and height_cm columns)
        :return: add to the DataFrame the column "player_cat"
             by each position value
             cat A si el jugador es de los mejores 3 jugadores en su posición de su país
             cat B si el jugador es de los mejores 5 jugadores en su posición de su país
             cat C si el jugador es de los mejores 10 jugadores en su posición de su país
             cat D for the rest
        """
        w: WindowSpec = Window \
            .partitionBy(nationality.column(), team_position.column())\
            .orderBy(overall.column().desc())

        rank: Column = f.rank().over(w)

        rule: Column = f.when(rank < 3, A) \
            .when(rank < 5, B) \
            .when(rank < 10, C) \
            .otherwise(D)

        df = df.withColumn(player_cat.name, rule)

        return df

    def add_potential_vs_overall(self, df: DataFrame) -> DataFrame:
        """
        :param df: is a DataFrame with players information (must have team_position and height_cm columns)
        :return: add to the DataFrame the column "potential_vs_overall "
             by Columna potential dividida por la columna overall
        """

        df = df.withColumn(potential_vs_overall.name, potential.column() / overall.column())

        return df

    def filter_column(self, df: DataFrame) -> DataFrame:
        """
        :param df: is a DataFrame with players information (must have team_position and height_cm columns)
        :return: filter to the DataFrame the column
             by Si player_cat esta en los siguientes valores: A, B
             Si player_cat es C y potential_vs_overall es superior a 1.15
             Si player_cat es D y potential_vs_overall es superior a 1.25
        """

        l = [A, B]

        df = df.filter((player_cat.column().isin(l)) \
                        | ((player_cat.column() == C) & (potential_vs_overall.column() > 1.15)) \
                        | ((player_cat.column() == D) & (potential_vs_overall.column() > 1.25)))

        return df

