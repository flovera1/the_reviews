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
        model = Reviews
        fields = [
            'id',
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
        model = Reviews
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
            'id',
            'company',
            #'slug',
            'comment',
            'pub_date'
        ]


