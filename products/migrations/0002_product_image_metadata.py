from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_alt',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='product',
            name='image_credit',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='image_source_url',
            field=models.URLField(blank=True),
        ),
    ]
