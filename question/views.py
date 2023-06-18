from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question,Comment
from .serializers import QuestionSerializer, CommentSerializer

class QuestionListCreateView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request):
        questions = Question.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionRetrieveUpdateDestroyView(APIView):
    serializer_class = QuestionSerializer

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = self.serializer_class(question)
        if request.user.is_authenticated:
            request.user.last_viewed_questions.add(question)
            if request.user.last_viewed_questions.count() > 10:
                request.user.last_viewed_questions.remove(
                    request.user.last_viewed_questions.earliest('created_at')
                )
        return Response(serializer.data)

    def put(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        data = request.data
        data["author"] = request.user.id
        serializer = self.serializer_class(question, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommentsView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, id):
        comments = Comment.objects.filter(question=id).order_by('id')
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)