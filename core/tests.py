from django.test import TestCase
from django.urls import reverse
from .models import Category, Video, Suggestion
from .forms import SuggestionForm


class CategoryModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name="Test Category", slug="test-cat", icon="📁", order=2
        )
        Category.objects.create(name="First", slug="first", order=1)
        Category.objects.create(name="Last", slug="last", order=3)

    def test_str(self):
        assert str(self.cat) == "Test Category"

    def test_ordering(self):
        cats = list(Category.objects.all())
        assert cats[0].slug == "first"
        assert cats[1].slug == "test-cat"
        assert cats[2].slug == "last"


class VideoModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name="Tech", slug="tech", icon="💻"
        )
        self.video = Video.objects.create(
            title="Test Video",
            youtube_id="abc123",
            category=self.cat,
            channel_name="Test Channel",
            curator_note="Great video",
        )

    def test_str(self):
        assert str(self.video) == "Test Video"

    def test_ordering(self):
        v2 = Video.objects.create(
            title="Newer",
            youtube_id="def456",
            category=self.cat,
            channel_name="Chan",
            curator_note="Note",
        )
        videos = list(Video.objects.all())
        assert videos[0] == v2
        assert videos[1] == self.video

    def test_unique_youtube_id(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Video.objects.create(
                title="Duplicate",
                youtube_id="abc123",
                category=self.cat,
                channel_name="Chan",
                curator_note="Note",
            )

    def test_category_cascade(self):
        self.cat.delete()
        assert Video.objects.count() == 0


class SuggestionModelTest(TestCase):
    def setUp(self):
        self.sugg = Suggestion.objects.create(
            name="Alice",
            department="CS",
            youtube_url="https://youtube.com/watch?v=xyz",
            description="Great course",
        )

    def test_str(self):
        result = str(self.sugg)
        assert "Alice" in result
        assert "pending" in result

    def test_default_status(self):
        s = Suggestion.objects.create(description="Just an idea")
        assert s.status == "pending"

    def test_status_choices(self):
        for choice, _ in Suggestion.STATUS_CHOICES:
            self.sugg.status = choice
            self.sugg.save()
            assert self.sugg.status == choice


class SuggestionFormTest(TestCase):
    def test_valid_empty(self):
        form = SuggestionForm(data={})
        assert form.is_valid()

    def test_valid_full(self):
        form = SuggestionForm(data={
            "name": "Bob",
            "department": "EE",
            "youtube_url": "https://youtube.com/watch?v=test",
            "description": "Good topic",
        })
        assert form.is_valid()

    def test_invalid_url(self):
        form = SuggestionForm(data={"youtube_url": "not-a-url"})
        assert not form.is_valid()
        assert "youtube_url" in form.errors


class HomeViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name="Math", slug="math", icon="📐"
        )
        self.v1 = Video.objects.create(
            title="Algebra", youtube_id="v1",
            category=self.cat, channel_name="Ch",
            curator_note="N1",
        )
        self.v2 = Video.objects.create(
            title="Calculus", youtube_id="v2",
            category=self.cat, channel_name="Ch",
            curator_note="N2", recommended=True,
        )

    def test_status(self):
        resp = self.client.get(reverse("home"))
        assert resp.status_code == 200

    def test_template(self):
        resp = self.client.get(reverse("home"))
        self.assertTemplateUsed(resp, "core/home.html")

    def test_all_videos(self):
        resp = self.client.get(reverse("home"))
        assert len(resp.context["videos"]) == 2

    def test_filter_category(self):
        resp = self.client.get(reverse("home"), {"category": "math"})
        assert len(resp.context["videos"]) == 2
        assert resp.context["selected_category"] == self.cat

    def test_filter_recommended(self):
        resp = self.client.get(reverse("home"), {"recommended": "1"})
        assert len(resp.context["videos"]) == 1
        assert resp.context["videos"][0].recommended is True
        assert resp.context["show_recommended"] is True

    def test_bad_category_returns_404(self):
        resp = self.client.get(reverse("home"), {"category": "nonexistent"})
        assert resp.status_code == 404


class VideoDetailViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="A", slug="a")
        self.video = Video.objects.create(
            title="Test", youtube_id="abc123",
            category=self.cat, channel_name="Ch",
            curator_note="Note",
        )

    def test_valid(self):
        resp = self.client.get(
            reverse("video_detail", kwargs={"youtube_id": "abc123"})
        )
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, "core/video_detail.html")
        assert resp.context["video"] == self.video

    def test_404(self):
        resp = self.client.get(
            reverse("video_detail", kwargs={"youtube_id": "doesnotexist"})
        )
        assert resp.status_code == 404


class SuggestViewTest(TestCase):
    def test_get(self):
        resp = self.client.get(reverse("suggest"))
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, "core/suggest.html")
        assert isinstance(resp.context["form"], SuggestionForm)

    def test_post_valid(self):
        data = {
            "name": "Test User",
            "description": "A good suggestion",
        }
        resp = self.client.post(reverse("suggest"), data)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, "core/suggest_success.html")
        assert Suggestion.objects.count() == 1

    def test_post_invalid(self):
        data = {"youtube_url": "bad-url"}
        resp = self.client.post(reverse("suggest"), data)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, "core/suggest.html")
        assert not resp.context["form"].is_valid()
