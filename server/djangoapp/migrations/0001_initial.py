from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='CarMake',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),('name',models.CharField(max_length=100,unique=True)),('description',models.TextField(blank=True))]),
        migrations.CreateModel(name='CarModel',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),('name',models.CharField(max_length=100)),('type',models.CharField(max_length=20,choices=[(x,x) for x in ['Sedan','SUV','Wagon','Coupe','Truck','Hatchback']])),('year',models.IntegerField(validators=[django.core.validators.MinValueValidator(2015),django.core.validators.MaxValueValidator(2023)])),('car_make',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='models',to='djangoapp.carmake'))]),
    ]
