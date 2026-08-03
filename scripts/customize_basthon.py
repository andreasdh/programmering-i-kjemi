"""Customize a downloaded Basthon Console for Programming in Chemistry."""

from pathlib import Path
import sys


TRANSLATIONS = {
    "Ouvrir un script, charger un module ou un fichier":
        "Open a script or load a module or file",
    "Il semble que Basthon ait rencontré un problème à sa dernière utilisation. "
    "Que voulez-vous faire ?":
        "The editor encountered a problem the last time it was used. What would you like to do?",
    "Il n'y a aucune sauvegarde à restaurer !":
        "There is no saved version to restore!",
    "Revenir à une version précédente du script":
        "Return to a previous version of the script",
    "Erreur de chargement de Basthon !!!<br>Vérifiez que votre navigateur est à jour."
    "<br>Version détectée :":
        "Could not load the Python editor.<br>Make sure your browser is up to date."
        "<br>Detected version:",
    "Changer le thème (sombre/lumineux)": "Switch theme (dark/light)",
    "Échanger l'éditeur et la console": "Swap the editor and console",
    "Afficher l'éditeur et la console": "Show the editor and console",
    "Afficher seulement l'éditeur": "Show only the editor",
    "Afficher seulement la console": "Show only the console",
    "Chargement des fichiers auxiliaires...": "Loading auxiliary files...",
    "Chargement des modules annexes...": "Loading additional modules...",
    "Aucune sauvegarde à restaurer": "No saved version to restore",
    "Copier dans le presse-papier": "Copy to clipboard",
    "Afficher la vue graphique": "Show graphical view",
    "Afficher la console": "Show console",
    "Charger dans l'éditeur": "Load into the editor",
    "Choisir une sauvegarde": "Choose a saved version",
    "Redémarrer le noyau": "Restart the Python kernel",
    "Télécharger le script": "Download the script",
    "Partager ce document": "Share this document",
    "Exécuter le script": "Run the script",
    "Installer le module": "Install the module",
    "Chargement de Basthon...": "Loading the Python editor...",
    "Un bac à sable pour ": "Online editor for ",
    "Partager ce code": "Share this code",
    "Propulsé par ": "Powered by ",
    "Récupération": "Recovery",
    "Exécuter": "Run",
    "Annuler": "Cancel",
    "Erreur": "Error",
}


def customize_javascript(path):
    content = path.read_text(encoding="utf-8")
    required = ("Exécuter", "Propulsé par ", "Un bac à sable pour ")
    missing = [text for text in required if text not in content]
    if missing:
        raise RuntimeError(
            "The Basthon interface has changed; could not find: " + ", ".join(missing)
        )

    for source, target in sorted(
        TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True
    ):
        source_literal = '"' + source.replace('"', '\\"') + '"'
        target_literal = '"' + target.replace('"', '\\"') + '"'
        content = content.replace(source_literal, target_literal)

    if "Exécuter" in content:
        raise RuntimeError("The French text 'Exécuter' is still present in the Basthon file")

    path.write_text(content, encoding="utf-8")


def customize_html(path):
    content = path.read_text(encoding="utf-8")
    content = content.replace('<html lang="fr">', '<html lang="en">')
    content = content.replace("<title>Basthon Console</title>", "<title>Python editor</title>")

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
        raise SystemExit("Usage: customize_basthon.py INDEX_HTML MAIN_JS")

    html_path = Path(sys.argv[1])
    javascript_path = Path(sys.argv[2])
    customize_html(html_path)
    customize_javascript(javascript_path)


if __name__ == "__main__":
    main()
