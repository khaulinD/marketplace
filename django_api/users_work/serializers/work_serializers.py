from rest_framework import serializers
from ..models import UserWork, ExtraWorkInfo


class ExtraWorkInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraWorkInfo
        exclude = ('workID',)

class WorkSerializer(serializers.ModelSerializer):
    extra_info = ExtraWorkInfoSerializer(required=False)

    class Meta:
        model = UserWork
        fields = ['id', 'title', 'creatorID', 'description', 'created_at', 'updated_at', 'price', 'extra_info']
        read_only_fields = ['id', "creatorID"]  # Assuming id is read-only

    def create(self, validated_data):
        extra_info_data = validated_data.pop('extra_info', None)
        resume = UserWork.objects.create(**validated_data)
        if extra_info_data:
            ExtraWorkInfo.objects.create(resume=resume, **extra_info_data)
        return resume

    def update(self, instance, validated_data):
        print(instance)
        extra_info_data = validated_data.pop('extra_info', None)
        try:
            extra_info_instance = instance.extra_info
        except AttributeError:
            extra_info_instance = None

        # Update main Resume model fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        # Update related ExtraResumeInfo model fields
        if extra_info_data and extra_info_instance:
            extra_info_instance.work_course_lvl = extra_info_data.get('work_course_lvl',
                                                                        extra_info_instance.work_course_lvl)
            extra_info_instance.work_subject_name = extra_info_data.get('work_subject_name',
                                                                        extra_info_instance.work_subject_name)
            extra_info_instance.work_subject_teacher = extra_info_data.get('work_subject_teacher',
                                                                        extra_info_instance.work_subject_teacher)
            extra_info_instance.save()
        elif extra_info_data:
            ExtraWorkInfo.objects.create(workID=instance, **extra_info_data)

        return instance
