from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from .models import BookInfo,PeopleInfo
from  .serializers import BookInfoSerializer,PeopleInfoSerializer
# Create your views here.

#######################视图相关的内容#################################

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
class BookGenericAPIView(ListModelMixin,RetrieveModelMixin,GenericAPIView):

    # 增加了对于列表视图和详情视图可能用到的通用支持方法

    #通过我们要 重写  queryset -->结果集
    # serializer_class  -->序列化器类
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    # lookup_field = 'id'

    #列表视图
    # def get(self,request):
    #
    #     #获取所有数据
    #     books = self.get_queryset()
    #     # 经过序列化器的序列化
    #     # get_serializer() 能够获取到一个序列化器实例对象
    #     serializer = self.get_serializer(books,many=True)
    #     #返回响应
    #     return Response(serializer.data)

    # GenericAPIView一般和 Mixin扩展类配合使用
    # def get(self,request):
    #     return self.list(request)

    #详情视图可能用到的通用支持方法
    # def get(self,request,pk):
    #
    #     #获取制定的书籍
    #     # books = BookInfo.objects.get(id=id)
    #     book = self.get_object()
    #     #获取序列化器对象
    #     serializer = self.get_serializer(book)
    #     #返回响应
    #     return JsonResponse(serializer.data)

    def get(self,request,pk):

        return self.retrieve(request)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class BookAPIView(APIView):

    def get(self,request):

        # 以前 request.GET 我们现在在APIView中
        #用 request.query_params
        params = request.query_params
        #<QueryDict: {'a': ['100']}>
        print(params)

        #获取书籍模型
        book = BookInfo.objects.get(id=1)
        #通过序列化器进行模型转JSON
        serializer = BookInfoSerializer(book)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self,request):

        # 以前request.POST request.body 现在用
        # request.data 来获取欧
        data = request.data

        # print(data)
        #{'name': '射雕英雄前传xxxxxxxxxxx', 'pub_date': '2000-1-1', 'readcount': 200}
        #获取数据进行校验
        serializer = BookInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #校验完成之后入库
        serializer.save()
        #返回JSON数据
        return Response(serializer.data,status=200)






# 反序列化 ： JSON --》校验 -->模型类

#第一种校验,字段选项的校验， required 默认为True 反序列化的时候必须传入此字段的值
#第二种校验 ，字段类型的校验， 例如 datefiled 必须传时间格式
#第三种校验， 针对于某个字段的值进行校验 ，语法形式为 validate_字段名
#第四中校验， 针对于多个字段的值进行校验， 使用序列化器的 validate
#第五种校验， 在字段选项 validators 中，添加自定义验证方法
#第六中校验， 我们可以针对于 唯一键字段进行校验

# from book.models import BookInfo
# from book.serializers import BookInfoSerializer
#
# #获取数据
# data = {
#     'name':'射雕英雄前传',
#     'pub_date':'2000-1-1'
# }
#
# # 经过反序列化
# # 第一个参数 instanc 指向模型
# # 第二个参数 data
# serializer = BookInfoSerializer(data=data)
# #需要对数据进行 校验
# #如果 data校验没有问题， 则返回true,否则返回False
# serializer.is_valid(raise_exception=True)
# serializer.save()


###############数据更新的操作##################
# from book.models import BookInfo
# from book.serializers import BookInfoSerializer
#
# #获取数据
# data = {
#     'name':'射雕英雄前传',
#     'pub_date':'2000-1-1'
# }
#
# book = BookInfo.objects.get(id=1)
#
# #创建序列化器对象
# #第一个参数是 instance -->模型
# #第二个参数 data  -->字典（JSON）
# serializer = BookInfoSerializer(instance=book,data=data)
# serializer.is_valid()
# serializer.save()

# from book.models import BookInfo
# from book.serializers import BookSerializer
#
# #创建一个序列化器对象
# serializer = BookSerializer()
#
# class BookView(View):
#
#
#     def get(self,request):
#
#         #获取所有图书
#         # books = BookInfo.objects.all()
#         # #将图书 序列化 （将模型转换为JSON）
#         # serializer = BookInfoSerializer(instance=books,many=True)
#         #
#         # # serializer.data
#         # return JsonResponse(serializer.data,safe=False)
#         # return HttpResponse('ok')
#
#         #获取一个人物信息
#         person = PeopleInfo.objects.get(id=1)
#         #创建序列化器对象
#         serializer = PeopleInfoSerializer(instance=person)
#         #返回JSON
#         return JsonResponse(serializer.data,safe=False)
#
#
#     def post(self,request):
#
#         # 反序列化
#         #接受参数
#         # request.body
#         body_bytes = request.body
#         body_str = body_bytes.decode()
#         import json
#         body_json = json.loads(body_str)
#
#         #校验参数,创建序列化对象
#         serializer = BookInfoSerializer(data=body_json)
#         # 创建了序列化器对象，进行反序列化操作的时候，必须要调用 is_valid方法
#         serializer.is_valid(raise_exception=True)
#         #数据入库
#         serializer.save()
#         #返回响应
#         return JsonResponse(serializer.data)



