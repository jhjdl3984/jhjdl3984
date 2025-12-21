from django.db import models

# Create your models here.
class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('url')
    create_at = models.DateTimeField('생성일시', auto_now_add=True)
    update_at = models.DateTimeField('수정일시', auto_now=True)

    # 생성한 북마크의 이름이 북마크프로젝트(1) => 생성할 때 쓴 name으로 바꿔줌
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'
