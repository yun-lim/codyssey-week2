"""Quiz and QuizGame classes for the console quiz game."""

import json
import os


STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'state.json')

DEFAULT_QUIZZES = [
    {
        'question': '"look up"의 의미로 가장 적절한 것은?',
        'choices': ['찾아보다', '올려다보다', '포기하다', '돌아보다'],
        'answer': 1,
        'hint': '모르는 단어가 있을 때 사전에서 ___합니다.',
    },
    {
        'question': '"give up"의 의미로 가장 적절한 것은?',
        'choices': ['나눠주다', '돌려주다', '포기하다', '양보하다'],
        'answer': 3,
        'hint': '더 이상 시도하지 않고 멈추는 것입니다.',
    },
    {
        'question': '"turn down"의 의미로 가장 적절한 것은?',
        'choices': ['돌아서다', '거절하다', '내려놓다', '줄이다'],
        'answer': 2,
        'hint': '누군가의 제안이나 요청을 받아들이지 않는 것입니다.',
    },
    {
        'question': '"put off"의 의미로 가장 적절한 것은?',
        'choices': ['끄다', '벗다', '미루다', '내려놓다'],
        'answer': 3,
        'hint': '해야 할 일을 나중으로 ___하는 것입니다.',
    },
    {
        'question': '"break down"의 의미로 가장 적절한 것은?',
        'choices': ['부수다', '고장 나다', '나누다', '무너뜨리다'],
        'answer': 2,
        'hint': '자동차나 기계가 갑자기 작동을 멈추는 것입니다.',
    },
    {
        'question': '"come up with"의 의미로 가장 적절한 것은?',
        'choices': ['따라잡다', '생각해내다', '참다', '마주치다'],
        'answer': 2,
        'hint': '새로운 아이디어나 해결책을 ___하는 것입니다.',
    },
    {
        'question': '"run into"의 의미로 가장 적절한 것은?',
        'choices': ['달려 들어가다', '도망치다', '우연히 만나다', '부딪히다'],
        'answer': 3,
        'hint': '길을 걷다가 예상치 못하게 아는 사람을 ___합니다.',
    },
]


class Quiz:
    """Represents a single quiz question with choices and an answer."""

    def __init__(self, question, choices, answer, hint=''):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number=None):
        """Display the quiz question and choices."""
        if number is not None:
            print(f'\n    [문제 {number}]')
        print(f'    {self.question}\n')
        for i, choice in enumerate(self.choices, 1):
            print(f'    {i}. {choice}')

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        return user_answer == self.answer

    def to_dict(self):
        """Convert quiz to dictionary for JSON serialization."""
        data = {
            'question': self.question,
            'choices': self.choices,
            'answer': self.answer,
        }
        if self.hint:
            data['hint'] = self.hint
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a Quiz instance from a dictionary."""
        return cls(
            question=data['question'],
            choices=data['choices'],
            answer=data['answer'],
            hint=data.get('hint', ''),
        )
