import mongoengine


class LoadedFeedEntry(mongoengine.Document):
    source_name = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)

    def __str__(self):
        return f"{self.title}, {self.date}, {self.source_name}"


class TransformedFeedEntry(mongoengine.Document):
    source_name = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)
    content = mongoengine.StringField()
    summary = mongoengine.StringField()
    num_sentences_in_content = mongoengine.IntField()
