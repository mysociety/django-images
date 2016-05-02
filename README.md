# django-images
Attach images to any Django model, with helpful admin


## Usage

You can create a GenericRelation from your model to the Images model.

```
# coding=utf-8
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from images.models import Image


class MyModel(models.Model, HasImageMixin):
    ...
    images = GenericRelation(Image)
    ...
```

And then you can create images and relate them to your model. i.e.
```
>> my_object = MyModel.objects.create(...)
>> image = Image.objects.create(content_object=my_object)
## And then you can get your primary image
>> my_object.primary_image()
```

The way to use within your templates is as follow:

```
<img src="{% static object.primary_image.url %}">
```
