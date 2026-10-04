class LeadGenerator:

    @staticmethod
    def generate(data):
        leads = []

        for item in data:
            lead = {
                "name": item["title"],
                "source": item["url"],
                "interest": "product",
                "status": "new"
            }

            if "author" in item:
                lead["interest"] = "news"

            leads.append(lead)

        return leads

