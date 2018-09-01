#coding:utf8
from rest_framework import serializers
from .models import BookInfo
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        #元选项，就可以理解为 进行一些配置
        model = BookInfo        #必须要设置关联的模型
        #fields = '__all__'      #必须设置fields  __all__表示所有字段
        #制定字段
        # fields = ['id','readcount','name','commentcount']

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


# 联合主键
# 联合唯一键

# name 字段 和 pub_date 字段为 联合唯一键

# name-pub_date

# 射雕英雄传-2000-1-1    这是一条唯一的记录

# 射雕英雄传-2000-1-2    这是一条唯一的记录

# 射雕英雄前传-2000-1-1    这是一条唯一的记录

# 射雕英雄传-2000-1-1    就冲突了！@！！！！！！


#  Django文档
# 串行器字段处理原始值和内部数据类型之间的转换。
    # 模型 --》JSON    序列化
    # JSON --》模型    反序列化
# 他们还处理验证输入值
class BookInfoSerializer(serializers.Serializer):

    #required	表明该字段在反序列化时必须输入，默认True

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
        #validated_data
        # 验证后的数据，已经通过我们的层层验证
        # {‘name’:'xxxx',...}

        #BookInfo(**validated_data) 这样数据不能直接入库
        # book =BookInfo(**validated_data)
        # book.save()
        # return book

        #也可以这样操作
        return BookInfo.objects.create(**validated_data)

    #把name设置为唯一的
    # name = serializers.CharField(max_length=20,validators=[
    #     UniqueValidator(queryset=BookInfo.objects.all())
    # ])

    #多个字段校验
    # def validate(self, data):
    # def validate(self, attrs):
    #     # attrs 就是我们传递过来的data
    #
    #     readcount = attrs.get('readcount')
    #     commentcount = attrs['commentcount']
    #     if readcount<commentcount:
    #         raise serializers.ValidationError('评论量不能大于阅读量')
    #
    #     #如果数据没有问题就把数据返回
    #     return attrs
    #
    #
    #
    # # validate_字段名（self,value）
    # def validate_readcount(self,value):
    #
    #     if value<0:
    #         raise serializers.ValidationError('阅读量不能为负数')
    #
    #     return value




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