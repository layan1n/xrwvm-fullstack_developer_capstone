from .models import CarMake, CarModel

def initiate():
    for make,model,kind,year in [('Toyota','Camry','Sedan',2023),('Honda','Civic','Sedan',2022),('Ford','Escape','SUV',2023),('Hyundai','Tucson','SUV',2022),('BMW','X3','SUV',2021)]:
        brand,_=CarMake.objects.get_or_create(name=make,defaults={'description':make+' vehicles'})
        CarModel.objects.get_or_create(car_make=brand,name=model,year=year,defaults={'type':kind})
