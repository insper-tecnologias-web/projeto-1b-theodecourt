from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag_name = request.POST.get('tag')

        tag, created = Tag.objects.get_or_create(name=tag_name)
        # TAREFA: Utilize o title e content para criar um novo Note no banco de dados
        new_note = Note(title=title, content=content, tag=tag)
        new_note.save()
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})
    
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    #note = Note.objects.get(id=note_id) #possivel tanto a opcao assima quanto essa
    note.delete()
    return redirect('index')  # Redirecionar para a página de lista de notas após a exclusão

def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        note.title = title
        note.content = content
        note.save()
        return redirect('index')  # Redirecionar para a página inicial após a edição
    
    return render(request, 'notes/edit.html', {'note': note})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': tags})

def notes_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    notes = Note.objects.filter(tag=tag)
    return render(request, 'notes/notes_by_tag.html', {'tag': tag, 'notes': notes})