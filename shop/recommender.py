import redis
from django.conf import settings
from .models import Product
#Redis 연결
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)
class Recommender:
    def get_product_key(self,id):
        # 프로덕트 객체의 Id를 받아서 관련 제품이 저장된 Redis 정렬된 세트의 키를 생성
        return f'product:{id}:purchased_with' # 키의 형식

    def products_bought(self,products): # 함께 구매된(동일주문) 프로덕트 객체의 목록을 받는다.
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id: # 각 제품과 함께 구매한 다른 제품 획득
                    r.zincrby(self.get_product_key(product_id), #함께 구매한 제품의 점수 증가
                              1,
                              with_id)
    def suggest_products_for(self, products, max_result=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # 단 1개의 제품
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0, -1, desc=True)[:max_result]
        else:
            #임시 키 생성
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # 주어진 각 제품들에 함께 구매한 제품의 점수 합산, 결과가 정렬된 세트를 임시 키에 저장
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            #처음에 주어진 제품들의 ID를 추천 목록에서 제거
            r.zrem(tmp_key, *product_ids)
            # 점수를 기준으로 역정렬해서 제품 ID 목록을 가져옴
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result]
            # 임시키 제거
            r.delete(tmp_key)
        suggested_product_ids = [int(id) for id in suggestions]
        # 추천 제품 정보 조회 및 순서대로 정렬해서 표시
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.value_list('id', flat=True):
            r.delete(self.get_product_key(id))
