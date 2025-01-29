# Ender3V3KEAutoThumbnail - Cura Post-Processing Script
# MIT License
#
# Copyright (c) 2025 Jeroen Oostrijck
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

import base64
from cura.Snapshot import Snapshot
from PyQt6.QtCore import QBuffer
from ..Script import Script

class Ender3V3KEAutoThumbnail(Script):
    def __init__(self):
        super().__init__()
    
    def getSettingDataString(self):
        """
        Retourneert een minimale instellingenstructuur om compatibiliteit met Cura te behouden.
        """
        return """{
            "version": 2,
            "name": "Ender-3 Auto Thumbnail",
            "key": "Ender3V3KEAutoThumbnail",
            "metadata": {
                "author": "User",
                "type": "postprocess"
            },
            "settings": {}
        }"""
    
    def generate_thumbnail(self, width, height):
        """
        Genereert een PNG-snapshot van het huidige model en zet deze om in base64.
        """
        snapshot = Snapshot.snapshot(width, height)
        if not snapshot:
            raise ValueError("Kon geen snapshot genereren.")
        
        thumbnail_buffer = QBuffer()
        thumbnail_buffer.open(QBuffer.OpenModeFlag.ReadWrite)
        snapshot.save(thumbnail_buffer, "PNG")
        thumbnail_data = thumbnail_buffer.data()
        base64_bytes = base64.b64encode(thumbnail_data)
        base64_message = base64_bytes.decode('ascii')
        thumbnail_buffer.close()
        
        return base64_message, len(thumbnail_data)

    def execute(self, data):
        """
        Genereert en injecteert vaste thumbnails (96x96 en 300x300) in de G-code,
        aangepast voor Creality Ender-3 compatibiliteit.
        """
        resolutions = [(96, 96), (300, 300)]
        thumbnails = []
        
        for width, height in resolutions:
            encoded_snapshot, thumbnail_size = self.generate_thumbnail(width, height)
            base64_lines = [encoded_snapshot[i:i+76] for i in range(0, len(encoded_snapshot), 76)]
            
            # Creality Ender-3 compatibele thumbnail headers (zonder spaties en juiste afsluiting)
            thumbnail_section = [
                f"; png begin {width}*{height} {thumbnail_size} 0 95 192\n"
            ] + [f"; {line}\n" for line in base64_lines] + [
                "; png end\n"
            ]
            
            thumbnails.extend(thumbnail_section)
        
        # Injecteer thumbnails aan het begin van de G-code
        if len(data) > 0:
            data[0] = "\n".join(thumbnails) + "\n" + data[0]
        
        return data
