import django.db.models.deletion
from django.db import migrations, models


def criar_autores(apps, schema_editor):
    Author = apps.get_model("biblioteca", "Author")
    Book = apps.get_model("biblioteca", "Book")
    for livro in Book.objects.all():
        autor, _ = Author.objects.get_or_create(name=livro.author_name)
        livro.author = autor
        livro.save()


def voltar_nomes(apps, schema_editor):
    Book = apps.get_model("biblioteca", "Book")
    for livro in Book.objects.all():
        livro.author_name = livro.author.name
        livro.save()


class Migration(migrations.Migration):

    dependencies = [
        ("biblioteca", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("nationality", models.CharField(blank=True, max_length=60)),
            ],
            options={
                "verbose_name": "Autor",
                "verbose_name_plural": "autores",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, unique=True)),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
                "ordering": ["name"],
            },
        ),
        migrations.RenameModel("Livro", "Book"),
        migrations.RenameField("Book", "titulo", "title"),
        migrations.RenameField("Book", "ano_publicacao", "year"),
        migrations.RenameField("Book", "disponivel", "available"),
        migrations.RenameField("Book", "autor", "author_name"),
        migrations.AlterModelOptions(
            name="book",
            options={"ordering": ["title"], "verbose_name": "Livro", "verbose_name_plural": "Livros"},
        ),
        migrations.AddField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="books",
                to="biblioteca.author",
            ),
        ),
        migrations.RunPython(criar_autores, voltar_nomes),
        migrations.RemoveField("Book", "author_name"),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="books",
                to="biblioteca.author",
                verbose_name="autor",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="categories",
            field=models.ManyToManyField(blank=True, related_name="books", to="biblioteca.category", verbose_name="categorias"),
        ),
        migrations.AlterField(
            model_name="book",
            name="title",
            field=models.CharField(max_length=200, verbose_name="título"),
        ),
        migrations.AlterField(
            model_name="book",
            name="year",
            field=models.IntegerField(verbose_name="ano de publicação"),
        ),
        migrations.AlterField(
            model_name="book",
            name="available",
            field=models.BooleanField(default=True, verbose_name="disponível"),
        ),
    ]
