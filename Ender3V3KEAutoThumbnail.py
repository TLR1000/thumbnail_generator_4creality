# Automatically include thumbnails in G-code 
# Tested with Cura 5.9 and Creality Ender 3 V3 KE
# Based on:
# https://github.com/Ultimaker/Cura/blob/master/plugins/PostProcessingPlugin/scripts/CreateThumbnail.py

import base64
from UM.Logger import Logger
from cura.Snapshot import Snapshot
from PyQt6.QtCore import QBuffer
from ..Script import Script


class Ender3V3KEAutoThumbnail(Script):
    def __init__(self):
        super().__init__()

    def _createSnapshot(self, width, height):
        Logger.log("d", f"Creating thumbnail image ({width}x{height})...")
        try:
            return Snapshot.snapshot(width, height)
        except Exception:
            Logger.logException("w", f"Failed to create snapshot image ({width}x{height})")

    def _encodeSnapshot(self, snapshot):
        Logger.log("d", "Encoding thumbnail image...")
        try:
            thumbnail_buffer = QBuffer()
            thumbnail_buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            snapshot.save(thumbnail_buffer, "PNG")
            thumbnail_data = thumbnail_buffer.data()
            base64_bytes = base64.b64encode(thumbnail_data)
            base64_message = base64_bytes.decode('ascii')
            thumbnail_buffer.close()
            Logger.log("d", f"Snapshot encoded, length={len(thumbnail_data)}")
            return base64_message, len(thumbnail_data)
        except Exception:
            Logger.logException("w", "Failed to encode snapshot image")

    def _convertSnapshotToGcode(self, thumbnail_length, encoded_snapshot, width, height, chunk_size=76):
        Logger.log("d", f"Converting {width}x{height} snapshot into G-code...")
        gcode = []

        header = f"; THUMBNAIL_BEGIN {width}x{height} {thumbnail_length}"
        Logger.log("d", f"Gcode header={header}")
        gcode.append(header)

        chunks = ["; " + encoded_snapshot[i:i + chunk_size]
                  for i in range(0, len(encoded_snapshot), chunk_size)]
        gcode.extend(chunks)

        gcode.append("; THUMBNAIL_END")
        gcode.append(";")

        return gcode

    def execute(self, data):
        Logger.log("d", "Ender3V3KEAutoThumbnail Plugin start")

        # Automatisch 96x96 en 300x300 thumbnails genereren
        for width, height in [(96, 96), (300, 300)]:
            snapshot = self._createSnapshot(width, height)
            if snapshot:
                Logger.log("d", f"Snapshot {width}x{height} created")
                encoded_snapshot, thumbnail_length = self._encodeSnapshot(snapshot)
                snapshot_gcode = self._convertSnapshotToGcode(thumbnail_length, encoded_snapshot, width, height)

                if len(data) > 0:
                    # Thumbnails toevoegen aan het begin van de G-code
                    data[0] = "\n".join(snapshot_gcode) + "\n" + data[0]
                    Logger.log("d", f"Added {width}x{height} snapshot G-code")

        Logger.log("d", "Ender3V3KEAutoThumbnail Plugin end")
        return data
