from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = (
        models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="notes",
        ))

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="notes",
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="notes"
    )

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title



# ============================================================
# Поля моделей Django и их примерные аналоги в SQL
# ============================================================
#
# Django Field                         SQL Type
# ------------------------------------------------------------
#
# CharField(max_length=100)         -> VARCHAR(100)
# TextField()                       -> TEXT
# IntegerField()                    -> INTEGER / INT
# SmallIntegerField()               -> SMALLINT
# BigIntegerField()                 -> BIGINT
# PositiveIntegerField()            -> INTEGER / INT
# PositiveSmallIntegerField()       -> SMALLINT
#
# FloatField()                      -> DOUBLE PRECISION / REAL
# DecimalField(max_digits=10,
#              decimal_places=2)   -> DECIMAL(10, 2) / NUMERIC(10, 2)
#
# BooleanField()                    -> BIT
#
# DateField()                       -> DATE
# TimeField()                       -> TIME
# DateTimeField()                   -> DATETIME / TIMESTAMP
# DurationField()                   -> INTERVAL / BIGINT
#
# EmailField()                      -> VARCHAR
# URLField()                        -> VARCHAR
# SlugField()                       -> VARCHAR
# UUIDField()                       -> UUID / CHAR(32)
#
# BinaryField()                     -> BINARY
#
# JSONField()                       -> JSON / JSONB / TEXT
#
# AutoField()                       -> INTEGER + AUTO INCREMENT
# BigAutoField()                    -> BIGINT + AUTO INCREMENT
# SmallAutoField()                  -> SMALLINT + AUTO INCREMENT
#
# FileField()                       -> VARCHAR
# ImageField()                      -> VARCHAR
#   Примечание: Файл/изображение не хранится непосредственно в БД.
#   В БД хранится только путь (path) к файлу.
#
# ============================================================
# Поля отношений (Relationship Fields)
# ============================================================
#
# ForeignKey(Model, ...)           -> FOREIGN KEY
# OneToOneField(Model, ...)         -> FOREIGN KEY + UNIQUE
#
# ManyToManyField(Model)           -> создаётся отдельная промежуточная
#                                     таблица связей (junction table).
#
# Например:
#
# class Article(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#
# Логика SQL:
#
# author_id BIGINT
# FOREIGN KEY (author_id) REFERENCES user(id)
#
# ============================================================
# Основные параметры Field и их аналоги в SQL
# ============================================================
#
# primary_key=True                 -> PRIMARY KEY
# unique=True                      -> UNIQUE
# null=True                        -> разрешает NULL
# null=False                       -> NOT NULL
# db_index=True                    -> создаётся INDEX
# default=value                    -> DEFAULT (не всегда на уровне БД)
#
# blank=True                       -> не связано с SQL!
#                                     Используется для валидации Django.
#
# editable=False                   -> не связано с SQL.
#                                     Используется в Django Admin/Form.
#
# choices=[...]                    -> Обычно не изменяет SQL-тип.
#                                     Ограничивает выбор на уровне Django.
#
# max_length=100                   -> определяет длину, например VARCHAR(100).
#
# ============================================================
# Важное примечание
# ============================================================
#
# Соответствие Django Field -> SQL Type может отличаться
# в зависимости от используемой базы данных:
#
# SQLite      PostgreSQL       MySQL
# -----------------------------------------------
# INTEGER     INTEGER          INT
# TEXT        TEXT             LONGTEXT
# BOOLEAN     BOOLEAN          BOOL/TINYINT
# DATETIME    TIMESTAMP        DATETIME
#
# Поэтому приведённые выше соответствия являются
# общими/приблизительными.
#
# Django самостоятельно создаёт конкретный SQL-тип
# в соответствии с используемым DATABASE ENGINE.
#
# Django Model
#       |
#       v
# Migration
#       |
#       v
# SQL
#       |
#       v
# Database Table
#
# models.CharField(max_length=100)
#       ↓
# migrations
#       ↓
# VARCHAR(100)

