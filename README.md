# thumbnail_generator_4creality
Voeg automatisch 2 thumbnails in gcode toe door Cura.
Getest met Cura 5.9 and Creality Ender 3 V3 KE.
 
# Script installeren in Cura:
## 1 Download het script:
Kopieer de aangepaste scriptcode en sla het op als een Python-bestand met de naam:
Ender3V3KEAutoThumbnail.py
Plaats het script in de juiste map:

## 2 Installeer het script
Open Cura en ga naar:
Help > Show Configuration Folder
Open de map scripts, deze bevindt zich meestal onder:
C:\Users\<JouwNaam>\AppData\Roaming\cura\<Cura-versie>\scripts (Windows)
~/.local/share/cura/<Cura-versie>/scripts (Linux/Mac)
Kopieer het bestand CreateEnder3V3KEThumbnail.py naar deze map.

## 3 Configureer Cura
Cura voert standaard geen post-processing scripts automatisch uit. Om dit te activeren, moeten we een printerconfiguratie aanpassen.

Ga naar de printerinstellingen:

Open Cura.
Ga naar Preferences > Configure Cura > Printers.
Selecteer je Creality Ender 3 V3 KE printer.
Klik op Machine Settings.
Automatische post-processing toevoegen:

Zoek de sectie "Post-processing scripts".
Voeg het volgende script toe als standaardwaarde:
```
"post_process_script": {
    "Ender3V3KEAutoThumbnail"
}
```
Sla de wijzigingen op en sluit het venster.
