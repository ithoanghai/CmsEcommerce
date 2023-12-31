from django.urls import reverse
from django.contrib.admin.sites import AdminSite

from ..forms import SurveyForm
from ..models import Survey, SurveyAnswer, SurveyQuestion, WaitingListEntry
from ..admin import WaitingListEntryAdmin
from .test import TestCase


class SurveyTestCase(TestCase):

    def setUp(self):
        self.survey = Survey.objects.create(
            label="My Test Survey"
        )
        self.entry = WaitingListEntry.objects.create(email="pinax@awesome.com")
        self.ice_cream_question = self.survey.questions.create(
            question="What is your favorite ice cream flavor?",
            kind=SurveyQuestion.TEXT_FIELD,
            help_text="(e.g. Vanilla, Strawberry, Chocolate)",
            required=True
        )
        self.summer_question = self.survey.questions.create(
            question="What did you do last summer?",
            kind=SurveyQuestion.TEXT_AREA,
            required=False
        )
        self.season_question = self.survey.questions.create(
            question="What is your favorite season?",
            kind=SurveyQuestion.RADIO_CHOICES,
            required=True
        )
        self.spring = self.season_question.choices.create(
            label="Spring"
        )
        self.summer = self.season_question.choices.create(
            label="Summer"
        )
        self.fall = self.season_question.choices.create(
            label="Fall"
        )
        self.winter = self.season_question.choices.create(
            label="Winter"
        )
        self.city_question = self.survey.questions.create(
            question="Select all the cities you have visited",
            kind=SurveyQuestion.CHECKBOX_FIELD,
            required=True
        )
        self.boston = self.city_question.choices.create(
            label="Boston"
        )
        self.denver = self.city_question.choices.create(
            label="Denver"
        )
        self.nashville = self.city_question.choices.create(
            label="Nashville"
        )
        self.danville = self.city_question.choices.create(
            label="Danville"
        )
        self.golf_question = self.survey.questions.create(
            question="Do you like golf?",
            kind=SurveyQuestion.BOOLEAN_FIELD,
            required=True
        )


class SurveyModelTests(SurveyTestCase):

    def test_create_second_survey(self):
        Survey.objects.create(label="Another test survey")
        self.assertEquals(Survey.objects.count(), 2)
        self.assertEquals(Survey.objects.filter(active=False).count(), 1)
        self.assertEquals(Survey.objects.filter(active=True).count(), 1)


class SurveyFormTests(SurveyTestCase):

    def test_survey_form_creation(self):
        form = SurveyForm(survey=self.survey)
        self.assertTrue(len(form.fields), 5)

    def test_survey_strings(self):
        self.assertEqual(str(self.summer), "Summer")

    def test_survey_form_invalid(self):
        form = SurveyForm(
            data={
                self.ice_cream_question.name: "Strawberry"
            },
            survey=self.survey
        )
        self.assertFalse(form.is_valid())

    def test_survey_form_valid(self):
        form = SurveyForm(
            data={
                self.ice_cream_question.name: "Strawberry",
                self.summer_question.name: "Swam in the lake",
                self.season_question.name: self.summer.pk,
                self.city_question.name: [self.nashville.pk],
                self.golf_question.name: True
            },
            survey=self.survey
        )
        self.assertTrue(form.is_valid())

    def test_survey_form_save(self):
        form = SurveyForm(
            data={
                self.ice_cream_question.name: "Strawberry",
                self.summer_question.name: "Swam in the lake",
                self.season_question.name: self.summer.pk,
                self.city_question.name: [self.nashville.pk, self.boston.pk],
                self.golf_question.name: True
            },
            survey=self.survey
        )
        self.assertTrue(form.is_valid())
        form.save(self.entry.surveyinstance)
        answers = self.entry.surveyinstance.answers.all()
        self.assertEquals(answers.count(), 5)
        self.assertEquals(answers.get(question=self.ice_cream_question).value, "Strawberry")
        self.assertEquals(answers.get(question=self.summer_question).value, "Swam in the lake")
        self.assertEquals(answers.get(question=self.season_question).value, self.summer.label)
        self.assertTrue(
            self.nashville.label in answers.get(question=self.city_question).value
        )
        self.assertTrue(
            self.boston.label in answers.get(question=self.city_question).value
        )
        self.assertTrue(answers.get(question=self.golf_question).value_boolean)


