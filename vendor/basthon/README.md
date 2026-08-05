# Local Basthon backup

This directory stores a compressed backup of the customized Basthon Console used by the website.

The website build prepares Basthon in this order:

1. the last successfully published copy from the `gh-pages` branch;
2. `basthon-console-custom.tgz` from this directory;
3. a fresh download from the official Basthon server.

The Python examples are not stored inside the backup. They remain normal source files in `docs/_static/basthon_examples/` and are copied into Basthon during every build.

The backup is generated deterministically by `scripts/prepare_basthon.sh`, and its SHA-256 checksum is stored alongside it. Basthon is free software distributed under the GNU General Public License. The upstream project is maintained at https://forge.apps.education.fr/basthon/.
