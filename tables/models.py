import uuid
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'https://o2city-serve.vercel.app/qrcode?table={self.table_number}')
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        self.qr_code.save(f'{self.table_number}_qr.png', File(buffer), save=False)
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return (f'table {self.table_number}')
        
