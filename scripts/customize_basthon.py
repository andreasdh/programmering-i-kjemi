"""Tilpass en nedlastet Basthon Console for Programmering i kjemi."""

from pathlib import Path
import sys


TRANSLATIONS = {
    "Ouvrir un script, charger un module ou un fichier":
        "Åpne et program eller last inn en modul eller fil",
    "Il semble que Basthon ait rencontré un problème à sa dernière utilisation. "
    "Que voulez-vous faire ?":
        "Det oppstod et problem forrige gang editoren ble brukt. Hva vil du gjøre?",
    "Il n'y a aucune sauvegarde à restaurer !":
        "Det finnes ingen lagret versjon å gjenopprette!",
    "Revenir à une version précédente du script":
        "Gå tilbake til en tidligere versjon",
    "Erreur de chargement de Basthon !!!<br>Vérifiez que votre navigateur est à jour."
    "<br>Version détectée :":
        "Kunne ikke laste Python-editoren.<br>Kontroller at nettleseren er oppdatert."
        "<br>Oppdaget versjon:",
    "Changer le thème (sombre/lumineux)": "Bytt tema (mørkt/lyst)",
    "Échanger l'éditeur et la console": "Bytt plass på editoren og konsollen",
    "Afficher l'éditeur et la console": "Vis editoren og konsollen",
    "Afficher seulement l'éditeur": "Vis bare editoren",
    "Afficher seulement la console": "Vis bare konsollen",
    "Chargement des fichiers auxiliaires...": "Laster tilleggsfiler...",
    "Chargement des modules annexes...": "Laster tilleggsmoduler...",
    "Aucune sauvegarde à restaurer": "Ingen lagret versjon å gjenopprette",
    "Copier dans le presse-papier": "Kopier til utklippstavlen",
    "Afficher la vue graphique": "Vis grafikk",
    "Afficher la console": "Vis konsollen",
    "Charger dans l'éditeur": "Last inn i editoren",
    "Choisir une sauvegarde": "Velg en lagret versjon",
    "Redémarrer le noyau": "Start Python-kjernen på nytt",
    "Télécharger le script": "Last ned programmet",
    "Partager ce document": "Del dokumentet",
    "Exécuter le script": "Kjør programmet",
    "Installer le module": "Installer modulen",
    "Chargement de Basthon...": "Laster Python-editoren...",
    "Un bac à sable pour ": "Nettbasert editor for ",
    "Partager ce code": "Del koden",
    "Propulsé par ": "Drevet av ",
    "Récupération": "Gjenoppretting",
    "Exécuter": "Kjør",
    "Annuler": "Avbryt",
    "Erreur": "Feil",
    "Module": "Modul",
}


def customize_javascript(path):
    content = path.read_text(encoding="utf-8")
    required = ("Exécuter", "Propulsé par ", "Un bac à sable pour ")
    missing = [text for text in required if text not in content]
    if missing:
        raise RuntimeError(
            "Basthon-grensesnittet har endret seg; fant ikke: " + ", ".join(missing)
        )

    for source, target in sorted(
        TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True
    ):
        content = content.replace(source, target)

    if "Exécuter" in content:
        raise RuntimeError("Den franske teksten 'Exécuter' finnes fortsatt i Basthon-fila")

    path.write_text(content, encoding="utf-8")


def customize_html(path):
    content = path.read_text(encoding="utf-8")
    content = content.replace('<html lang="fr">', '<html lang="nb">')
    content = content.replace("<title>Basthon Console</title>", "<title>Python-editor</title>")

    marker = "programmering-i-kjemi-basthon"
    if marker not in content:
        style = (
            '<style id="programmering-i-kjemi-basthon">'
            'div:has(> a > img[alt="Basthon"]) {'
            'display: none !important;'
            '}'
            '</style>'
        )
        content = content.replace("</head>", style + "</head>")

    path.write_text(content, encoding="utf-8")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Bruk: customize_basthon.py INDEX_HTML MAIN_JS")

    html_path = Path(sys.argv[1])
    javascript_path = Path(sys.argv[2])
    customize_html(html_path)
    customize_javascript(javascript_path)


if __name__ == "__main__":
    main()
