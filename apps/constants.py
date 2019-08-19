class ContentTypes():

    try:
        from django.contrib.contenttypes.models import ContentType
        profile = ContentType.objects.get(app_label='account', model='profile')
        writer = ContentType.objects.get(app_label='account', model='writer')
        tag = ContentType.objects.get(app_label='post', model='tag')
        cut = ContentType.objects.get(app_label='post', model='cut')
        post = ContentType.objects.get(app_label='post', model='post')
        like = ContentType.objects.get(app_label='social', model='like')
        comment = ContentType.objects.get(app_label='social', model='comment')
    except:
        profile = None
        writer = None
        tag = None
        cut = None
        post = None
        like = None
        comment = None

    @classmethod
    def string_to_contenttype(cls, value):
        if value == 'profile':
            return cls.profile
        if value == 'writer':
            return cls.writer
        if value == 'tag':
            return cls.tag
        if value == 'cut':
            return cls.cut
        if value == 'post':
            return cls.post
        if value == 'like':
            return cls.like
        if value == 'comment':
            return cls.comment
        return None