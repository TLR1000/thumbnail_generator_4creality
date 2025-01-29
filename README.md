# Thumbnail Generator For Creality
Post processing script.
Voeg automatisch 2 thumbnails in gcode toe door Cura.  
Getest met Ultimaker Cura 5.9 and Creality Ender 3 V3 KE.  

# Wat dit oplost:
Cura genereert geen thumbnails, en de postprocessing scripts uit de open source community genereren slechts 1 of een niet werkende thumbnail. 
Dit komt omdat er in de Creality firmware een afwijking zit voor interpretatie van thumbnails tov. de standaard die daarvoor is afgesproken. Bug of noodgedwongen feature? Anyway, dit script lost dat op.

Wanneer je dit script installeert, zal Cura automatisch grote en kleine thumbnails aan de gcode file toevoegen waardoor je model precies zo de display van de printer wordt getoond als dat het in Cura wordt getoond.
   
# Script installeren in Cura:
## 1 Download het script:
Download de scriptcode uit deze repository en sla ergens lokaal op onder de naam:  
[Ender3V3KEAutoThumbnail.py](Ender3V3KEAutoThumbnail.py)
Plaats het script in de juiste map:  

## 2 Installeer het script
Open Cura en ga naar:  
```Help```> ```Show Configuration Folder```  
Open de map scripts, deze bevindt zich meestal onder:  
```C:\Users\<JouwNaam>\AppData\Roaming\cura\<Cura-versie>\scripts``` (Windows)  
```~/.local/share/cura/<Cura-versie>/scripts``` (Linux/Mac)  
Kopieer het bestand [Ender3V3KEAutoThumbnail.py](Ender3V3KEAutoThumbnail.py) naar deze map.  

## 3 Gebruik in Cura
Om dit script te activeren als post-processing script moet je het handmatig toevoegen.

Open Cura.  
Ga naar ```Extensions``` > ```Post Processing``` > ```Modify G-code```  
Selecteer ```Ender 3 Auto Thumbnail``` uit de lijst.
Klik op ```Add Script```      
En klaar. ```Close```

Omdat het script nu geactiveerd is zie je rechtsonder in je Cura scherm iets met ```</>``` en tenminste een ```1``` erbij. Dit betekent dat een post processing script actief is.   
Het genereren van de thumbnails in de .gcode files gaat nu automatisch. 
