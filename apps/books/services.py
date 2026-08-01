from .models import Category


class CategoryService:

    @staticmethod
    def get_all_categories():
        return Category.objects.all().order_by("name")

    @staticmethod
    def get_category(category_id):
        return Category.objects.get(id=category_id)

    @staticmethod
    def create_category(validated_data):
        return Category.objects.create(**validated_data)

    @staticmethod
    def update_category(category, validated_data):

        for field, value in validated_data.items():
            setattr(category, field, value)

        category.save()

        return category

    @staticmethod
    def delete_category(category):
        category.delete()