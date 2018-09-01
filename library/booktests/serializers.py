from rest_framework import serializers

from library.booktests.models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID',read_only=True)
    btitle = serializers.CharField(label='名称',max_length=20)
    bpub_data = serializers.DateField(label='发布日期',required=False)
    bcomment = serializers.IntegerField(label='评论量',required=True)
    image = serializers.ImageField(label='图片',required=False)