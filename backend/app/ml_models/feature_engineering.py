
"""
Feature Engineering Utilities
"""

import pandas as pd
import numpy as np


class FeatureEngineer:

    @staticmethod
    def create_time_features(df):

        df['timestamp'] = pd.to_datetime(df['timestamp'])

        df['hour'] = df['timestamp'].dt.hour

        df['minute'] = df['timestamp'].dt.minute

        df['day_of_week'] = df['timestamp'].dt.dayofweek

        return df

    @staticmethod
    def create_lag_features(
        df,
        column,
        lags=[1, 2, 3]
    ):

        for lag in lags:

            df[f'{column}_lag_{lag}'] = (
                df[column].shift(lag)
            )

        return df

    @staticmethod
    def create_rolling_features(
        df,
        column,
        windows=[5, 10]
    ):

        for window in windows:

            df[f'{column}_mean_{window}'] = (
                df[column]
                .rolling(window)
                .mean()
            )

            df[f'{column}_std_{window}'] = (
                df[column]
                .rolling(window)
                .std()
            )

        return df

    @staticmethod
    def create_trend_feature(df, column):

        df[f'{column}_trend'] = (
            df[column].diff()
        )

        return df

    @staticmethod
    def preprocess_metrics(df):

        df = FeatureEngineer.create_time_features(df)

        metrics = [
            'cpu_usage',
            'memory_usage',
            'disk_usage'
        ]

        for metric in metrics:

            if metric in df.columns:

                df = FeatureEngineer.create_lag_features(
                    df,
                    metric
                )

                df = (
                    FeatureEngineer
                    .create_rolling_features(
                        df,
                        metric
                    )
                )

                df = FeatureEngineer.create_trend_feature(
                    df,
                    metric
                )

        df = df.dropna()

        return df
