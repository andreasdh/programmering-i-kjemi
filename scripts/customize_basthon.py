"""Customize a downloaded or restored Basthon Console for Programming in Chemistry."""

from hashlib import sha256
from pathlib import Path
import re
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


STORAGE_SCRIPT_ID = "programmering-i-kjemi-basthon-storage"
STORAGE_SCRIPT = f'''<script id="{STORAGE_SCRIPT_ID}">
(() => {{
  "use strict";

  const source = new URLSearchParams(window.location.search).get("from");
  if (!source) return;

  const prefix = `programmering-i-kjemi:basthon:${{encodeURIComponent(source)}}:`;
  const prototype = Storage.prototype;
  const nativeGetItem = prototype.getItem;
  const nativeSetItem = prototype.setItem;
  const nativeRemoveItem = prototype.removeItem;
  const nativeClear = prototype.clear;
  const nativeKey = prototype.key;
  const local = window.localStorage;
  const session = window.sessionStorage;

  const isScopedStore = (store) => store === local || store === session;
  const scopedKey = (key) => prefix + String(key);

  prototype.getItem = function (key) {{
    return nativeGetItem.call(this, isScopedStore(this) ? scopedKey(key) : key);
  }};

  prototype.setItem = function (key, value) {{
    return nativeSetItem.call(
      this,
      isScopedStore(this) ? scopedKey(key) : key,
      value,
    );
  }};

  prototype.removeItem = function (key) {{
    return nativeRemoveItem.call(this, isScopedStore(this) ? scopedKey(key) : key);
  }};

  prototype.clear = function () {{
    if (!isScopedStore(this)) return nativeClear.call(this);

    const keys = [];
    for (let index = 0; index < this.length; index += 1) {{
      const key = nativeKey.call(this, index);
      if (key && key.startsWith(prefix)) keys.push(key);
    }}
    keys.forEach((key) => nativeRemoveItem.call(this, key));
  }};
}})();
</script>'''


FOCUS_SCRIPT_ID = "programmering-i-kjemi-basthon-focus"
FOCUS_SCRIPT = f'''<script id="{FOCUS_SCRIPT_ID}">
(() => {{
  "use strict";

  const source = new URLSearchParams(window.location.search).get("from");
  if (!source) return;

  let guardStartupFocus = true;
  const nativeFocus = HTMLElement.prototype.focus;

  HTMLElement.prototype.focus = function (options) {{
    if (!guardStartupFocus) {{
      return nativeFocus.call(this, options);
    }}

    const guardedOptions =
      options && typeof options === "object"
        ? {{ ...options, preventScroll: true }}
        : {{ preventScroll: true }};
    return nativeFocus.call(this, guardedOptions);
  }};

  const releaseGuard = () => {{
    guardStartupFocus = false;
    window.removeEventListener("pointerdown", releaseGuard, true);
    window.removeEventListener("touchstart", releaseGuard, true);
    window.removeEventListener("keydown", releaseGuard, true);
  }};

  window.addEventListener("pointerdown", releaseGuard, true);
  window.addEventListener("touchstart", releaseGuard, true);
  window.addEventListener("keydown", releaseGuard, true);
}})();
</script>'''


def customize_javascript(path):
    content = path.read_text(encoding="utf-8")
    required = ("Exécuter", "Propulsé par ", "Un bac à sable pour ")
    missing = [
        text for text in required
        if text not in content and TRANSLATIONS[text] not in content
    ]
    if missing:
        raise RuntimeError(
            "The Basthon interface has changed; could not find: " + ", ".join(missing)
        )

    # Basthon stores an explicit user choice in browser storage. This only changes
    # the initial value for users who have not selected a theme themselves.
    dark_default = 'theme:"dark",viewMode:"default",rightPanel:"terminal"'
    light_default = 'theme:"light",viewMode:"default",rightPanel:"terminal"'
    dark_count = content.count(dark_default)
    light_count = content.count(light_default)
    if dark_count == 1 and light_count == 0:
        content = content.replace(dark_default, light_default, 1)
    elif not (dark_count == 0 and light_count == 1):
        raise RuntimeError(
            "The Basthon interface has changed; could not set a unique light-theme default"
        )

    # A stored dark preference from the previous deployment would otherwise
    # override the new default. Force light during initialization; users can still
    # switch theme for the remainder of the open session.
    stored_state_init = 'case"init":return null!=i&&(e=se(i)),e.ready=!0,e;'
    forced_light_init = (
        'case"init":return null!=i&&(e=se(i)),e.theme="light",e.ready=!0,e;'
    )
    stored_count = content.count(stored_state_init)
    forced_count = content.count(forced_light_init)
    if stored_count == 1 and forced_count == 0:
        content = content.replace(stored_state_init, forced_light_init, 1)
    elif not (stored_count == 0 and forced_count == 1):
        raise RuntimeError(
            "The Basthon interface has changed; could not force light theme on startup"
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


def replace_or_insert_script(content, script_id, script):
    pattern = re.compile(rf'<script id="{script_id}">.*?</script>', re.DOTALL)
    if pattern.search(content):
        return pattern.sub(script, content, count=1)
    return content.replace("</head>", script + "</head>")


def customize_html(path, javascript_path):
    content = path.read_text(encoding="utf-8")
    content = content.replace('<html lang="fr">', '<html lang="en">')
    content = content.replace("<title>Basthon Console</title>", "<title>Python editor</title>")

    # The upstream filename stays unchanged even though this script modifies its
    # contents. Add a content hash so browsers do not reuse the previous bundle.
    cache_key = sha256(javascript_path.read_bytes()).hexdigest()[:12]
    script_pattern = re.compile(
        r'(<script\b[^>]*\bsrc="assets/main\.[^"?]+\.js)(?:\?[^"]*)?(")'
    )
    content, replacements = script_pattern.subn(
        lambda match: f"{match.group(1)}?custom={cache_key}{match.group(2)}",
        content,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError(
            "The Basthon interface has changed; could not update the script cache key"
        )

    style_marker = "programmering-i-kjemi-basthon"
    if style_marker not in content:
        style = (
            '<style id="programmering-i-kjemi-basthon">'
            'div:has(> a > img[alt="Basthon"]) {'
            'display: none !important;'
            '}'
            '</style>'
        )
        content = content.replace("</head>", style + "</head>")

    # Basthon saves editor state in browser storage. Several same-origin iframes on
    # one chapter would otherwise share that state. Namespace all storage operations
    # by the file in the `from` query parameter before the deferred app bundle runs.
    content = replace_or_insert_script(content, STORAGE_SCRIPT_ID, STORAGE_SCRIPT)

    # Basthon may focus its editor during startup. A focused control inside a lazy
    # iframe can make the parent document scroll to that iframe. Prevent scrolling
    # for programmatic startup focus, then restore normal focus behavior as soon as
    # the user interacts with the embedded editor.
    content = replace_or_insert_script(content, FOCUS_SCRIPT_ID, FOCUS_SCRIPT)

    path.write_text(content, encoding="utf-8")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: customize_basthon.py INDEX_HTML MAIN_JS")

    html_path = Path(sys.argv[1])
    javascript_path = Path(sys.argv[2])
    customize_javascript(javascript_path)
    customize_html(html_path, javascript_path)


if __name__ == "__main__":
    main()
