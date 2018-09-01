#coding:utf8
from rest_framework import serializers
from .models import BookInfo
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookInfo        #必须要设置关联的模型
        #设置只读字段
        read_only_fields = ['id','name']
        exclude = ['image']
        #额外设置 字段的选项
        extra_kwargs = {
            # “字段名”：{"选项名"：选项值}  语法
            'readcount':{
                'min_value':0
            },
            'pub_date':{
                'required':True
            }

        }

# 他们还处理验证输入值
class BookInfoSerializer(serializers.Serializer):


    def custom_validate(value):
        raise serializers.ValidationError('我就是来捣乱的')

    id = serializers.IntegerField(label='ID',read_only=True)
    # validators=[函数名]
    #name = serializers.CharField(label='书籍名',max_length=20,validators=[custom_validate])
    name = serializers.CharField(label='书籍名',max_length=20)
    pub_date = serializers.DateField(label='发布日期',allow_null=True)
    readcount = serializers.IntegerField(label='阅读量',default=0,required=False)
    commentcount = serializers.IntegerField(label='评论量',default=0,required=False)
    is_delete = serializers.BooleanField(label='逻辑删除',default=False)
    image = serializers.ImageField(label='图片',allow_null=True,required=False)


    #实现 update方法
    def update(self, instance, validated_data):
        # instance -->模型
        # validated_data -->验证后的数据

        instance.name = validated_data.get('name',instance.name)
        instance.pub_date = validated_data.get('pub_date',instance.pub_date)
        instance.readcount = validated_data.get('readcount',instance.readcount)
        instance.commentcount = validated_data.get('commentcount',instance.commentcount)

        #保存
        instance.save()

        return instance


    #实现 create 方法
    def create(self, validated_data):

        return BookInfo.objects.create(**validated_data)




class PeopleInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(label='名字', max_length=20)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    description = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)

    book = BookInfoSerializer()