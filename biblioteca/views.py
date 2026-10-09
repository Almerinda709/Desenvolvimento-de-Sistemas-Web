from django.shortcuts import get_object_or_404, render

from .models import Author, Book


def listar_livros(request):
    livros = Book.objects.select_related("author")
    return render(request, "biblioteca/lista_livros.html", {"livros": livros})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, "biblioteca/author_detail.html", {"author": author, "livros": author.books.all()})
