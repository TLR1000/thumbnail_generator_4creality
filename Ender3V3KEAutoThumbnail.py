import base64
from cura.Snapshot import Snapshot
from PyQt6.QtCore import QBuffer
from ..Script import Script

class Ender3V3KEAutoThumbnail(Script):
    def __init__(self):
        super().__init__()
    
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
        Genereert en injecteert meerdere thumbnails (96x96 en 300x300) in de G-code,
        aangepast voor Creality Ender-3 compatibiliteit.
        """
        resolutions = [(96, 96), (300, 300)]
        thumbnails = []
        
        for width, height in resolutions:
            encoded_snapshot, thumbnail_size = self.generate_thumbnail(width, height)
            base64_lines = [encoded_snapshot[i:i+76] for i in range(0, len(encoded_snapshot), 76)]
            
            # Creality Ender-3 compatibele thumbnail headers
            thumbnail_section = [
                f"; png begin {width} * {height} {thumbnail_size} 0 95 160\n"
            ] + [f"; {line}\n" for line in base64_lines] + [
                "; png end\n"
            ]
            
            thumbnails.extend(thumbnail_section)
        
        # Injecteer thumbnails aan het begin van de G-code
        if len(data) > 0:
            data[0] = "\n".join(thumbnails) + "\n" + data[0]
        
        return data
