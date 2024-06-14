from django.shortcuts import get_object_or_404
from ninja import NinjaAPI , responses 
from .models import *
from .schemas import *
from django.http import  JsonResponse  , HttpResponse 
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ninja.errors import HttpError
api = NinjaAPI()

def handle_exception(e):
    if isinstance(e, ObjectDoesNotExist):
        return JsonResponse({"error": "Object not found"}, status=404)
    elif isinstance(e, ValidationError):
        return JsonResponse({"error": e.messages}, status=400)
    elif isinstance(e, HttpError):
        return JsonResponse({"error": str(e)}, status=e.status_code)
    else:
        return JsonResponse({"error": "An unexpected error occurred "}, status=500)
    
# CRUD FUCNTIONS : 
@api.post("/category/",response=CategoryIn)
def create_category(request,payload:CategoryIn):
    try : 
        category=Category.objects.create(
            name=payload.name,
            description=payload.description
        )
        return CategoryIn(
            id=category.id,
            name=category.name,
            description=category.description,
        )
    except Exception as e:
        return handle_exception(e)

@api.post("/tags/",response=TagIn)
def create_tags(request,payload : TagIn):
    try:
        tags=Tag.objects.create(
            name=payload.name,
            description=payload.description
        )
        return TagIn(
            id=tags.id,
            name=tags.name,
            description=tags.description
        )
    except Exception as e:
        return handle_exception(e)
    
@api.post("/items/", response=ItemOut)
def create_item(request, payload: ItemIn):
    try:
        category = get_object_or_404(Category, id=payload.category_id)
        tag = get_object_or_404(Tag, id=payload.tag_id)

        item = Item.objects.create(
            name=payload.name,
            description=payload.description,
            tag=tag,
            weight=payload.weight,
            brand=payload.brand,
            category=category,
        )
        item_dict = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'tag_id': tag.id,
            'category_id': category.id,
            'weight': item.weight,
            'brand': item.brand,
        }

        return item_dict
    except Exception as e:
        return handle_exception(e)

@api.post("/woocomerseuser/",response=woocomerseuserIn)
def create_woocomeerseuser(request,payload : woocomerseuserIn):
    try:
        woocomerceuserr= woocomerceuser.objects.create(
            consumer_key=payload.consumer_key,
            secret_key=payload.serect_key,
            active=payload.active,
        )
        return woocomerseuserIn(
            id=woocomerceuserr.id,
            consumer_key=woocomerceuserr.consumer_key,
            serect_key=woocomerceuserr.secret_key,
            active=woocomerceuserr.active
        )
    except Exception as e:
        return handle_exception(e)

@api.post("/integration/",response=integrateIn)
def create_integration(request,payload : integrateIn):
    try:
        integratee=integrate.objects.create(
            type=payload.type,
            consumer_key=payload.consumer_key,
            secret_key=payload.serect_key,
            active=payload.active,
            name=payload.name,
            description=payload.description
        )
        return integrateIn(
            id=integratee.id,
            type=integratee.type,
            consumer_key=integratee.consumer_key,
            serect_key=integratee.secret_key,
            active=integratee.active,
            name=integratee.name,
            description=integratee.description
        )
    except Exception as e:
        return handle_exception(e)

@api.delete("/category/{category_id}/")
def delete_category(request, category_id: int):
    category = Category.objects.filter(id=category_id).first()
    if not category:
        return HttpResponse(status=404)

    category.delete()
    return {"succces" : True}

@api.put("/category/{category_id}/", response=CategoryIn)
def update_category(request, category_id: int, payload: CategoryIn):
    category = get_object_or_404(Category, id=category_id)

    category.name = payload.name
    category.description = payload.description
    category.save()

    return CategoryIn(
        id=category.id,
        name=category.name,
        description=category.description
    )

@api.delete("/tag/{tag_id}/")
def delete_tag(request, tag_id: int):
    tag = Tag.objects.filter(id=tag_id).first()
    if not tag:
        return HttpResponse(status=404)

    tag.delete()
    return {"succces" : True}

@api.put("/tag/{tag_id}/", response=TagIn)
def update_tag(request, tag_id: int, payload: TagIn):
    tag= get_object_or_404(Tag, id=tag_id)

    tag.name = payload.name
    tag.description = payload.description
    tag.save()

    return TagIn(
        id=tag.id,
        name=tag.name,
        description=tag.description
    )

@api.delete("/item/{item_id}/")
def delete_item(request, item_id: int):
    item = Item.objects.filter(id=item_id).first()
    if not item:
        return HttpResponse(status=404)

    item.delete()
    return HttpResponse(status=204)

