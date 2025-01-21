import json
import os

# Ordner mit JSON-Profilen und Zielordner für Chunks
PROFILE_PATH = "Merged"
OUTPUT_PATH = "Profile_Chunks"

# Sicherstellen, dass der Ausgabeordner existiert
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# Liste aller relevanten Abschnitte
sections = [
    "auticonProjects", "studyProjects", "projects", "education",
    "professionalExperience", "studies", "training", "engagements",
    "privateProjects", "furtherProjects", "auticonTraining",
    "certificates", "certifications"
]

# Funktion zur Erstellung einzelner Chunk-Dateien
def chunk_consultant_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        profile = json.load(file)

    chunks = []
    profile_id = profile.get("autilityId", "unknown")
    profile_name = profile.get("fullName", "unknown")

    # Iteriere durch alle Abschnitte im Profil und erstelle Chunks
    for section in sections:
        if section in profile:
            for entry in profile[section]:
                chunks.append({
                    "type": section,
                    "content": f"{entry.get('startDate', 'N/A')} - {entry.get('endDate', 'N/A')} - {entry.get('description', '')}",
                    "source": profile_name
                })

    # Skills separat verarbeiten
    if "technicalSkills" in profile:
        for skill_category in profile["technicalSkills"]:
            category_name = skill_category["category"]["name"]
            skills = [skill["name"] for skill in skill_category["category"]["skills"]]
            chunks.append({
                "type": "technicalSkills",
                "category": category_name,
                "content": f"{category_name}: {', '.join(skills)}",
                "source": profile_name
            })

    # Berufliche Zusammenfassung als einzelner Chunk
    if "professionalSummary" in profile:
        chunks.append({
            "type": "professionalSummary",
            "content": profile["professionalSummary"],
            "source": profile_name
        })

    # Speichere Chunks in einer separaten JSON-Datei pro Profil im Ordner profile_chunks
    output_file = os.path.join(OUTPUT_PATH, f"profile_{profile_id}.json")
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(chunks, outfile, indent=4, ensure_ascii=False)

    print(f"Chunks für {profile_name} gespeichert unter: {output_file}")

# Verarbeitung aller Profile in JSON-Dateien
for filename in os.listdir(PROFILE_PATH):
    if filename.endswith(".json"):
        chunk_consultant_profile(os.path.join(PROFILE_PATH, filename))
