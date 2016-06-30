from wrapup.models import Stories
from datetime import import datetime, timedelta

class Command(BaseCommand):
    help = 'Updates wrapup'
    def handle(self, *args, **options):
        print("*********************\n*Cleaning wrapup database*\n*********************")

        limit = datetime.now() - timedelta(days=30)
        stories = Stories.objects.filter(storyDate__gte=limit)
        for story in stories:
            story.delete()

