"""퀴즈 게임의 Quiz, QuizGame 클래스 정의 모듈."""

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
    """개별 퀴즈 한 문제를 표현하는 클래스."""

    def __init__(self, question, choices, answer, hint=''):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number=None):
        """퀴즈 문제와 선택지를 화면에 출력한다."""
        if number is not None:
            print(f'\n    [문제 {number}]')
        print(f'    {self.question}\n')
        for i, choice in enumerate(self.choices, 1):
            print(f'    {i}. {choice}')

    def check_answer(self, user_answer):
        """사용자의 답이 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self):
        """퀴즈를 딕셔너리로 변환한다 (JSON 저장용)."""
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
        """딕셔너리로부터 Quiz 인스턴스를 생성한다."""
        return cls(
            question=data['question'],
            choices=data['choices'],
            answer=data['answer'],
            hint=data.get('hint', ''),
        )


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스 (메뉴, 풀기, 추가, 목록, 점수, 저장/불러오기)."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.score_history = []

    def _get_number_input(self, prompt, min_val, max_val):
        """범위 내 숫자 입력을 검증하여 반환한다."""
        while True:
            try:
                raw = input(prompt).strip()
                if not raw:
                    print(f'    입력이 비어 있습니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
                    continue
                num = int(raw)
                if num < min_val or num > max_val:
                    print(f'    잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')
                    continue
                return num
            except ValueError:
                print(f'    잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.')

    def _get_text_input(self, prompt):
        """비어 있지 않은 텍스트 입력을 반환한다."""
        while True:
            raw = input(prompt).strip()
            if raw:
                return raw
            print('    입력이 비어 있습니다. 다시 입력하세요.')

    def show_menu(self):
        """메인 메뉴를 화면에 출력한다."""
        print('\n    ========================================')
        print('            나만의 퀴즈 게임')
        print('    ========================================')
        print('    1. 퀴즈 풀기')
        print('    2. 퀴즈 추가')
        print('    3. 퀴즈 목록')
        print('    4. 점수 확인')
        print('    5. 퀴즈 삭제')
        print('    6. 종료')
        print('    ========================================')

    def run(self):
        """메인 게임 루프."""
        try:
            while True:
                self.show_menu()
                choice = self._get_number_input('    선택: ', 1, 6)

                if choice == 1:
                    print('\n    [퀴즈 풀기 - 미구현]')
                elif choice == 2:
                    print('\n    [퀴즈 추가 - 미구현]')
                elif choice == 3:
                    print('\n    [퀴즈 목록 - 미구현]')
                elif choice == 4:
                    print('\n    [점수 확인 - 미구현]')
                elif choice == 5:
                    print('\n    [퀴즈 삭제 - 미구현]')
                elif choice == 6:
                    print('\n    게임을 종료합니다. 안녕히 가세요!')
                    break
        except (KeyboardInterrupt, EOFError):
            print('\n\n    프로그램을 안전하게 종료합니다.')
