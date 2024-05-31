from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

class Category(TranslatableModel):
    translations = TranslatedFields(
    name = models.CharField(max_length=200),
    slug = models.SlugField(max_length=200, unique=True) # 중복을 허용하지 않는다.
    )
    class Meta:
        #ordering = ['name']
        #indexes = [models.Index(fields=['name']),]
        verbose_name = 'category' # 사용자가 사용할 자세한 이름을 지정
        verbose_name_plural = 'categories' # 복수형으로 사용할 이름을 지정할때 사용,
        # 장고 어드민이 알아서 복수로 만들어 줄경우, category -> categorys 형태로 만들어 버려서....
    def __str__(self):
        return self.name

    def get_absolute_url(self): # 주어진 객체의 URL을 조회하는 방식, urls.py파일에서 정의한 URL 패턴을 사용
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200),
        description = models.TextField(blank=True)
    )
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) #화폐 금액을 저장 , 십진수타입 , 소수점 반올림시 문제를 일으키지 않는다.
    #decimal_places 소수점 몇자리 , 소수점 2자리 까지 허용
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        #ordering = ['name']
        indexes = [
            #models.Index(fields=['id', 'slug']),
            #models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])