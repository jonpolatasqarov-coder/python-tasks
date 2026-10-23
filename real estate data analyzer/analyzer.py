import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from apartment import Apartment
from house import House


class RealEstateAnalyzer:
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.properties = self.create_properties()


    def create_properties(self):
        properties = []

        for _, row in self.df.iterrows():
            property_type = str(row["type"]).strip()

            if property_type == "Apartment":
                property_class = Apartment
            elif property_type == "House":
                property_class = House
            else:
                raise ValueError(
                    f"Unknown property type: {property_type}"
                )

            property_obj = property_class(
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

    def export_to_excel(self, data, filename):
        if data.empty:
            print("No properties found. Nothing to export.")
            return

        if not filename.lower().endswith(".xlsx"):
            filename += ".xlsx"

        data.to_excel(filename, index=False)
        print(f"Exported successfully to {filename}")


    def price_predictor(self, area, rooms, district, property_type):
        if area <= 0:
            raise ValueError("Area must be greater than zero.")

        if rooms <= 0:
            raise ValueError("Rooms must be greater than zero.")

        district = district.strip()

        available_districts = self.df["district"].astype(str).str.strip()

        matched_districts = available_districts[
            available_districts.str.casefold() == district.casefold()
        ]

        if matched_districts.empty:
            available = sorted(available_districts.unique())
            raise ValueError(
                f"Unknown district. Available districts: {available}"
            )

        district = matched_districts.iloc[0]

        if property_type not in self.df["type"].unique():
            raise ValueError("Unknown property type in the dataset.")

        features = ["area", "rooms", "district", "type"]
        data = self.df[features + ["price"]].dropna()

        X = data[features]
        y = data["price"]

        if len(data) < 10:
            raise ValueError("Not enough data to train the model.")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("categories", OneHotEncoder(handle_unknown="ignore"),
                 ["district", "type"])
            ],
            remainder="passthrough"
        )

        model = make_pipeline(
            preprocessor,
            LinearRegression()
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        input_data = pd.DataFrame([{
            "area": area,
            "rooms": rooms,
            "district": district,
            "type": property_type
        }])

        predicted_price = max(0, model.predict(input_data)[0])

        return predicted_price, mae, r2


    def property_price_analysis(self):
        results = []

        for property_obj in self.properties:
            results.append({
                "id": property_obj.property_id,
                "type": type(property_obj).__name__,
                "district": property_obj.district,
                "area": property_obj.area,
                "rooms": property_obj.rooms,
                "price": property_obj.price,
                "status": property_obj.status,
                "price_per_m2": property_obj.calculate_price_per_m2()
            })

        return pd.DataFrame(results)
