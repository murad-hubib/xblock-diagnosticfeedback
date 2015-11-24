import collections


class StudentResultPresenter(object):
    html_body = ''

    def __init__(self, **data):
        self.html_body = data.get('html_body', '')

    def generate_result(self):
        return {_property: getattr(self, _property) for _property in dir(self) if not _property.startswith('__')
                and not callable(getattr(self, _property))}


class QuizResultMixin(object):
    """
    Return result to student at a quiz completed
    """

    def get_buzzfeed_result(self):
        """
            Calculate the result of BuzzFeed Quiz type
        """
        result = {
            'id': '',
            'name': '',
            'image': '',
            'html_body': 'we cannot calculate your outcome',
        }

        outcomes = {}
        for choice in self.student_choices:
            if outcomes.get(self.student_choices[choice]):
                outcomes[self.student_choices[choice]] += 1
            else:
                outcomes[self.student_choices[choice]] = 1

        # get the outcome of user based on user's selected values
        max_outcome = max(outcomes.iteritems(), key=lambda v: v[1])[0]

        for result in self.results:
            if max_outcome in result['id']:
                result = result
                break

        return result

    def get_diagnostic_result(self):

        """
        Calculate the result of Diagnostic Quiz type

        """
        result = {
            'name': '',
            'min_value': '',
            'max_value': '',
            'image': '',
            'html_body': 'we cannot calculate your outcome'
        }
        total_value = 0.0
        for choice in self.student_choices.values():
            total_value += float(choice)

        for result in self.results:
            if float(result['min_value']) <= total_value <= float(result['max_value']):
                result = result
                break

        return result

    def get_result(self):
        """
        Get result for student based on his/her answer'
        """
        if self.quiz_type == self.BUZZFEED_QUIZ_VALUE:
            result = self.get_buzzfeed_result()
            self.student_result = result['id']
        else:
            result = self.get_diagnostic_result()
            self.student_result = result['name']

        html_body = result['html_body']
        if result['image']:
            html_body = '<img class="result-img" src="{}" alt="{}">{}'.format(result['image'], result['name'],
                                                                              result['html_body'])

        replace_urls = getattr(self.runtime, 'replace_urls', lambda html: html)
        html_body = replace_urls(html_body)

        presenter = StudentResultPresenter(html_body=html_body)
        result = presenter.generate_result()

        return result
