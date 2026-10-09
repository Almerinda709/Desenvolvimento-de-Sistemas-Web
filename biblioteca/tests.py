from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase

from .models import Author, Book, Category


class AuthorTests(TestCase):
    def test_nacionalidade_e_opcional(self):
        autor = Author.objects.create(name="Machado de Assis")
        self.assertEqual(autor.nationality, "")

    def test_autor_com_livros_nao_pode_ser_apagado(self):
        autor = Author.objects.create(name="Machado de Assis")
        Book.objects.create(title="Dom Casmurro", author=autor, year=1899)
        with self.assertRaises(ProtectedError):
            autor.delete()

    def test_autor_sem_livros_pode_ser_apagado(self):
        autor = Author.objects.create(name="Jorge Amado")
        autor.delete()
        self.assertEqual(Author.objects.count(), 0)

    def test_related_name_books(self):
        autor = Author.objects.create(name="Machado de Assis")
        Book.objects.create(title="Dom Casmurro", author=autor, year=1899)
        Book.objects.create(title="Quincas Borba", author=autor, year=1891)
        self.assertEqual(autor.books.count(), 2)

    def test_autores_ordenados_por_nome(self):
        Author.objects.create(name="Jorge Amado")
        Author.objects.create(name="Clarice Lispector")
        nomes = [a.name for a in Author.objects.all()]
        self.assertEqual(nomes, ["Clarice Lispector", "Jorge Amado"])


class CategoryTests(TestCase):
    def test_nome_unico(self):
        Category.objects.create(name="Romance")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Romance")


class BookTests(TestCase):
    def test_livro_pode_ficar_sem_categoria(self):
        autor = Author.objects.create(name="Machado de Assis")
        livro = Book.objects.create(title="Dom Casmurro", author=autor, year=1899)
        self.assertEqual(livro.categories.count(), 0)

    def test_livro_com_varias_categorias(self):
        autor = Author.objects.create(name="Machado de Assis")
        livro = Book.objects.create(title="Dom Casmurro", author=autor, year=1899)
        livro.categories.set([Category.objects.create(name="Romance"), Category.objects.create(name="Clássico")])
        self.assertEqual(livro.categories.count(), 2)
