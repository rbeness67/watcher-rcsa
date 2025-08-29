#!/usr/bin/env bash
set -o errexit  # Stop on error

# Répertoire persistant sur Render (autorisé en écriture)
STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "⬇️ Téléchargement de Chrome (cache inexistant)"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src  # Retour dans le dossier source
else
  echo "✅ Chrome trouvé en cache, utilisation..."
fi

# Installer dépendances Python
pip install -r requirements.txt