class SurveyViewTests(SurveyTestCase):
    """
    Test views.
    """
    def setUp(self):
        super(SurveyViewTests, self).setUp()
        self.email = "pinax@example.com"
        self.signup_urlname = "waitinglist:list_signup"
        self.survey_urlname = "waitinglist:survey"

    def test_list_signup(self):
        """
        Ensure email address is added to waiting list.
        """
        post_data = {
            "email": self.email,
        }
        self.post(self.signup_urlname, data=post_data, follow=True)
        self.response_200()
        self.assertTrue(WaitingListEntry.objects.filter(email=self.email))

    def test_list_signup_duplicate(self):
        """
        Ensure email address already in waiting list is rejected.
        """
        post_data = {
            "email": self.email,
        }
        response = self.post(self.signup_urlname, data=post_data)
        try:
            entry = WaitingListEntry.objects.get(email=self.email)
        except WaitingListEntry.DoesNotExist:
            raise
        self.assertRedirects(
            response,
            reverse("waitinglist:survey", kwargs=dict(code=entry.surveyinstance.code))
        )

        # Form should not validate if we add same email address again.
        response = self.post(self.signup_urlname, data=post_data)
        self.response_200()
        self.assertInContext("form")
        self.assertFalse(response.context["form"].is_valid())

    def test_ajax_list_signup(self):
        """
        Ensure email address is added to waiting list via AJAX post.
        """
        post_data = {
            "email": self.email,
        }
        self.post(
            "waitinglist:ajax_list_signup",
            data=post_data,
            extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        )
        self.response_200()
        self.assertTrue(WaitingListEntry.objects.filter(email=self.email))

    def test_ajax_list_signup_duplicate(self):
        """
        Ensure email address already in waiting list is rejected via AJAX.
        """
        post_data = {
            "email": self.email,
        }
        self.post(
            "waitinglist:ajax_list_signup",
            data=post_data,
            extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        )

        # Form should not validate if we add same email address again.
        self.post(
            "waitinglist:ajax_list_signup",
            data=post_data,
            extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        )
        self.response_200()
        # Check JSON response for failure indicator and form error.

    def test_get_survey(self):
        """
        Ensure a SurveyForm is returned in context for a SurveyInstance.
        """
        response = self.get(self.survey_urlname, code=self.entry.surveyinstance.code)
        self.response_200()
        self.assertInContext("form")
        self.assertTrue(isinstance(response.context["form"], SurveyForm))

    def test_post_survey_answers(self):
        """
        Ensure posted answers are saved as SurveyAnswers for SurveyInstance.
        """
        # Create answers for every question.
        answers = [
            "Chocolate",
            "Trailwork",
            "{}".format(self.summer.pk),
            "{}".format(self.denver.pk),
            "True"
        ]
        keys = [question.name for question in self.survey.questions.all()]
        post_data = dict(zip(keys, answers))

        response = self.post(
            self.survey_urlname,
            data=post_data,
            code=self.entry.surveyinstance.code
        )
        self.assertRedirects(response, reverse("waitinglist:survey_thanks"))

        # Find SurveyAnswer for every question.
        self.assertEqual(
            SurveyAnswer.objects.filter(instance=self.entry.surveyinstance).count(),
            5
        )


class MockRequest(object):
    pass


class WaitingListEntryAdminCSVTest(TestCase):

    def setUp(self):
        self.request = MockRequest()
        self.waitinglist_entry_admin = WaitingListEntryAdmin(WaitingListEntry, AdminSite())
        self.entry = WaitingListEntry.objects.create(email="pinax@awesome.com")

    def test_content_type(self):
        queryset = WaitingListEntry.objects.filter(pk=1)
        csv = self.waitinglist_entry_admin.export_waitinglist_entries(self.request, queryset)
        self.assertEqual(csv["Content-Type"], "text/csv")

    def test_csv_data(self):
        queryset = WaitingListEntry.objects.filter(pk=1)
        csv = self.waitinglist_entry_admin.export_waitinglist_entries(self.request, queryset)
        self.assertIn(b"email,created", csv.content)
        self.assertIn(b"pinax@awesome.com", csv.content)
