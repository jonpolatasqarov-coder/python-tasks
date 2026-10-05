import pandas as pd
from sklearn.linear_model import LinearRegression

from apartment import Apartment
from house import House


class RealEstateAnalyzer:
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.properties = self.create_properties()

    def create_properties(self):
        properties = []

        for _, row in self.df.iterrows():
            if row["type"] == "Apartment":
                property_obj = Apartment(
                    row["id"],
                    row["district"],
                    row["area"],
                    row["rooms"],
                    row["price"],
                    row["status"]
                )
            else:
                property_obj = House(
                    row["id"],
                    row["district"],
                    row["area"],
                    row["rooms"],
                    row["price"],
                    row["status"]
                )

            properties.append(property_obj)

        return properties

    def average_price(self):
        return self.df["price"].mean()

    def highest_price(self):
        return self.df["price"].max()

    def sold_count(self):
        return (self.df["status"] == "sold").sum()

    def most_expensive_district(self):
        district_prices = self.df.groupby("district")["price"].mean()
        return district_prices.idxmax()

    def apply_filter(self, strategy):
        return strategy.filter(self.df)

    def export_to_excel(self, df, filename):
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"

        df.to_excel(filename, index=False)

    def price_predictor(self, area, rooms):
        X = self.df[["area", "rooms"]]
        y = self.df["price"]

        model = LinearRegression()
        model.fit(X, y)

        input_data = pd.DataFrame(
            [[area, rooms]],
            columns=["area", "rooms"]
        )

        predicted_price = model.predict(input_data)

        return predicted_price[0]