"""
AI Baseball Game - 숫자야구
사용자는 투수, AI는 타자 역할
3자리부터 10자리까지 선택 가능
"""

import random
import time
from itertools import permutations

DIGITS = list(range(1, 10))


def calculate_strikes_balls(answer, guess):
    """스트라이크와 볼을 계산"""
    length = len(answer)
    strikes = sum(1 for i in range(length) if answer[i] == guess[i])
    common = len(set(answer) & set(guess))
    return strikes, common - strikes


class AIBatter:
    """AI 타자 - 피드백 기반 추측"""
    
    def __init__(self, length):
        self.length = length
        self.guess_history = []
        self.feedback_history = []
    
    def reset(self):
        self.guess_history = []
        self.feedback_history = []
    
    def _is_valid_guess(self, guess):
        """이전 피드백과 일치하는 추측인지 확인"""
        for i, prev_guess in enumerate(self.guess_history):
            prev_strikes, prev_balls = self.feedback_history[i]
            strikes, balls = calculate_strikes_balls(prev_guess, guess)
            if strikes != prev_strikes or balls != prev_balls:
                return False
        return True
    
    def guess_number(self):
        """숫자 추측"""
        if not self.guess_history:
            guess = random.sample(DIGITS, self.length)
        else:
            valid = [list(c) for c in permutations(DIGITS, self.length)
                    if list(c) not in self.guess_history
                    and self._is_valid_guess(list(c))]
            guess = random.choice(valid) if valid else random.sample(DIGITS, self.length)
        
        self.guess_history.append(guess)
        return guess
    
    def record_feedback(self, strikes, balls):
        self.feedback_history.append((strikes, balls))


class BaseballGame:
    """야구 게임"""
    
    def __init__(self):
        self.length = 3
        self.ai_batter = None
        self.answer = None
    
    def _get_length(self):
        """자릿수 입력받기"""
        print("\n몇 자리 숫자로 플레이하시겠습니까? (3-10)")
        
        while True:
            try:
                length = int(input(">> ").strip())
                if 3 <= length <= 10:
                    return length
                print("3-10 사이의 숫자를 입력해주세요!")
            except ValueError:
                print("올바른 숫자를 입력해주세요!")
    
    def _get_answer(self):
        """사용자로부터 정답 입력받기"""
        print(f"\n{self.length}자리 숫자를 입력하세요 (1-9, 중복 없음)")
        
        while True:
            try:
                user_input = input(">> ").strip()
                if len(user_input) != self.length:
                    print(f"{self.length}자리 숫자를 입력해주세요!")
                    continue
                
                digits = [int(d) for d in user_input]
                
                if not all(1 <= d <= 9 for d in digits):
                    print("1-9 사이의 숫자만 사용할 수 있습니다!")
                    continue
                
                if len(set(digits)) != self.length:
                    print("중복된 숫자는 사용할 수 없습니다!")
                    continue
                
                return digits
            except ValueError:
                print("올바른 숫자를 입력해주세요!")
    
    def _format_number(self, digits):
        return ''.join(map(str, digits))
    
    def play_round(self):
        """한 라운드 플레이"""
        self.length = self._get_length()
        self.ai_batter = AIBatter(self.length)
        
        self.answer = self._get_answer()
        answer_str = self._format_number(self.answer)
        print(f"\n정답: {answer_str}")
        print("="*50)
        
        self.ai_batter.reset()
        
        for attempt in range(1, 1000):
            print(f"\n[시도 {attempt}회]")
            
            ai_guess = self.ai_batter.guess_number()
            guess_str = self._format_number(ai_guess)
            print(f"AI의 추측: {guess_str}")
            time.sleep(0.2)
            
            strikes, balls = calculate_strikes_balls(self.answer, ai_guess)
            self.ai_batter.record_feedback(strikes, balls)
            
            if strikes == self.length:
                print(f"🎉 성공! {attempt}회 만에 {answer_str}를 맞췄습니다!")
                return attempt
            
            print(f"⚾ {strikes}스트라이크 {balls}볼")
            time.sleep(0.2)
        
        return attempt
    
    def _print_stats(self, results):
        """통계 출력"""
        if not results:
            return
        
        avg = sum(results) / len(results)
        print(f"총 {len(results)}라운드 플레이")
        print(f"평균 시도 횟수: {avg:.1f}회")
        print(f"최고 기록: {min(results)}회")
        print(f"최악 기록: {max(results)}회")
    
    def start_game(self):
        """게임 시작"""
        print("="*50)
        print("  🏟️  AI Baseball Game  🏟️")
        print("="*50)
        print("\n게임 방법:")
        print("- 3-10자리 숫자(1-9, 중복 없음)를 입력하세요")
        print("- AI가 그 숫자를 맞추려고 시도합니다")
        print("- 정확한 자리에 정확한 숫자 = 스트라이크")
        print("- 다른 자리에 숫자가 존재 = 볼")
        print("- 모든 자릿수가 스트라이크 = 성공!\n")
        
        input("게임을 시작하려면 Enter를 누르세요...")
        
        results = []
        while True:
            attempts = self.play_round()
            results.append(attempts)
            
            print("\n" + "="*50)
            print(f"이번 라운드: {attempts}회 만에 맞춤")
            print(f"평균 시도 횟수: {sum(results) / len(results):.1f}회")
            print("="*50)
            
            if input("\n다시 플레이하시겠습니까? (y/n): ").lower() != 'y':
                break
        
        print("\n" + "="*50)
        print("게임 종료!")
        self._print_stats(results)
        print("="*50)


if __name__ == "__main__":
    BaseballGame().start_game()
