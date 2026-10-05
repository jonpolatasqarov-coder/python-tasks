import matplotlib.pyplot as plt
import seaborn as sns


class RealEstateVisualizer:
    def __init__(self, df):
        self.df = df

    def average_price_by_district(self):
        district_prices = (
            self.df.groupby("district")["price"]
            .mean()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(10, 6))

        sns.barplot(
            x=district_prices.index,
            y=district_prices.values
        )

        plt.title("Average Property Price by District")
        plt.xlabel("District")
        plt.ylabel("Average Price")
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def property_count_by_district(self):
        plt.figure(figsize=(10, 6))

        sns.countplot(
            data=self.df,
            x="district"
        )

        plt.title("Number of Properties by District")
        plt.xlabel("District")
        plt.ylabel("Number of Properties")
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def price_vs_area(self):
        plt.figure(figsize=(10, 6))

        sns.scatterplot(
            data=self.df,
            x="area",
            y="price",
            hue="type"
        )

        plt.title("Property Price vs Area")
        plt.xlabel("Area (m²)")
        plt.ylabel("Price")

        plt.tight_layout()
        plt.show()