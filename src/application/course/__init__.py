from dishka import Provider, Scope, provide

from src.application.course.answer import (
    CreateAnswerCommand,
    DeleteAnswerCommand,
    UpdateAnswerCommand,
)
from src.application.course.lesson import (
    CreateLessonCommand,
    DeleteLessonCommand,
    UpdateLessonCommand,
)
from src.application.course.course import (
    CreateCourseCommand,
    DeleteCourseCommand,
    UpdateCourseCommand,
)
from src.application.course.question import (
    CreateQuestionCommand,
    DeleteQuestionCommand,
    UpdateQuestionCommand,
)
from src.application.course.test import (
    CreateTestCommand,
    DeleteTestCommand,
    UpdateTestCommand,
)


class CourseCommandsProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    create_course_command = provide(CreateCourseCommand)
    update_course_command = provide(UpdateCourseCommand)
    delete_course_command = provide(DeleteCourseCommand)

    create_test_command = provide(CreateTestCommand)
    update_test_command = provide(UpdateTestCommand)
    delete_test_command = provide(DeleteTestCommand)

    create_question_command = provide(CreateQuestionCommand)
    update_question_command = provide(UpdateQuestionCommand)
    delete_question_command = provide(DeleteQuestionCommand)

    create_lesson_command = provide(CreateLessonCommand)
    update_lesson_command = provide(UpdateLessonCommand)
    delete_lesson_command = provide(DeleteLessonCommand)

    create_answer_command = provide(CreateAnswerCommand)
    update_answer_command = provide(UpdateAnswerCommand)
    delete_answer_command = provide(DeleteAnswerCommand)