@api.put("/item/{item_id}/", response=ItemIn)
def update_item(request, item_id: int, payload: ItemIn):
    item = get_object_or_404(Item, id=item_id)
    category = get_object_or_404(Category, id=payload.category_id)

    item.category = category
    item.name = payload.name
    item.description = payload.description
    item.weight = payload.weight
    item.brand = payload.brand
    item.save()

    return ItemIn(
        id=item.id,
        name=item.name,
        description=item.description,
        weight=item.weight,
        brand=item.brand,
        category_id=category.id
    )

@api.delete("/woocommerce/{woocommerce_id}/",response=woocomerseuserIn)
def delete_woocommerce(request,woocommerce_id : int):
    woocommercee=woocomerceuser.objects.filter(id=woocommerce_id).first()
    if not woocommercee:
        return HttpResponse(status=404)

    woocommercee.delete()
    return HttpResponse(status=204)

@api.put("/woocommerce/{woocommerce_id}/",response=woocomerseuserIn)
def update_woocommerce(request, woocommerce_id : int , payload : woocomerseuserIn):
    woocommmrcee=get_object_or_404(woocomerceuser,id=woocommerce_id)
    woocommmrcee.consumer_key=payload.consumer_key
    woocommmrcee.secret_key=payload.consumer_key
    woocommmrcee.active=payload.active
    woocommmrcee.save()

    return woocomerseuserIn(
        id=woocommmrcee.id,
        consumer_key=woocommmrcee.consumer_key,
        serect_key=woocommmrcee.secret_key,
        active=woocommmrcee.active,
    )

@api.delete("/integration/{integration_id}/",response=integrateIn)
def delete_integration(request, integration_id : int):
    integrationn = integrate.objects.filter(id=integration_id).first()
    if not integrationn :
        return HttpResponse(status=404)
    
    integrationn.delete()
    return HttpResponse(status=204)

@api.put("/integration/{integration_id}/",response=integrateIn)
def update_integrate(request,integration_id : int , payload : integrateIn):
    integratee=get_object_or_404(integrate,id=integration_id)
    integratee.type=payload.type
    integratee.consumer_key=payload.consumer_key
    integratee.secret_key=payload.serect_key
    integratee.active=payload.active
    integratee.name=payload.name
    integratee.description=payload.description


    return integrateIn(
        id=integratee.id,
        type=integratee.type,
        consumer_key=integratee.consumer_key,
        serect_key=integratee.secret_key,
        active=integratee.active,
        name=integratee.name,
        description=integratee.description,
    )


@api.get("/category/{category_id}/", response=CategoryIn)
def get_category(request, category_id: int):
    try:
        category = get_object_or_404(Category, id=category_id)
        return CategoryIn(
            id=category.id,
            name=category.name,
            description=category.description
        )
    except Exception as e:
        return handle_exception(e)



@api.get("/tags/{tag_id}/", response=TagIn)
def get_tag(request, tag_id: int):
    try:
        tag = get_object_or_404(Tag, id=tag_id)
        return TagIn(
            id=tag.id,
            name=tag.name,
            description=tag.description
        )
    except Exception as e:
        return handle_exception(e)


@api.get("/items/{item_id}/", response=ItemOut)
def get_item(request, item_id: int):
    try:
        item = get_object_or_404(Item, id=item_id)
        item_dict = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'tag_id': item.tag.id,
            'category_id': item.category.id,
            'weight': item.weight,
            'brand': item.brand,
        }
        return item_dict
    except Exception as e:
        return handle_exception(e)



@api.get("/woocomerseuser/{user_id}/", response=woocomerseuserIn)
def get_woocomerseuser(request, user_id: int):
    try:
        woocomerceuserr = get_object_or_404(woocomerceuser, id=user_id)
        return woocomerseuserIn(
            id=woocomerceuserr.id,
            consumer_key=woocomerceuserr.consumer_key,
            serect_key=woocomerceuserr.secret_key,
            active=woocomerceuserr.active
        )
    except Exception as e:
        return handle_exception(e)


@api.get("/integration/{integration_id}/",response=integrateIn)
def get_integration(request,integration_id : int):
    try:
        integration=get_object_or_404(integrate,id=integration_id)
        return integrateIn(
            id=integration.id,
            type=integration.type,
            consumer_key=integration.consumer_key,
            serect_key=integration.secret_key,
            active=integration.active,
            name=integration.name,
            description=integration.description,
        )
    except Exception as e :
        return handle_exception(e)
    