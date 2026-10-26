import os
import json
from datetime import datetime

from storage import load_json, save_json
from logger import log


class LeadManager:
    VALID_STATUSES = {
        "new",
        "contacted",
        "qualified",
        "converted",
        "lost"
    }

    def __init__(self, filename="leads.json"):
        self.filename = filename

    def load_leads(self):
        try:
            if (
                not os.path.exists(self.filename)
                or os.path.getsize(self.filename) == 0
            ):
                return []

            leads = load_json(self.filename)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"{self.filename} contains invalid JSON."
            ) from error

        if not isinstance(leads, list):
            raise ValueError(
                f"{self.filename} must contain a JSON list."
            )

        for lead in leads:
            if not isinstance(lead, dict):
                raise ValueError(
                    "Invalid lead record in JSON file."
                )

        return leads

    def save_leads(self, leads):
        save_json(leads, self.filename)

    def find_lead(self, lead_id):
        lead_id = lead_id.strip()

        if not lead_id:
            return None

        for lead in self.load_leads():
            if str(lead.get("id", "")).strip() == lead_id:
                return lead

        return None


    def merge_leads(self, scraped_data):
        leads = self.load_leads()
        leads_by_id = {}

        for lead in leads:
            lead_id = lead.get("id")
            if lead_id:
                leads_by_id[str(lead_id)] = lead

        for item in scraped_data:
            if not isinstance(item, dict):
                continue

            lead_id = item.get("id")
            if not lead_id:
                continue

            lead_id = str(lead_id)
            existing = leads_by_id.get(lead_id)

            # SocialScraper "source" ishlatadi,
            # boshqa scraperlar "profile_url" ishlatishi mumkin.
            source = item.get("source") or item.get("profile_url")

            if existing:
                existing["name"] = item.get(
                    "name"
                ) or existing.get("name")

                if source:
                    existing["source"] = source

                for field in (
                    "headline",
                    "location",
                    "region",
                    "industry",
                    "open_to",
                    "connections"
                ):
                    if item.get(field):
                        existing[field] = item[field]

                existing.setdefault("status", "new")
                existing.setdefault(
                    "created_at",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                existing.setdefault("notes", [])

            else:
                leads_by_id[lead_id] = {
                    "id": lead_id,
                    "name": item.get("name"),
                    "source": source,
                    "headline": item.get("headline", ""),
                    "location": item.get("location", ""),
                    "status": "new",
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "notes": []
                }

                # Mavjud bo'lsa, qo'shimcha maydonlarni ham saqlaymiz.
                for field in (
                    "region",
                    "industry",
                    "open_to",
                    "connections"
                ):
                    if field in item:
                        leads_by_id[lead_id][field] = item[field]

        merged = list(leads_by_id.values())

        if merged:
            self.save_leads(merged)

        return merged


    def show_leads(self):
        leads = self.load_leads()

        if not leads:
            print("\nNo leads found.")
            return

        print("\n========== LEADS ==========")

        for index, lead in enumerate(leads, start=1):
            print(
                f"\n{index}. {lead.get('name', 'Unknown')}"
                f"\n   ID: {lead.get('id', 'N/A')}"
                f"\n   Status: {lead.get('status', 'new')}"
                f"\n   Location: {lead.get('location', 'N/A')}"
            )

        print(f"\nTotal leads: {len(leads)}")

    def update_status(self, lead_id, new_status):
        new_status = new_status.strip().lower()

        if new_status not in self.VALID_STATUSES:
            print("Invalid status.")
            print(
                "Available statuses: "
                + ", ".join(sorted(self.VALID_STATUSES))
            )
            return False

        leads = self.load_leads()

        for lead in leads:
            if str(lead.get("id", "")).strip() == lead_id:
                old_status = lead.get("status", "new")

                if old_status == new_status:
                    print(
                        f"Status is already '{new_status}'."
                    )
                    return True

                lead["status"] = new_status
                lead.setdefault("notes", []).append({
                    "type": "status_change",
                    "from": old_status,
                    "to": new_status,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                })

                self.save_leads(leads)
                print(
                    f"Status updated: {old_status} -> {new_status}"
                )
                return True

        print(f"Lead ID '{lead_id}' was not found.")
        return False

    def add_note(self, lead_id, note_text):
        note_text = note_text.strip()

        if not note_text:
            print("Note cannot be empty.")
            return False

        leads = self.load_leads()

        for lead in leads:
            if str(lead.get("id", "")).strip() == lead_id:
                lead.setdefault("notes", []).append({
                    "type": "note",
                    "text": note_text,
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                })

                self.save_leads(leads)
                print(
                    f"Note added to {lead.get('name', lead_id)}."
                )
                return True

        print(f"Lead ID '{lead_id}' was not found.")
        return False

    def show_history(self, lead_id):
        lead = self.find_lead(lead_id)

        if lead is None:
            print(f"Lead ID '{lead_id}' was not found.")
            return False

        notes = lead.get("notes", [])

        print(f"\n========== HISTORY: {lead.get('name')} ==========")

        if not notes:
            print("No history recorded for this lead.")
            return True

        for entry in notes:
            timestamp = entry.get("timestamp", "Unknown time")

            if entry.get("type") == "status_change":
                print(
                    f"[{timestamp}] Status changed: "
                    f"{entry.get('from')} -> {entry.get('to')}"
                )
            else:
                print(
                    f"[{timestamp}] "
                    f"{entry.get('text', '')}"
                )

        return True
