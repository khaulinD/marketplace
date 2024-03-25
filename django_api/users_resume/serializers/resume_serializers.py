from rest_framework import serializers

from users_resume.models import Resume, ExtraResumeInfo


class ExtraResumeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraResumeInfo
        fields = ['resume_course_lvl']

class ResumeSerializer(serializers.ModelSerializer):
    extra_info = ExtraResumeInfoSerializer(required=False)

    class Meta:
        model = Resume
        fields = ['id', 'title', 'creatorID', 'description', 'updated_at', 'created_at', 'min_price', 'extra_info']
        read_only_fields = ['id', "creatorID"]  # Assuming id is read-only

    def create(self, validated_data):
        extra_info_data = validated_data.pop('extra_info', None)
        resume = Resume.objects.create(**validated_data)
        if extra_info_data:
            ExtraResumeInfo.objects.create(resume=resume, **extra_info_data)
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
        instance.min_price = validated_data.get('min_price', instance.min_price)
        instance.save()

        # Update related ExtraResumeInfo model fields
        if extra_info_data and extra_info_instance:
            extra_info_instance.resume_course_lvl = extra_info_data.get('resume_course_lvl',
                                                                        extra_info_instance.resume_course_lvl)
            extra_info_instance.save()
        elif extra_info_data:
            ExtraResumeInfo.objects.create(resumeID=instance, **extra_info_data)

        return instance