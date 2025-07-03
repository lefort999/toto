from flask import Flask, request, render_template
import os

app = Flask(__name__)

# 🔹 Fonction utilitaire
def lire_texte(nom_fichier):
    """Lit le contenu d'un fichier texte."""
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()
    except FileNotFoundError:
        return "⚠️ Information non disponible."

# 🔹 Route principale
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Traitement du formulaire d’analyse
@app.route("/analyse", methods=["POST"])
def analyse():
    msg = []
    prof = request.form.get("profession", "").lower()
    naissance = request.form.get("naissance", type=int)
    lieu = request.form.get("lieu_naissance", "").lower()

    militaire = "militaire" in request.form
    blesse = "blesse" in request.form
    officier = "officier" in request.form
    celibataire = "celibataire" in request.form
    etatcivil = "etatcivil" in request.form
    doc_keywords = request.form.getlist("documentation")

    # 🧠 Analyse des règles
    if prof == "douanier" and naissance and 1760 < naissance < 1810:
        msg.append("📂 Douanier né entre 1760–1810 : dossier aux Archives nationales (F/12, F/14).")

    if "alsace" in lieu and naissance and 1870 < naissance < 1918:
        msg.append("🇩🇪 Né en Alsace entre 1870 et 1918 : consulter ANOM ou archives allemandes.")

    if prof == "orfèvre":
        msg.append("💎 Orfèvre : consulter les registres de poinçons.")

    if militaire and officier and blesse:
        msg.append("🎖️ Militaire blessé/officier : consulter les registres militaires.")

    if celibataire and etatcivil:
        msg.append("📜 Célibataire avec acte complet : voir actes notariés et mentions marginales.")

    # 📄 Chargement des fichiers documentaires
    for mot_cle in doc_keywords:
        fichier = f"{mot_cle}.txt"
        try:
            with open(fichier, encoding="utf-8") as f:
                contenu = f.read().replace("\n", "<br>")
            msg.append(f"📄 <strong>{fichier}</strong> :<br>{contenu}")
        except FileNotFoundError:
            msg.append(f"❌ Le fichier <strong>{fichier}</strong> est introuvable.")

    if not msg:
        msg.append("🤷 Aucune règle déclenchée.")

    return render_template("index.html", message="<br><br>".join(msg))

# 🔹 Consultation directe d’une rubrique professionnelle
@app.route("/profession", methods=["POST"])
def profession():
    profession = request.form.get("lecture", "").lower()

    if profession in ["militaire", "fisc", "cadastre", "police", "notaire"]:
        contenu = lire_texte(f"{profession}.txt")
        message = f"📘 Contenu de la rubrique : {profession}\n\n{contenu}"
    else:
        message = f"❌ La rubrique « {profession} » est inconnue."

    return render_template("index.html", lecture_result=message)

# 🔹 Exécution de l’application Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)