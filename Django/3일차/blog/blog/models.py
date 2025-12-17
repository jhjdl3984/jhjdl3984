from django.db import models

class Blog(models.Model):
    CATEGORY_CHOICES = (
        # 첫번째 값 => DB에 저장되는 값 / 두번째 값 => 사람에게 보여질 값
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )
    # max_length => 각 카테고리의 글자길이 (카테고리 개수 X)
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    # author = models.CharField(pk=pk)
    content = models.TextField('본문')
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

    def __str__(self):
        # get_category_display() => self.category 값(free, cat, ...)을 보고 choices에서 매칭되는 두번째 값을 찾아 반환
        return f'[{self.get_category_display()}] {self.title[:10]}'

    # python manage.py makemigrations => DB 변경사항이 있을 때 사용
