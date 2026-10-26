
from datetime import datetime


class LeadGenerator:

    @staticmethod
    def generate(data, existing_leads=None):
        if existing_leads is None:
            existing_leads = []

        existing_by_id = {
            lead["id"]: lead
            for lead in existing_leads
            if lead.get("id")
        }

        leads = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in data:
            lead_id = item.get("id")

            if not lead_id:
                continue

            existing = existing_by_id.get(lead_id)

            if existing:
                lead = existing.copy()

                lead["name"] = item.get("name")
                lead["source"] = item.get("profile_url")
                lead["headline"] = item.get("headline")
                lead["location"] = item.get("location")

            else:
                lead = {
                    "id": lead_id,
                    "name": item.get("name"),
                    "source": item.get("profile_url"),
                    "headline": item.get("headline"),
                    "location": item.get("location"),
                    "status": "new",
                    "created_at": now,
                    "notes": []
                }

            leads.append(lead)

        return leads
