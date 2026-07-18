from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
        ('products', '0002_product_image_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured_image_alt',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='post',
            name='image_credit',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='image_source_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='related_categories',
            field=models.ManyToManyField(blank=True, related_name='related_posts', to='products.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='related_products',
            field=models.ManyToManyField(blank=True, related_name='related_posts', to='products.product'),
        ),
    ]
