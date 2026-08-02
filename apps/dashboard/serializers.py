from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    total_books = serializers.IntegerField()
    total_copies = serializers.IntegerField()
    available_copies = serializers.IntegerField()
    borrowed_copies = serializers.IntegerField()
    damaged_copies = serializers.IntegerField()
    pending_returns = serializers.IntegerField()
    overdue_books = serializers.IntegerField()
    total_students = serializers.IntegerField()
    current_visitors = serializers.IntegerField()
    today_visits = serializers.IntegerField()