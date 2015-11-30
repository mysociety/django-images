from django.db import models
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    # This fallback import is the version that was deprecated in
    # Django 1.7 and is removed in 1.9:
    from django.contrib.contenttypes.generic import GenericForeignKey

from sorl.thumbnail import ImageField


class Image(models.Model):

    # link to other objects using the ContentType system
    content_type   = models.ForeignKey(ContentType)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # store the actual image
    image = ImageField( upload_to="images" )

    # added
    source = models.CharField(max_length=400)
    # user

    is_primary = models.BooleanField( default=False )

    def save(self, *args, **kwargs):
        """
        Only one image should be marked as is_primary for an object.
        """

        # other images for this object
        siblings = Image.objects.filter(
            content_type = self.content_type,
            object_id    = self.object_id,
        )

        # check that we are not first entry for content_object
        if not siblings.count():
            self.is_primary = True

        super(Image, self).save(*args, **kwargs)

        # If we are true then make sure all others are false
        if self.is_primary is True:

            primary_siblings = siblings.exclude( is_primary = False ).exclude( id = self.id )

            for sibling in primary_siblings:
                sibling.is_primary = False
                sibling.save()


class HasImageMixin():

    def primary_image(self):
        primary_image_model = self.primary_image_model()
        if primary_image_model:
            return primary_image_model.image
        return None

    def primary_image_model(self):
        primary_images = [i for i in self.images.all() if i.is_primary]
        if primary_images:
            return primary_images[0]
        return None
