Diagnostic Feedback
--------------------

This repository provides Diagnostic Feedback Authoring XBlock.

This xblock allows the author to create a series of questions which will assess
and subsequently provide feedback to the student attempting the published quiz.

The xblock provides two types assessments:
* Range Based (Diagnostic)
* Category Based (Like Buzzfeed)

In both, a student is asked to answer multiple choice questions and depending
on her answers, she is classified into one of the defined range or category,
and the associated feedback is displayed to the her.

* In range based (Diagnostic) quiz, first a result is defined as a range, e.g:

    Efficient team (0-5 points)
    Mediocre team (6-9 points)
    Awful team (10-15 points)

  Then each choice within each question is given a numeric value. When the student
  attempts a quiz, the values against all her selected choices are added together
  and compared against each range to determine the appropriate feedback to be shown.

* In category based (Like Buzzfeed), each result is defined as a category and
  each choice within each question is associated with one of the defined categories.
  Finally when the student completes a quiz, frequency of each category against
  selected choices is calculated and the result against the most frequent category
  is displayed as the feedback.

  For example with with categories defined as A, B and C:

    More A answers than any other: You are Small!
    More B answers than any other: You are Medium!
    More C answers than any other: You are Large!

Usage
-----

    Enabling in Studio
    ------------------

You can enable the Diagnostic Feedback XBlocks in Studio by modifying the
advanced settings for your course:

1. From the main page of a specific course, navigate to **Settings** ->
   **Advanced Settings** from the top menu.
2. Find the **Advanced Module List** setting.
3. To enable Diagnostic Feedback for your course, add `"diagnostic-feedback "` to
   the modules listed there.
4. Click **Save changes** button.

   Using Diagnostic Feedback
   -------------------------

See [Usage Instructions](doc/Usage.md)

Installation
------------

Install the requirements into the Python virtual environment of your
`edx-platform` installation by running the following command from the
root folder:

```bash
$ pip install -r requirements.txt
```

Running tests
-------------

First of all, make sure the [XBlock SDK (Workbench)](https://github.com/edx/xblock-sdk)
is installed in the same virtual environment as xblock-diagnostic-feedback.

From the xblock-diagnostic-feedback repository root, run the tests with the
following command:

```bash
$ ./run_tests.py
```

API for native mobile frontends
-------------------------------
**Retrieve fixed data for all Diagnostic Feedback XBlocks in a course:**
```
GET https://<lms_server_url>/api/courses/v1/blocks/?course_id=<course_id>&username=<username>&depth=all&requested_fields=student_view_data
```

Example diagnostic feedback return value:
```
"student_view_data": {
    "quiz_title": "Dummy title",
    "description": "<p>Dummy description</p>",
    "questions": [
        {
            "group": "Default Group",
            "title": "Lorem ipsum",
            "text": "<p>Dummy text</p>",
            "choices": [
                {
                    "name": "<p>Dummy choice one</p>",
                    "value": 1
                },
                {
                    "name": "<p>Dummy choice two</p>",
                    "value": 2
                }
            ],
            "order": "0",
            "id": "2c051c1c-2877-48db-b784-24094fcefbec"
        },
        {
            "group": "Default Group",
            "title": "Dummy diagnostic",
            "text": "<p>Diagnostic text</p>",
            "choices": [
                {
                    "name": "<p>Dummy diagnostic choice</p>",
                    "value": 3
                }
            ],
            "order": "1",
            "id": "69bee8a6-60a1-4083-93ba-8a47f96a18e1"
        }
    ],
    "quiz_type": "DG"
},
```

**Retrieve user's current state**
```
GET https://<lms_server_url>/courses/<course_id>/xblock/<diagnostic_feedback_xblock_id>/handler/student_view_user_state
```

Example return value:
```
{
    "current_step":3,
    "student_result":"Dummy result",
    "completed":true,
    "student_choices":{
        "a1b072ea-e65a-459d-b3a4-98016d96e095":"e1d01ab8-43af-4989-9519-d3880fb7945d",
        "d39a8c6a-a35c-4a25-9f41-6a472169bdac":"e1d01ab8-43af-4989-9519-d3880fb7945d",
        "cdb6e12e-4109-4997-b8ee-77406f434c74":"e1d01ab8-43af-4989-9519-d3880fb7945d"
    }
}
```
