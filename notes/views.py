from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm  # Importe um formulário para a nota (criaremos isso a seguir)

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        # TAREFA: Utilize o title e content para criar um novo Note no banco de dados
        new_note = Note(title=title, content=content)
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
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirecione para a página inicial após a edição
    else:
        form = NoteForm(instance=note)
        
    return render(request, 'notes/edit.html', {'form': form, 'note': note})