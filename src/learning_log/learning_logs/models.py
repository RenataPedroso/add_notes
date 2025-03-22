from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """Assunto sobre qual o usuario esta aprendendo"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Devolve uma representacao em string do modelo"""
        return self.text
    
class Entry(models.Model):
    """Uma anotacao especifica sobre determinado topico"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # esse models.CASCADE diz que quando a categoria for excluida, todos os registros dessas cateogria seram excluidos tbm
    #O parametro on_delete se refere a o que deve acontecer com esse objeto caso sua foreignKey seja excluida
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries" #esse parametro diz como o django deve chamar essa classe no plural por padrao ele so adiciona um s no final

    def __str__(self):
        return self.text[:50] + '...' #estamos dizendo que queremos retornar apenas 50 primeiros caracteres
    

