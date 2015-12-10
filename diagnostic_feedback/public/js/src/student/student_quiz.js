function StudentQuiz(runtime, element) {
  "use strict";
  /* Javascript for Student view in LMS.*/

  var runtime = runtime,
    element = element;

  var studentQuiz = this;
  studentQuiz.startOver = false;
  studentQuiz.movingToStep = false;

  if (typeof gettext == "undefined") {
    window.gettext = function gettext_stub(string) {
      return string;
    };
    window.ngettext = function ngettext_stub(strA, strB, n) {
      return n == 1 ? strA : strB;
    };
  }

  $(function ($) {

    // selector' for elements that are present in DOM or either required in jQuery.steps callback functions
    var common = new Common(runtime, element),

    // selector' to scope elements for the current XBlock instance, to
    // differentiate multiple diagnostic feedback blocks on one page
      $exportProgress = $('.diagnostic-feedback .export_progress', element),
      $form = $(".diagnostic-feedback .student_view_form", element),

    // child selector' which are either searched in an element already in current XBlock instance scope OR
    // used as combination with some other selector, will be scoped to current XBlock instance (if required)
    // at their usage places
      finalResult = '.diagnostic-feedback .response_body',
      studentViewFormSelector = ".diagnostic-feedback.diagnostic-feedback-student",
      completedStepSelector = ".diagnostic-feedback .completed_step",
      nextActionSelector = '.diagnostic-feedback ul[role="menu"] a[href*="next"]',
      previousActionSelector = '.diagnostic-feedback ul[role="menu"] a[href*="previous"]',
      finishActionSelector = '.diagnostic-feedback ul[role="menu"] a[href*="finish"]',
      cancelActionSelector = '.diagnostic-feedback ul[role="menu"] a[href*="cancel"]',
      choiceSelectedBtnSelector = "input[type='radio']",
      choiceSelector = '.diagnostic-feedback .answer-choice',
      visibleAnswerChoice = 'section.answer-choice.current',
      currentAnswerContainer = ".diagnostic-feedback .current",
      studentViewFormSecSelector = ".diagnostic-feedback .student_view_form section",
      questionId = '.question-id',
      selectedStudentChoice = 'input[type="radio"]:checked',
      exportDataBtnSelector = ".export_data";


    $form.children("div").steps({
      headerTag: "h3",
      bodyTag: "section",
      transitionEffect: "slideLeft",
      enableCancelButton: true,
      onInit: initialize,
      onStepChanging: changeStep,
      onStepChanged: updateResultHtml,
      onCanceled: startOver,
      labels: {
        cancel: gettext("Start Over"),
        current: gettext("Current Step"),
        finish: gettext("Finish"),
        next: gettext("Next"),
        previous: gettext("Previous"),
        loading: gettext("Loading ...")
      }
    });

    resetActions();

    function hideActions() {
      // hide next, previous, finish action button
      // show start over button
      $(nextActionSelector + ', ' + previousActionSelector + ', ' + finishActionSelector, element).hide();
      $(cancelActionSelector, element).show();
    }

    function resetActions() {
      // hide start over button
      // show next, previous, finish action button
      $(nextActionSelector + ', ' + previousActionSelector, element).show();
      $(cancelActionSelector, element).hide();
    }

    function showResult(result) {
      // shows result of student
      $(finalResult, element).html('<div class="html_body">' + result.html_body + '</div>');
      hideActions();
    }

    function getStudentChoice() {
      //Get student selected answer of wizard current question

      var id = $(currentAnswerContainer, element).find(questionId).val();
      var studentChoice = $(currentAnswerContainer, element).find(selectedStudentChoice).val();
      return {'question_id': id, 'student_choice': studentChoice};
    }

    function submitQuestionResponse(isLast, currentStep) {
      // this method is called on valid submission and pass the student's selected value

      var answerHandlerUrl = runtime.handlerUrl(element, 'save_choice');
      var choice = getStudentChoice();
      choice['currentStep'] = currentStep;
      choice['isLast'] = isLast;  //if student given last answer of the question, this flag is true.

      var success = false;
      $.ajax({
        type: "POST",
        url: answerHandlerUrl,
        async: false,
        data: JSON.stringify(choice),
        success: function (response) {
          success = response.success;

          if (success && response.student_result) {
            showResult(response.student_result);
          }
        }
      });
      return success;
    }

    function startOverQuiz() {
      var startOverUrl = runtime.handlerUrl(element, 'start_over_quiz');
      var success = false;
      $.ajax({
        type: "POST",
        url: startOverUrl,
        async: false,
        data: JSON.stringify({}),
        success: function (response) {
          success = response.success;
          resetActions();
        }
      });
      return success;
    }


    function initialize(event) {
      //If the form is reloaded and the user already have answered some of the questions,
      //he will be resumed to where he left.
      var completedStep = parseInt($(completedStepSelector, element).val());

      if (completedStep > 0) {
        studentQuiz.movingToStep = true;
        $form.children("div").steps("setStep", completedStep);
      }
    }

    function changeStep(event, currentIndex, newIndex) {
      //on every step change this method either save the data to the server or skip it.
      var currentStep = currentIndex + 1;
      var isLast = (newIndex == $(studentViewFormSecSelector, element).length - 1);

      return saveOrSkip(isLast, currentStep, currentIndex, newIndex);

    }

    function updateResultHtml(event, currentIndex, newIndex) {
      //If the form is reloaded and the user have answered all the questions,
      //he will be showed the result and start over button.

      var isLast = (currentIndex == $(studentViewFormSecSelector, element).length - 1);
      if (isLast) {
        hideActions();
      }
    }

    function startOver(event) {
      //If user have answered all the questions, start over button shown to again start the Quiz
      studentQuiz.startOver = true;
      $(choiceSelector, element).find(choiceSelectedBtnSelector).removeAttr('checked');
      $form.children("div").steps("setStep", 0);
    }


    function saveOrSkip(isLast, currentStep, currentIndex, newIndex) {
      common.clearErrors();

      // if start over button is click just return and do nothing
      if (studentQuiz.startOver) {

        studentQuiz.startOver = false;
        return startOverQuiz();

      } else if (studentQuiz.movingToStep) {
        studentQuiz.movingToStep = false;
        return true;

      } else {
        if (currentIndex > newIndex) {
          // allow to move backwards without validate & save
          return true;
        }
        var selectedChoice = $(visibleAnswerChoice, element).find(selectedStudentChoice).val();

        if (selectedChoice != "" && selectedChoice != undefined) {
          return submitQuestionResponse(isLast, currentStep);
        } else {
          common.showStudentValidationError({success: false, warning: false, msg: gettext('Please select an answer')});
          return false;
        }
      }
    }

    function getStatus() {
      $.ajax({
        type: 'POST',
        url: runtime.handlerUrl(element, 'get_status'),
        data: '{}',
        success: updateStatus,
        dataType: 'json'
      });
    }

    function updateStatus(response) {
      console.log(response);
      if (response.export_pending) {
        $exportProgress.html(gettext('The report is currently being generated…'));
        setTimeout(getStatus, 1000);
      } else {
        $exportProgress.html(gettext('Report is successfully generated. Downloading…'));
        window.location.href = response.download_url;
      }
    }


    $(studentViewFormSelector, element).on('click', exportDataBtnSelector, function (eventObject) {
      eventObject.preventDefault();

      var link = $(eventObject.currentTarget);
      var handlerUrl = runtime.handlerUrl(element, 'start_export');

      $.ajax({
        type: 'POST',
        url: handlerUrl,
        data: JSON.stringify({}),
        success: updateStatus,
        error: function (response) {
          console.log(response);
        },
        dataType: 'json'
      });

    });

  });
}
