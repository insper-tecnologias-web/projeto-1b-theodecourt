from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag_name = request.POST.get('tag').lower()

        if tag_name!='':
            tag, created = Tag.objects.get_or_create(name=tag_name)
            new_note = Note(title=title, content=content, tag=tag)
        else:
            new_note = Note(title=title, content=content)
    
        new_note.save()
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})
    
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    #note = Note.objects.get(id=note_id) #possivel tanto a opcao assima quanto essa
    
    tag = note.tag

    note.delete()

    if tag:
        if not Note.objects.filter(tag=tag).exists():
            # Se não estiver mais sendo usada, exclua a tag
            tag.delete()
    return redirect('index')  # Redirecionar para a página de lista de notas após a exclusão

def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_name = request.POST.get('tag').lower()  


        old_tag = note.tag
        
        if tag_name != '':
            tag, created = Tag.objects.get_or_create(name=tag_name)
            note.tag = tag
        else:
            note.tag = None

        note.title = title
        note.content = content
        note.save()

        if old_tag:
            if not Note.objects.filter(tag=old_tag).exclude(pk=note_id).exists():
                # Se não estiver mais sendo usada, exclua a tag antiga
                old_tag.delete()

        return redirect('index')  # Redirecionar para a página inicial após a edição
    
    return render(request, 'notes/edit.html', {'note': note})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': tags})

def notes_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    notes = Note.objects.filter(tag=tag)
    return render(request, 'notes/notes_by_tag.html', {'tag': tag, 'notes': notes})