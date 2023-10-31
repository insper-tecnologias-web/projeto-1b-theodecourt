from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .serializers import NoteSerializer
from rest_framework import status



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

@api_view(['GET', 'POST', 'DELETE'])
def api_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        new_note_data = request.data
        note.title = new_note_data['title']
        note.content =  new_note_data['content']
        note.save()

    if request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Retorna um código 204 indicando que a nota foi excluída com sucesso
    

    serialized_note = NoteSerializer(note)
    return Response(serialized_note.data)

@api_view(['GET', 'POST'])
def api_note2(request):
    notes = Note.objects.all()
    serialized_notes = []

    for note in notes:
        serialized_note = NoteSerializer(note)
        serialized_notes.append(serialized_note.data)

    if request.method == 'POST':
        new_note_data = request.data
        print(new_note_data)
        title = new_note_data['title']
        content = new_note_data['content']
        new_note = Note(title=title, content=content)
        new_note.save()

    return Response(serialized_notes)