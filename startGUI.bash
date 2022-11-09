#!/user/bin/env_bash
echo Starte Update track_generator
pip install track_generator -U
echo Update beendet

echo Starte GUI
python3 build_road_gui.py
echo GUI beendet