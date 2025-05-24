from django.db import models


class Categoria(models.Model):
    id= models.CharField(max_length=10, primary_key=True)
    nombre= models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.id} {self.nombre}"

class Producto(models.Model):
    id = models.CharField(max_length=20, primary_key=True) 
    marca = models.CharField(max_length=30, null=True)
    cod_ext = models.CharField(max_length=15, null=True)
    nombre = models.CharField(max_length=100, null=True)
    precio = models.IntegerField(null=True)
    fec_modif = models.DateField(null=True)
    categoria= models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock= models.IntegerField(null=True)

    def __str__(self):
       return f"{self.id} {self.marca} {self.nombre} {self.precio}"
    
class Carrito(models.Model):
    session_key = models.CharField(max_length=50)
    fec_creacion = models.DateField(auto_now_add=True)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['carrito', 'producto'], name='unique_productos_carrito')
        ]


    
