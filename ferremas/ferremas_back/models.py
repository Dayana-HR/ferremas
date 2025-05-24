from django.db import models


class Categoria(models.Model):
    id= models.CharField(max_length=10, primary_key=True)
    nombre= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} {self.nombre}"

class Producto(models.Model):
    id = models.CharField(max_length=20, primary_key=True) 
    marca = models.CharField(max_length=30)
    cod_ext = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField
    fec_modif = models.DateField
    categoria= models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock= models.IntegerField

    def __str__(self):
       return f"{self.id} {self.marca} {self.nombre} {self.precio}"



    
