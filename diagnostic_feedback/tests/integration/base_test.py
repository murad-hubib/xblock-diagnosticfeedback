from selenium.webdriver.support.ui import WebDriverWait
from xblock.fields import String
from xblockutils.base_test import SeleniumXBlockTest
from xblockutils.resources import ResourceLoader
# Studio adds a url_name property to each XBlock but Workbench doesn't.
# Since we rely on it, we need to mock url_name support so it can be set via XML and
# accessed like a normal field.
from diagnostic_feedback.quiz import QuizBlock

QuizBlock.url_name = String()

loader = ResourceLoader(__name__)


class DiagnosticFeedbackBaseTest(SeleniumXBlockTest):
    """
    Base class for integration tests.
    Scenarios can be loaded and edited on the fly.
    """

    def _get_previous_button(self):
        return self.browser.find_elements_by_xpath("//ul[@role='menu']/li")[0]

    def _get_previous_button_link(self):
        return self.browser.find_element_by_xpath("//ul[@role='menu']/li/a[@href='#previous']")

    def _get_next_button(self):
        return self.browser.find_elements_by_xpath("//ul[@role='menu']/li")[1]

    def _get_next_button_link(self):
        return self.browser.find_element_by_xpath("//ul[@role='menu']/li/a[@href='#next']")

    def wait_until_has_class_disabled(self, elem):
        """ Need to wait until the given element has disabled class """

        wait = WebDriverWait(elem, self.timeout)
        wait.until(lambda e: 'disabled' in elem.get_attribute('class'),
                   u"{} should be disabled".format(elem.text))

    def _get_final_result_text(self):
        return self.browser.find_element_by_css_selector('div.response_body').text

    def _get_final_results(self):
        return self.browser.find_elements_by_css_selector('div.response_body div.result')

    def load_scenario(self, xml_file, params=None, load_immediately=True, view='student_view'):
        """
        Given the name of an XML file in the xml_templates folder, load it into the workbench.
        """
        params = params or {}
        scenario = loader.render_template("xml_templates/{}".format(xml_file), params)
        self.set_scenario_xml(scenario)
        if load_immediately:
            return self.go_to_view(view)

    def load_student_view(self, xml_file, params=None):
        """
        Load student view in workbench
        """
        self.load_scenario("student_{}.xml".format(xml_file), params=params)

    def load_studio_view(self, xml_file, params=None):
        """
        Load studio view in workbench
        """
        self.load_scenario("studio_{}.xml".format(xml_file), params=params, view='studio_view')


class StudentBaseTest(DiagnosticFeedbackBaseTest):

    def _get_startover_button(self):
        return self.browser.find_elements_by_xpath("//ul[@role='menu']/li")[3]

    def _get_startover_button_link(self):
        return self.browser.find_element_by_xpath("//ul[@role='menu']/li/a[@href='#cancel']")

    def _get_visible_choices(self):
        """
        Return one OR all visible choices
        """
        return [c for c in self.browser.find_elements_by_xpath("//input[@type='radio']") if c.is_displayed()]

    def _is_any_choice_selected(self):
        return any(choice.is_selected() for choice in self._get_visible_choices())

    def _verify_question(self, question_order=0, next_btn=None, back_btn=None, choice_idx=0):
        self.assertFalse(self._is_any_choice_selected(), False)

        if question_order > 0:
            self.assertEqual(back_btn.get_attribute('class'), '')
        else:
            self.assertEqual(back_btn.get_attribute('class'), 'disabled')

        self.assertEqual(next_btn.get_attribute('class'), 'disabled')

        choice = self._get_visible_choices()[choice_idx]
        choice.click()
        self.assertTrue(self._is_any_choice_selected(), True)

        if question_order == 0:
            self.assertEqual(back_btn.get_attribute('class'), 'disabled')
        else:
            self.assertEqual(back_btn.get_attribute('class'), '')

        self.assertEqual(next_btn.get_attribute('class'), '')

    def _verify_startover(self, next_btn, back_btn, next_btn_link, back_btn_link, startover_link):

        startover_link.click()
        self.wait_until_visible(next_btn)
        self.assertFalse(startover_link.is_displayed(), False)
        self.wait_until_has_class_disabled(next_btn)
        self.assertEqual(back_btn.get_attribute('class'), 'disabled')
        self.assertEqual(next_btn.get_attribute('class'), 'disabled')

        self._verify_question(question_order=0, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=1, next_btn=next_btn, back_btn=back_btn, choice_idx=1)
        self._submit_question()

        self._get_previous_button_link().click()

        self.assertEqual(back_btn.get_attribute('class'), '')
        self.assertEqual(next_btn.get_attribute('class'), '')

        self._get_previous_button_link().click()

        self.assertEqual(back_btn.get_attribute('class'), 'disabled')
        self.assertEqual(next_btn.get_attribute('class'), '')

        self._submit_question(wait_until_next_btn_disabled=False)

        self.assertEqual(back_btn.get_attribute('class'), '')
        self.assertEqual(next_btn.get_attribute('class'), '')

        self._submit_question()

        self.assertEqual(back_btn.get_attribute('class'), '')
        self.assertEqual(next_btn.get_attribute('class'), 'disabled')

        self._verify_question(question_order=2, next_btn=next_btn, back_btn=back_btn, choice_idx=2)
        self._submit_question(wait_until_next_btn_disabled=False)

        self.wait_until_visible(startover_link)

        self.assertFalse(back_btn_link.is_displayed(), False)
        self.assertFalse(next_btn_link.is_displayed(), False)
        self.assertTrue(startover_link.is_displayed(), True)

    def _submit_question(self, wait_until_next_btn_disabled=True):
        self.wait_until_visible(self._get_next_button())
        self._get_next_button_link().click()
        if wait_until_next_btn_disabled:
            self.wait_until_has_class_disabled(self._get_next_button())


class StudioBaseTest(DiagnosticFeedbackBaseTest):

    def get_step1_fields(self):
        title = self.browser.find_element_by_css_selector("input[id*='_title']")

        type = self.browser.find_element_by_css_selector("select[id*='_type']")
        description = self.browser.find_element_by_css_selector("textarea[id*='_description']")

        return title, type, description
