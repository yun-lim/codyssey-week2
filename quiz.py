"""퀴즈 게임의 Quiz, QuizGame 클래스 정의 모듈."""

import json
import os
import random
from datetime import datetime


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
        self.load_data()

    def load_data(self):
        """state.json에서 퀴즈 데이터를 불러온다. 파일이 없거나 손상되면 기본 데이터를 사용한다."""
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get('quizzes', [])]
            self.best_score = data.get('best_score', None)
            self.score_history = data.get('score_history', [])
            count = len(self.quizzes)
            score_info = f', 최고점수 {self.best_score}점' if self.best_score is not None else ''
            print(f'    저장된 데이터를 불러왔습니다. (퀴즈 {count}개{score_info})')
        except FileNotFoundError:
            self._load_defaults()
            print('    저장 파일이 없어 기본 퀴즈 데이터를 사용합니다.')
        except (json.JSONDecodeError, KeyError, TypeError):
            self._load_defaults()
            print('    저장 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.')

    def _load_defaults(self):
        """기본 퀴즈 데이터를 로드한다."""
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = None
        self.score_history = []

    def save_data(self):
        """퀴즈 데이터를 state.json에 저장한다."""
        data = {
            'quizzes': [q.to_dict() for q in self.quizzes],
            'best_score': self.best_score,
            'score_history': self.score_history,
        }
        try:
            with open(STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f'\n    저장 중 오류가 발생했습니다: {e}')

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

    def play_quiz(self):
        """퀴즈를 랜덤 출제하고 점수를 계산한다."""
        if not self.quizzes:
            print('\n    등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.')
            return

        total = len(self.quizzes)
        print(f'\n    총 {total}개의 퀴즈가 있습니다.')
        count = self._get_number_input(
            f'    몇 문제를 풀겠습니까? (1-{total}): ', 1, total
        )

        selected = random.sample(self.quizzes, count)
        score = 0
        hints_used = 0

        print(f'\n    퀴즈를 시작합니다! (총 {count}문제)')

        for i, quiz in enumerate(selected, 1):
            print('\n    ----------------------------------------')
            quiz.display(number=i)

            if quiz.hint:
                print('\n    (힌트를 보려면 0을 입력하세요)')

            answer = self._get_answer_with_hint(quiz)

            if answer == -1:
                hints_used += 1
                answer = self._get_number_input('    정답 입력: ', 1, 4)

            if quiz.check_answer(answer):
                print('    정답입니다!')
                score += 1
            else:
                print(f'    오답입니다. 정답은 {quiz.answer}번입니다.')

        hint_penalty = hints_used * 0.5
        final_score = max(0, score - hint_penalty)
        percentage = int((final_score / count) * 100)

        print('\n    ========================================')
        print(f'    결과: {count}문제 중 {score}문제 정답! ({percentage}점)')
        if hints_used > 0:
            print(f'    (힌트 {hints_used}회 사용, 감점 {hint_penalty}점)')

        is_new_best = False
        if self.best_score is None or percentage > self.best_score:
            self.best_score = percentage
            is_new_best = True
            print('    새로운 최고 점수입니다!')
        print('    ========================================')

        record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': count,
            'correct': score,
            'hints_used': hints_used,
            'score': percentage,
            'is_best': is_new_best,
        }
        self.score_history.append(record)
        self.save_data()

    def _get_answer_with_hint(self, quiz):
        """정답 입력을 받되, 힌트가 있으면 0번으로 힌트를 볼 수 있다."""
        while True:
            try:
                raw = input('\n    정답 입력: ').strip()
                if not raw:
                    print('    입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.')
                    continue
                num = int(raw)
                if num == 0 and quiz.hint:
                    print(f'\n    힌트: {quiz.hint}')
                    return -1
                if num < 1 or num > 4:
                    print('    잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.')
                    continue
                return num
            except ValueError:
                print('    잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.')

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
                    self.play_quiz()
                elif choice == 2:
                    print('\n    [퀴즈 추가 - 미구현]')
                elif choice == 3:
                    print('\n    [퀴즈 목록 - 미구현]')
                elif choice == 4:
                    print('\n    [점수 확인 - 미구현]')
                elif choice == 5:
                    print('\n    [퀴즈 삭제 - 미구현]')
                elif choice == 6:
                    self.save_data()
                    print('\n    게임을 종료합니다. 안녕히 가세요!')
                    break
        except (KeyboardInterrupt, EOFError):
            self.save_data()
            print('\n\n    프로그램을 안전하게 종료합니다.')
