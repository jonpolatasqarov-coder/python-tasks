
class FilterStrategy:
    def filter(self, df):
        raise NotImplementedError(
            "Subclasses must implement filter()"
        )


class PriceFilter(FilterStrategy):
    def __init__(self, max_price):
        self.max_price = max_price

    def filter(self, df):
        return df[df["price"] <= self.max_price]


class AreaFilter(FilterStrategy):
    def __init__(self, min_area):
        self.min_area = min_area

    def filter(self, df):
        return df[df["area"] >= self.min_area]


class DistrictFilter(FilterStrategy):
    def __init__(self, district):
        self.district = district.strip()

    def filter(self, df):
        return df[
            df["district"].astype(str).str.strip().str.casefold()
            == self.district.casefold()
        ]


class RoomFilter(FilterStrategy):
    def __init__(self, rooms):
        self.rooms = rooms

    def filter(self, df):
        return df[df["rooms"] == self.rooms]


class CombinedFilter(FilterStrategy):
    def __init__(self, *strategies):
        self.strategies = strategies

    def filter(self, df):
        result = df.copy()

        for strategy in self.strategies:
            result = strategy.filter(result)

        return result
