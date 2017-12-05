from rest_framework import serializers
from .models import Reviews, Company
from django.contrib.auth.models import User

from django.db.models import Q

from rest_framework.authtoken.models import Token

from rest_framework.serializers import (
	CharField,
	EmailField,
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField,
	ValidationError)



class ReviewsSerializer(serializers.ModelSerializer):
	"""Serializer to map the Model instance into JSON format."""
	#owner = serializers.ReadOnlyField(source = 'owner.username') 
	owner 			 = serializers.ReadOnlyField(source='owner.username')
	#highlight 		 = serializers.HyperlinkedIdentityField(view_name='views-highlight', format='html')
	class Meta:
		"""Meta class to map serializer's fields with the model fields."""
		model            = Reviews
		fields           = ('company', 'owner','pub_date',
		 					'user_name', 'comment', 'rating', 'title', 
		 					'summary', 
		 					'ip_address'
		 					)
		#read_only_fields = ('pub_date')
'''
class create_reviews_serializer(model_type='post', slug=None, user=None):
	class ReviewsCreateSerializer(ModelSerializer):
		class Meta:
			model = Reviews
			fields = ['id', 'comment', 'pub_date']

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug	    = slug
            self.parent_obj = None
            return super(ReviewsCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs   = ContentType.objects.filter(model = model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel  = model_qs.first().model_class()
            obj_qs     = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type, slug, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer
'''

class UserDetailSerializer(ModelSerializer):
	class Metal:
		model = User
		fields = [
			'user_name',
			'email', 
			'ip_address',
		]


class UserSerializer(serializers.ModelSerializer):
    reviews = serializers.PrimaryKeyRelatedField(many=True, queryset=Reviews.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'reviews', 
        	'ip_address'
        	)

'''
class UserCreateSerializer(serializers.ModelSerializer):
	email  = EmailField(label = "Email Address")
	email2 = EmailField(label = "Confirm email")
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]
		extra_kwargs = {"password":
						{"write_only": True}
						}
	def validate(self, data):
		# email   = data['email']
		# user_qs = User.objects.filter(email=email)
		# if user_qs.existx():
		#	raise ValidationError("This user has already registered")	
		return data

	def validate_email(self, value):
		data   = self.get_initial()
		email1 = data.get("email2")
		email2 = value
		if email1 != email2:
			raise ValidationError("emails must match.")

		user_qs = User.objects.filter(email = email2)
		if user_qs.exists():
			raise ValidationError("This user has already registered")

		return value

	def validate_email2(self, value):
		data   = self.get_initial()
		email1 = data.get("email")
		email2 = value
		if email1 != email2:
			raise ValidationError("emails must match.")
		return value

	def create(self, validated_data):
		username = validated_data['username']
		email    = validated_data['email']
		password = validated_data['password']
		user_obj = User(
			username=username,
			email=email
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data


'''
'''
class UserLoginSerializer(serializers.ModelSerializer):
	token    = CharField(allow_blank=True, read_only = True)
	username = CharField(required = False, allow_blank = True)
	email  = EmailField(label = "Email Address", required = False, allow_blank = True)
	
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'token',
		]
		extra_kwargs = {"password":
						{"write_only": True}
						}
	def validate(self, data):
		user_obj = None
		email    = data.get("email", None)
		username = data.get("username", None) 
		password = data["password"]
		if not email and not username:
			raise ValidationError ("A username or email is required to login.")
		
		user = User.objects.filter(
				Q(email = email)|
				Q(username = username)
				).distinct()
		user = user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("This username/email is not valid.")

		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials please try again")

	#	data["token"] = "some random token"#Token.objects.create(user=instance)

		return data
'''

