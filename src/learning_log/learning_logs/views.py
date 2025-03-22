from django.shortcuts import render
from .models import Topic,Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """Página principal do learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''Mostra todos os assuntos'''
    topics = Topic.objects.order_by('date_added') #pegando do mais antigo para o mais recente
    context = {
        'topics': topics
        }

    return render(request, 'learning_logs/topics.html', context)

@login_required
#decorators servem para alterar o comportamento de uma funcao sem precisar alterar seu codigo fonte
def topic(request, topic_id):
    '''Apresenta um unico assunto com todas as suas entradas'''

    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added') #pegando do mais recente para mais antigo
    context = {
        'topic': topic,
        'entries': entries
        }

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''Adiciona um novo assunto'''
    if request.method != 'POST':
        #Aqui criamos um form em branco, pois nenhum dado está sendo passado
        form = TopicForm()
    else:
        #Aqui estamos recebendo dados por post
        form = TopicForm(request.POST)
        #Precisamos validar nosso formulario
        if form.is_valid():
            #se for valido ele salva os dados no db, automaticamente porque
            #o form tem ligacao direta com o model e o mode com o banco de dados
            form.save()
            #redirecionando para a pagina de topicos
            #o reverse utiliza o name da URL no lugar do caminho completo e isso
            #é bom porque o dominio pode mudar e nao precisamos austar no codigo
            return HttpResponseRedirect(reverse('topics'))
        
    context = {
        'form': form
        }
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Adiciona uma nova anotacao'''
    topic = Topic.objects.get(id = topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            #adicionando o topic ao entry
            new_entry = form.save(commit=False) #cria um registro temporario, nao salva no bd
            new_entry.topic = topic #adicionando o topic como propriedade do objeto
            new_entry.save()

            #aqui estou redirecionando para a pagina topic e passando o parametro do id do topic, assim conseguimos listar as entries
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
        
    context = {
        'form': form,
        'topic': topic
        }
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''Edita uma anotacao existente'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        #aqui nao precisamos criar outro form porque ja existe um form para a entry
        form = EntryForm(instance=entry) #para que o formulario apareca com pre preenchimento, utilizamos o instace
    else:
        #Estou pegando a instancia que foi encontrada e atualizando ela com os dados que vieram via POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
        }
    
    return render(request, 'learning_logs/edit_entry.html', context)