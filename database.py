import sqlite3
from datetime import datetime
import pandas as pd
from collections import Counter

class Database:
    def __init__(self, db_name="it_skills.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Schéma "standard" (singulier)
        c.execute("""
        CREATE TABLE IF NOT EXISTS skills_survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            niveau_etude TEXT,
            langages TEXT,
            frameworks TEXT,
            experience_annees INTEGER,
            heures_semaine INTEGER,
            domaine_interet TEXT,
            systeme_exploitation TEXT,
            outils_dev TEXT,
            projet_github TEXT,
            objectif TEXT,
            date_soumission TEXT
        )
        """)

        conn.commit()
        conn.close()

    def insert_data(self, data: dict):
        """
        Accepte les clés:
        - domaine_interet OU domaines_interet
        - systeme_exploitation (standard)
        """
        try:
            domaine = data.get("domaine_interet") or data.get("domaines_interet")  # fallback
            if domaine is None:
                return False, "Champ domaine_interet manquant (bug de mapping)."

            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            c.execute("""
                INSERT INTO skills_survey (
                    nom, email, niveau_etude, langages, frameworks,
                    experience_annees, heures_semaine, domaine_interet,
                    systeme_exploitation, outils_dev, projet_github,
                    objectif, date_soumission
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("nom", ""),
                data.get("email", ""),
                data.get("niveau_etude", ""),
                data.get("langages", ""),
                data.get("frameworks", ""),
                int(data.get("experience_annees", 0)),
                int(data.get("heures_semaine", 0)),
                domaine,
                data.get("systeme_exploitation", ""),
                data.get("outils_dev", ""),
                data.get("projet_github", ""),
                data.get("objectif", ""),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            conn.commit()
            conn.close()
            return True, "Données enregistrées avec succès ✅"

        except sqlite3.IntegrityError:
            return False, "Cet email est déjà enregistré ⚠️"
        except Exception as e:
            return False, f"Erreur: {e}"

    def get_all_data(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM skills_survey", conn)
        conn.close()
        return df

    def _count_items(self, series):
        all_items = []
        for items in series.fillna(""):
            if isinstance(items, str) and items.strip():
                all_items.extend([x.strip() for x in items.split(",") if x.strip()])
        return dict(Counter(all_items).most_common(10))

    def get_statistics(self):
        df = self.get_all_data()
        if df.empty:
            return None

        # Sécuriser le nom de colonne du domaine (au cas où)
        if "domaine_interet" in df.columns:
            domaine_col = "domaine_interet"
        elif "domaines_interet" in df.columns:
            domaine_col = "domaines_interet"
        else:
            domaine_col = None

        stats = {
            "total_reponses": len(df),
            "experience_moyenne": df["experience_annees"].mean() if "experience_annees" in df.columns else 0,
            "experience_mediane": df["experience_annees"].median() if "experience_annees" in df.columns else 0,
            "heures_moyenne": df["heures_semaine"].mean() if "heures_semaine" in df.columns else 0,
            "heures_mediane": df["heures_semaine"].median() if "heures_semaine" in df.columns else 0,
            "langages_populaires": self._count_items(df["langages"]) if "langages" in df.columns else {},
            "frameworks_populaires": self._count_items(df["frameworks"]) if "frameworks" in df.columns else {},
            "niveaux_etude": df["niveau_etude"].value_counts().to_dict() if "niveau_etude" in df.columns else {},
            "os_distribution": df["systeme_exploitation"].value_counts().to_dict() if "systeme_exploitation" in df.columns else {},
            "domaines_populaires": df[domaine_col].value_counts().to_dict() if domaine_col else {}
        }
        return stats

    def clear_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM skills_survey")
        conn.commit()
        conn.close()
        return True