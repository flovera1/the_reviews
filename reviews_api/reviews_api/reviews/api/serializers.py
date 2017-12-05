from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )


from accounts.api.serializers import UserDetailSerializer
#from comments.api.serializers import CommentSerializer
#from comments.models import Comment

from reviews.models import Reviews


class ReviewsCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            #'id',
            'company',
            #'slug',
            'comment',
            'pub_date'
        ]


reviews_detail_url = HyperlinkedIdentityField(
        view_name='reviews-api:detail',
        lookup_field='slug'
        )


class ReviewsDetailSerializer(ModelSerializer):
    url      = reviews_detail_url
    user     = UserDetailSerializer(read_only=True)
    comment  = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'company',
            'slug',
            
            'publish',
            
            'comment',
        ]

    def get_html(self, obj):
        return obj.get_markdown()



class ReviewsListSerializer(ModelSerializer):
    url = reviews_detail_url
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Reviews
        fields = [
            #'id',
            'company',
            #'slug',
            'comment',
            'pub_date'
        ]




""""

from posts.models import Post
from posts.api.serializers import PostDetailSerializer


data = {
    "title": "Yeahh buddy",
    "content": "New content",
    "publish": "2016-2-12",
    "slug": "yeah-buddy",
    
}

obj = Post.objects.get(id=2)
new_item = PostDetailSerializer(obj, data=data)
if new_item.is_valid():
    new_item.save()
else:
    print(new_item.errors)


"""