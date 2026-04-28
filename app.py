import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from database import Database

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="IT Skills Tracker",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def init_db():
    return Database()

db = init_db()

# =========================================================
# CSS (BLEU/BLANC + TEXTE NOIR)
# =========================================================
def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

        :root{
            --blue-900:#0B3D91;
            --blue-700:#1565C0;
            --blue-600:#1E88E5;
            --blue-100:#E3F2FD;
            --bg:#F7FBFF;
            --card:#FFFFFF;
            --text:#0F172A;
            --muted:#475569;
            --border:#D6E6F7;
            --shadow: 0 12px 30px rgba(2, 32, 71, 0.10);
        }

        html, body, [class*="css"] { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
        .stApp { background: linear-gradient(180deg, var(--bg) 0%, #FFFFFF 70%); color: var(--text); }

        /* Container */
        .block-container { padding-top: 1.6rem !important; max-width: 1350px; }

        /* Sidebar (clair) */
        [data-testid="stSidebar"]{
            background: linear-gradient(180deg, var(--blue-100) 0%, #FFFFFF 100%);
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] * { color: var(--text) !important; }

        /* Hide Streamlit branding */
        #MainMenu { visibility: hidden; }
        
        footer { visibility: hidden; }

        /* Hero */
        .hero{
            background: linear-gradient(135deg, #FFFFFF 0%, var(--blue-100) 55%, #FFFFFF 100%);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 2.2rem 2rem;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }
        .hero:before{
            content:"";
            position:absolute; inset:-80px;
            background: radial-gradient(circle at 20% 20%, rgba(30,136,229,.25), transparent 45%),
                        radial-gradient(circle at 80% 20%, rgba(21,101,192,.18), transparent 45%),
                        radial-gradient(circle at 50% 90%, rgba(11,61,145,.12), transparent 55%);
        }
        .hero-inner{ position:relative; z-index:2; text-align:center; }
        .hero-title{
            font-size: 2.7rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            color: var(--blue-900);
        }
        .hero-sub{
            margin-top: .6rem;
            font-size: 1.05rem;
            color: var(--muted);
            font-weight: 400;
        }
        .badge{
            display:inline-block;
            margin-top: 1.1rem;
            padding: .45rem 1.1rem;
            border-radius: 999px;
            border: 1px solid rgba(30,136,229,.25);
            background: rgba(30,136,229,.10);
            color: var(--blue-900);
            font-weight: 700;
            font-size: .85rem;
            letter-spacing: .06em;
        }

        /* Section header */
        .sec{
            margin: 1.6rem 0 1rem 0;
        }
        .sec h2{
            margin:0;
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--blue-900);
        }
        .sec p{
            margin:.35rem 0 0 0;
            color: var(--muted);
        }
        .divider{
            height:4px; width:70px; border-radius:999px;
            background: linear-gradient(90deg, var(--blue-600), var(--blue-900));
            margin-top:.7rem;
        }

        /* Cards */
        .card{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.2rem 1.2rem;
            box-shadow: 0 10px 24px rgba(2, 32, 71, 0.07);
        }

        /* Metric cards */
        .metric{
            background: linear-gradient(180deg, #FFFFFF 0%, #F4FAFF 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.15rem 1rem;
            box-shadow: 0 10px 22px rgba(2, 32, 71, 0.08);
            transition: transform .2s ease, box-shadow .2s ease;
            height: 100%;
        }
        .metric:hover{
            transform: translateY(-4px);
            box-shadow: 0 16px 32px rgba(2, 32, 71, 0.12);
        }
        .metric .top{
            display:flex; align-items:center; justify-content:space-between;
            gap:.75rem;
        }
        .metric .icon{
            width:42px; height:42px; border-radius:12px;
            display:flex; align-items:center; justify-content:center;
            background: rgba(30,136,229,.12);
            border: 1px solid rgba(30,136,229,.18);
            font-size: 1.3rem;
        }
        .metric .label{
            margin-top:.6rem;
            color: var(--muted);
            font-size:.82rem;
            letter-spacing: .08em;
            text-transform: uppercase;
            font-weight: 700;
        }
        .metric .value{
            margin-top:.25rem;
            font-size: 1.9rem;
            font-weight: 800;
            color: var(--text);
        }
        .metric .delta{
            margin-top:.45rem;
            font-size:.85rem;
            color: var(--blue-900);
            background: rgba(30,136,229,.10);
            border: 1px solid rgba(30,136,229,.18);
            padding: .25rem .6rem;
            border-radius: 999px;
            display:inline-block;
        }

        /* Inputs readability */
        label, .stMarkdown, .stTextInput label, .stSelectbox label,
        .stTextArea label, .stNumberInput label, .stMultiSelect label, .stSlider label {
            color: var(--text) !important;
            font-weight: 700 !important;
        }

        /* Text inputs */
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            background: #FFFFFF !important;
            color: var(--text) !important;
            border: 1.5px solid var(--border) !important;
            border-radius: 12px !important;
            padding: .75rem .9rem !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
            border-color: rgba(30,136,229,.65) !important;
            box-shadow: 0 0 0 4px rgba(30,136,229,.15) !important;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #94A3B8 !important;
        }

        /* Select/MultiSelect containers */
        .stSelectbox [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div {
            background: #FFFFFF !important;
            border: 1.5px solid var(--border) !important;
            border-radius: 12px !important;
        }
        .stSelectbox span, .stMultiSelect span { color: var(--text) !important; }

        /* Tags */
        .stMultiSelect [data-baseweb="tag"]{
            background: rgba(30,136,229,.12) !important;
            border: 1px solid rgba(30,136,229,.22) !important;
            color: var(--blue-900) !important;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, var(--blue-600), var(--blue-900)) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 999px !important;
            padding: .85rem 1.2rem !important;
            font-weight: 800 !important;
            letter-spacing: .06em !important;
            text-transform: uppercase !important;
            box-shadow: 0 12px 28px rgba(21,101,192,.25) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 16px 34px rgba(21,101,192,.30) !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"]{
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: .4rem;
            gap: .4rem;
            box-shadow: 0 10px 22px rgba(2, 32, 71, 0.06);
        }
        .stTabs [data-baseweb="tab"]{
            border-radius: 12px;
            padding: .7rem 1rem;
            color: var(--muted);
            font-weight: 800;
        }
        .stTabs [aria-selected="true"]{
            background: rgba(30,136,229,.12) !important;
            color: var(--blue-900) !important;
        }

        /* Dataframe */
        .stDataFrame {
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 22px rgba(2, 32, 71, 0.06);
        }

        /* Footer */
        .foot{
            margin-top: 2.2rem;
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.6rem;
            text-align: center;
            color: var(--muted);
            box-shadow: 0 10px 22px rgba(2, 32, 71, 0.06);
        }
        .foot .t{
            font-weight: 900;
            color: var(--blue-900);
            font-size: 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

load_css()

# =========================================================
# UI HELPERS
# =========================================================
def hero(title: str, subtitle: str, badge: str):
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-inner">
            <div class="hero-title">{title}</div>
            <div class="hero-sub">{subtitle}</div>
            <div class="badge">{badge}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def section(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="sec">
          <h2>{title}</h2>
          <p>{subtitle}</p>
          <div class="divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def metric(label: str, value: str, icon: str, delta: str | None = None):
    delta_html = f'<div class="delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric">
          <div class="top"><div class="icon">{icon}</div></div>
          <div class="label">{label}</div>
          <div class="value">{value}</div>
          {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def validate_email(email: str) -> bool:
    if not email or not email.strip():
        return False
    e = email.strip()
    return ("@" in e) and ("." in e.split("@")[-1]) and (len(e) >= 6)

def validate_github(url: str) -> bool:
    if not url or not url.strip():
        return True
    return "github.com" in url.strip().lower()

# =========================================================
# PLOTLY THEME (bleu/blanc)
# =========================================================
def plotly_common_layout(fig, title: str):
    fig.update_layout(
        template="plotly_white",
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center"),
        font=dict(color="#0F172A", family="Inter"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=430,
        margin=dict(t=70, b=60, l=50, r=30),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(2, 32, 71, 0.08)")
    return fig

def chart_bar(data_dict: dict, title: str):
    if not data_dict:
        return None
    s = pd.Series(data_dict).sort_values(ascending=False).head(10)
    fig = px.bar(
        s.reset_index(),
        x="index",
        y=0,
        labels={"index": "", "0": "Nombre"},
        color=0,
        color_continuous_scale=["#BBDEFB", "#1E88E5", "#0B3D91"],
    )
    fig.update_traces(text=s.values, textposition="outside", cliponaxis=False)
    fig = plotly_common_layout(fig, title)
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(tickangle=-30)
    return fig

def chart_donut(data_dict: dict, title: str):
    if not data_dict:
        return None
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(line=dict(color="white", width=2)),
                textinfo="label+percent",
            )
        ]
    )
    fig = plotly_common_layout(fig, title)
    fig.update_layout(showlegend=True, legend=dict(font=dict(size=11)))
    return fig

def chart_hist(df: pd.DataFrame, col: str, title: str, x_label: str):
    if df.empty or col not in df.columns:
        return None
    fig = px.histogram(df, x=col, nbins=15, color_discrete_sequence=["#1E88E5"])
    fig = plotly_common_layout(fig, title)
    fig.update_xaxes(title=x_label)
    fig.update_yaxes(title="Fréquence")
    return fig

# =========================================================
# PAGES
# =========================================================
def page_collecte():
    hero("💻 IT Skills Tracker", "Collecte & analyse descriptive des compétences en informatique", "FRENCH VERSION ")

    stats = db.get_statistics()
    if stats:
        exp_med = stats.get("experience_mediane")
        hrs_med = stats.get("heures_mediane")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric("Participants", str(stats.get("total_reponses", 0)), "👥")
        with col2:
            metric("Expérience moyenne", f"{stats.get('experience_moyenne', 0):.1f} ans", "⭐",
                   delta=(f"Médiane: {exp_med:.0f} ans" if exp_med is not None else None))
        with col3:
            metric("Heures / semaine", f"{stats.get('heures_moyenne', 0):.0f}h", "⏱️",
                   delta=(f"Médiane: {hrs_med:.0f}h" if hrs_med is not None else None))
        with col4:
            metric("Langages distincts", str(len(stats.get("langages_populaires", {}) or {})), "💻")

    st.markdown(
        """
        <div class="card" style="margin-top:1.2rem;">
          <b>Objectif :</b> collecter des données sur les profils IT (langages, frameworks, domaines, environnement)
          puis afficher des statistiques descriptives et des visualisations.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("skills_form", clear_on_submit=True):
        section("🧑‍💼 Informations personnelles", "Identité et niveau d’études (champs lisibles : texte noir).")

        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom complet *", placeholder="Ex: Jean Dupont")
            email = st.text_input("Email *", placeholder="ex: jean.dupont@email.com")
        with c2:
            niveau_etude = st.selectbox(
                "Niveau d'études *",
                ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat", "Professionnel"],
            )
            experience = st.number_input("Années d'expérience en programmation *", min_value=0, max_value=50, value=1)

        section("💻 Compétences techniques", "Langages, frameworks et domaine principal.")

        c3, c4 = st.columns(2)
        with c3:
            langages = st.multiselect(
                "Langages de programmation *",
                ["Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "PHP", "Go", "Rust", "Kotlin", "Swift", "R", "SQL"],
            )
            frameworks = st.multiselect(
                "Frameworks / Bibliothèques",
                ["Django", "Flask", "FastAPI", "React", "Vue.js", "Angular", "Node.js", "Spring", "Laravel",
                 "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"],
            )
        with c4:
            domaine = st.selectbox(
                "Domaine d'intérêt principal *",
                ["Développement Web", "Data Science", "Intelligence Artificielle", "Cybersécurité",
                 "Développement Mobile", "DevOps", "Cloud Computing", "IoT", "Blockchain", "Autre"],
            )
            heures_semaine = st.slider("Heures de codage par semaine", min_value=0, max_value=80, value=10)

        section("🛠️ Environnement de travail", "OS, outils et lien GitHub (optionnel).")

        c5, c6 = st.columns(2)
        with c5:
            os_choice = st.selectbox(
                "Système d'exploitation *",
                ["Windows", "macOS", "Linux (Ubuntu)", "Linux (Autre)", "Autre"],
            )
            outils = st.multiselect(
                "Outils de développement",
                ["VS Code", "PyCharm", "IntelliJ IDEA", "Git", "GitHub", "GitLab", "Docker", "Postman", "Kubernetes"],
            )
        with c6:
            github = st.text_input("Lien GitHub (optionnel)", placeholder="https://github.com/username")
            objectif = st.text_area("Objectif professionnel (optionnel)", placeholder="Ex: devenir Data Scientist...", max_chars=500)

        submitted = st.form_submit_button("🚀 Soumettre", use_container_width=True, type="primary")

    if submitted:
        errors = []
        if not nom or len(nom.strip()) < 3:
            errors.append("Le nom doit contenir au moins 3 caractères.")
        if not email or not validate_email(email):
            errors.append("Email invalide (ex: user@domain.com).")
        if not langages:
            errors.append("Sélectionnez au moins un langage.")
        if github and github.strip() and not validate_github(github):
            errors.append("Lien GitHub invalide (doit contenir github.com).")

        if errors:
            for e in errors:
                st.error("❌ " + e)
            return

        payload = {
            "nom": nom.strip(),
            "email": email.strip().lower(),
            "niveau_etude": niveau_etude,
            "langages": ", ".join(langages),
            "frameworks": ", ".join(frameworks) if frameworks else "",
            "experience_annees": int(experience),
            "heures_semaine": int(heures_semaine),
            "domaine_interet": domaine,
            "systeme_exploitation": os_choice,
            "outils_dev": ", ".join(outils) if outils else "",
            "projet_github": github.strip() if github else "",
            "objectif": objectif.strip() if objectif else "",
        }

        ok, msg = db.insert_data(payload)
        if ok:
            st.success("✅ " + msg)
            st.info("Astuce : allez dans **Analyse des Données** pour voir les graphiques mis à jour.")
        else:
            st.error("⚠️ " + msg)


def page_analyse():
    hero("📊 Analyse des Données", "Tableaux, statistiques descriptives et visualisations", "DASHBOARD BLEU & BLANC")

    stats = db.get_statistics()
    df = db.get_all_data()

    if stats is None or df is None or len(df) == 0:
        st.warning("Aucune donnée disponible. Remplissez d’abord le formulaire dans **Collecte de Données**.")
        return

    exp_med = stats.get("experience_mediane")
    hrs_med = stats.get("heures_mediane")

    section("📈 Vue d’ensemble", "Indicateurs principaux calculés automatiquement.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric("Total réponses", str(stats.get("total_reponses", 0)), "📌")
    with col2:
        metric("Expérience moy.", f"{stats.get('experience_moyenne', 0):.1f} ans", "⭐",
               delta=(f"Médiane: {exp_med:.0f} ans" if exp_med is not None else None))
    with col3:
        metric("Heures moy.", f"{stats.get('heures_moyenne', 0):.0f}h", "⏱️",
               delta=(f"Médiane: {hrs_med:.0f}h" if hrs_med is not None else None))
    with col4:
        metric("Langages (Top)", str(len(stats.get("langages_populaires", {}) or {})), "💻")

    tabs = st.tabs(["🔤 Langages & Frameworks", "🎯 Domaines", "💻 OS & Temps", "📚 Niveaux", "📋 Données & Export"])

    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            fig = chart_bar(stats.get("langages_populaires", {}), "Top 10 Langages")
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c2:
            fig = chart_bar(stats.get("frameworks_populaires", {}), "Top 10 Frameworks")
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[1]:
        fig = chart_donut(stats.get("domaines_populaires", {}), "Répartition des domaines")
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[2]:
        c1, c2 = st.columns(2)
        with c1:
            fig = chart_donut(stats.get("os_distribution", {}), "Systèmes d’exploitation")
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c2:
            fig = chart_hist(df, "heures_semaine", "Distribution des heures de codage", "Heures / semaine")
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[3]:
        c1, c2 = st.columns(2)
        with c1:
            fig = chart_bar(stats.get("niveaux_etude", {}), "Niveaux d’études")
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c2:
            fig = chart_hist(df, "experience_annees", "Distribution de l’expérience", "Années d’expérience")
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[4]:
        section("🔎 Filtres", "Affichez une partie des données avant export.")
        c1, c2, c3 = st.columns(3)
        with c1:
            domaine_filter = st.multiselect("Domaine", options=sorted(df["domaine_interet"].dropna().unique()))
        with c2:
            niveau_filter = st.multiselect("Niveau d'études", options=sorted(df["niveau_etude"].dropna().unique()))
        with c3:
            os_filter = st.multiselect("OS", options=sorted(df["systeme_exploitation"].dropna().unique()))

        filtered = df.copy()
        if domaine_filter:
            filtered = filtered[filtered["domaine_interet"].isin(domaine_filter)]
        if niveau_filter:
            filtered = filtered[filtered["niveau_etude"].isin(niveau_filter)]
        if os_filter:
            filtered = filtered[filtered["systeme_exploitation"].isin(os_filter)]

        st.dataframe(filtered, use_container_width=True, height=420)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Télécharger CSV",
            data=csv,
            file_name=f"it_skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="foot">
          <div class="t">IT Skills Tracker</div>
          <div>Design bleu & blanc • Texte noir • Streamlit + Plotly + SQLite</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MAIN
# =========================================================
def main():
    with st.sidebar:
        st.markdown("<div class='card'><b>Navigation</b><br/>Choisissez une page.</div>", unsafe_allow_html=True)

        stats = db.get_statistics()
        total = stats.get("total_reponses") if stats else 0
        st.markdown(f"<div class='card'><b>Participants enregistrés :</b> {total}</div>", unsafe_allow_html=True)
        page = st.radio(
              "Navigation",  # label NON vide
              ["📝 Collecte de Données", "📊 Analyse des Données"],
              label_visibility="collapsed"
)
        st.markdown(
            """
            <div class="card">
              <b>Fonctionnalités</b><br/>
              • Collecte (formulaire)<br/>
              • Stockage SQLite<br/>
              • Statistiques descriptives<br/>
              • Graphiques interactifs<br/>
              • Export CSV
            </div>
            """,
            unsafe_allow_html=True,
        )

    if page == "📝 Collecte de Données":
        page_collecte()
    else:
        page_analyse()

if __name__ == "__main__":
    main()
