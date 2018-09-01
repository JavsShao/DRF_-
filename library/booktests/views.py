from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin

from .models import BookInfo
from  .serializers import BookInfoSerializer
# Create your views here.


class BookGenericAPIView(ListModelMixin,RetrieveModelMixin,GenericAPIView):

    # serializer_class  -->序列化器类
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer


    def get(self,request,pk):

        return self.retrieve(request)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class BookAPIView(APIView):

    def get(self,request):

        params = request.query_params
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

        #{'name': '射雕英雄前传xxxxxxxxxxx', 'pub_date': '2000-1-1', 'readcount': 200}
        #获取数据进行校验
        serializer = BookInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #校验完成之后入库
        serializer.save()
        #返回JSON数据
        return Response(serializer.data,status=200)








