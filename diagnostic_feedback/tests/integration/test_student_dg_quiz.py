from .base_test import StudentBaseTest


class StudentDiagnosticStyleTest(StudentBaseTest):

    def test_for_single_group_efficient_team(self):
        self.load_student_view('dg_quiz')

        next_btn = self._get_next_button()
        back_btn = self._get_previous_button()
        startover_link = self._get_startover_button_link()

        self.assertFalse(startover_link.is_displayed(), False)

        self._verify_question(question_order=0, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=1, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=2, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question(wait_until_next_btn_disabled=False)

        self.wait_until_visible(startover_link)

        self.assertTrue(startover_link.is_displayed(), True)

        final_result = self._get_final_result_text()

        self.assertIn('Efficient', final_result)

    def test_for_single_group_mediocre_team(self):
        self.load_student_view('dg_quiz')

        next_btn = self._get_next_button()
        back_btn = self._get_previous_button()
        startover_link = self._get_startover_button_link()

        self.assertFalse(startover_link.is_displayed(), False)

        self._verify_question(question_order=0, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=1, next_btn=next_btn, back_btn=back_btn, choice_idx=1)
        self._submit_question()

        self._verify_question(question_order=2, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question(wait_until_next_btn_disabled=False)

        self.wait_until_visible(startover_link)

        self.assertTrue(startover_link.is_displayed(), True)

        final_result = self._get_final_result_text()

        self.assertIn('Mediocre', final_result)

    def test_for_single_group_awful_team(self):
        self.load_student_view('dg_quiz')

        next_btn = self._get_next_button()
        back_btn = self._get_previous_button()
        startover_link = self._get_startover_button_link()

        self.assertFalse(startover_link.is_displayed(), False)

        self._verify_question(question_order=0, next_btn=next_btn, back_btn=back_btn, choice_idx=2)
        self._submit_question()

        self._verify_question(question_order=1, next_btn=next_btn, back_btn=back_btn, choice_idx=1)
        self._submit_question()

        self._verify_question(question_order=2, next_btn=next_btn, back_btn=back_btn, choice_idx=2)
        self._submit_question(wait_until_next_btn_disabled=False)

        self.wait_until_visible(startover_link)

        self.assertTrue(startover_link.is_displayed(), True)

        final_result = self._get_final_result_text()

        self.assertIn('Awful', final_result)

    def test_for_multi_group(self):
        self.load_student_view('dg_multi_group_quiz')

        next_btn = self._get_next_button()
        back_btn = self._get_previous_button()
        startover_link = self._get_startover_button_link()

        self.assertFalse(startover_link.is_displayed(), False)

        self._verify_question(question_order=0, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=1, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=2, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=3, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=4, next_btn=next_btn, back_btn=back_btn, choice_idx=1)
        self._submit_question()

        self._verify_question(question_order=5, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question(wait_until_next_btn_disabled=False)

        self.wait_until_visible(startover_link)

        self.assertTrue(startover_link.is_displayed(), True)

        final_results = self._get_final_results()

        self.assertIn('Efficient', final_results[0].text)
        self.assertIn('Mediocre', final_results[1].text)

    def test_startover(self):
        self.load_student_view('dg_quiz')
        next_btn = self._get_next_button()
        back_btn_link = self._get_previous_button_link()
        back_btn = self._get_previous_button()
        next_btn_link = self._get_next_button_link()
        startover_link = self._get_startover_button_link()

        self.assertFalse(startover_link.is_displayed(), False)

        self._verify_question(question_order=0, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=1, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question()

        self._verify_question(question_order=2, next_btn=next_btn, back_btn=back_btn, choice_idx=0)
        self._submit_question(wait_until_next_btn_disabled=False)

        self.wait_until_visible(startover_link)

        self.assertFalse(back_btn_link.is_displayed(), False)
        self.assertFalse(next_btn_link.is_displayed(), False)
        self.assertTrue(startover_link.is_displayed(), True)

        final_result = self._get_final_result_text()

        self.assertIn('Efficient', final_result)

        self._verify_startover(next_btn, back_btn, next_btn_link, back_btn_link, startover_link)

        final_result = self._get_final_result_text()

        self.assertIn('Awful', final_result)
