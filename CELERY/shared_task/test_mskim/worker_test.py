from app1.tasks import add
from app1.tasks import mul
from celery.result import AsyncResult
from test_mskim.conf_celery import result_backend

print("add Function first call")
k1 = AsyncResult(mul.delay(4,4), app=mul)
print(k1.get())

print("\n add Function second call")
k2 = AsyncResult(add.apply_async((1,1), countdown=3), app=add)
print(k2.get())

print("add Function third call")
k3 = AsyncResult(mul.apply_async((5,6), countdown=5), app=mul)
print(k3.get())
