# 1장

## 특별 메서드

- 마술메서드
- 던더 메서드
- **getitem()** 과 같은 메서드를 봤을텐데 이런 애들을 특별 메서드라고 한다
  - 던더 getitem이라고 불러야한다!

## 특별 메서드 연습문제

```java
import collections

Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)]+list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards=[Card(rank,suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

beer_card = Card('7','diamonds')
print(beer_card)
deck = FrenchDeck()
print(len(deck))
print(deck[0]) # Card(rank='2', suit='spades')
```

- **len** ()과 **getitem**() 특별메서드를 구현함으로써 표준 파이썬 시퀀스 처럼 작동

질문

1. 여기서 rank가 뭐에여? `# Card(rank='2', suit='spades')`

## 어떨때 특별 메서드가 사용될까?

- 파이썬 인터프리터가 호출하기 위한 함수이다.
- len(a) 이런 선언은 사실상 **len**()을 호출한거다.
- 특별 메서드 구현하면 사용자 정의 객체도 내장형 객체처럼 작동한다.

## 문자열 표현

- 객체를 문자열로 표현할때는 **str**()보다 **repr**()를 쓸 것
- **str**()은 str()생성자에 의해 호출됨.

```java
>>> a = "Life is too short"
>>> str(a)
'Life is too short'
>>> repr(a)
"'Life is too short'"
```

- repr()은 문자열로 객체를 다시 생성한다.

## 왜 len은 메서드가 아닐까?

- len(),abs() 등은 데이터 모델에서 특별한 대우를 받으므로 메서드라고 부르지 않는다.
- len()이라는 특별 메서드 덕분에 정의한 객체에서 len()을 직접 사용할 수 있다.
- 내장형 객체의 효율성과 언어의 일관성 간의 타협점을 어느정도 찾은 것.

## 파이썬에서 메서드와 함수의 차이?

[[python] 함수(function)와 메서드(method)의 차이, 간단 설명](https://bskyvision.com/entry/python-함수function와-메서드method의-차이-간단-설명)

- 자바에서는 메서드와 함수가 비슷하게 불리는데 파이썬은 어떤 관계가 있을까?
  - 함수는 덧셈, 곱셈같은 기능을 독립적으로 처리
  - 메서드는 **[클래스 및 객체(object)](https://bskyvision.com/735)와 연관되어 있는 함수**
- 다시 돌아가서 파이썬에서 a의 길이는 len(a) 라 하지 a.len()이라 안함
- 헉! 그러면 자바세계에서 전부다 메서드라 하는건 다 객체 종속적이라서??!!? 맹진님 답해줘요

## 가지치기

### 파이썬의 self는 자바의 this랑 어떤 공통점과 차이점이 있을까?

[[Re:Python] 1. self 이해하기](https://velog.io/@magnoliarfsit/RePython-1.-self-이해하기)

[Difference between Python self and Java this](https://stackoverflow.com/questions/21694901/difference-between-python-self-and-java-this)

## self가 뭘까?

- `self`는 **객체의 인스턴스 그 자체를 말한다.**
- 객체 자기자신을 참조하는 매개변수
- 파이썬에서 클래스를 만들고, 클래스 내부에 메소드를 선언할 때에는 반드시 self라는 변수가 첫번째로 들어가야 한다
- 객체지향 언어는 모두 이걸 메소드에 안보이게 전달하지만, 파이썬은 클래스의 메소드를 정의할 때 `self`를 명시한다.
- self로 전달되는건 인스턴스 자체

### self 왜 쓸까?

```java
>>> class Foo:
        def func1():
                print("function 1")

        def func2(self):
                print(id(self))
                print("function 2")
```

- self의 id찍어보면 주소가 나온다.
- 인스턴스의 주솟값을 담고 있다.
- `인스턴스.메서드()` , `클래스.메서드(인스턴스)` 전부 가능하다
  - f2.func2() Foo.func2(f2) 같은 의미
- `self`를 사용함으로 클래스내에 정의한 멤버에 접근할 수 있게된다.
  - 질문 : 이 접근은 클래스의 메서드 안에서 클래스 멤버에 접근한다는거죠?

### self 와 this는 별 차이가 없는거 같은데?

- 솔직히 차이를 잘 모르겠어요!
- https://gist.github.com/shoark7/e57e5874fc0bad9dd995ae5ff3f45abb
  - 파이썬에서 a.introduce()이런 함수를 실행시키면 a.introduce(p)라고 변환돼서 실행된다고 한다.
  - 클래스의 메소드를 실행시킬 때 첫 인자로 인스턴스를 준다!

### 질문

근데 왜 클래스 내부에 선언할때 self가 첫번째로 들어가야 해요?

인스턴스에 의해 생성된 변수인걸 알려주기 위해 self를 쓰는걸까요?

파이썬의 클래스는 그 자체가 하나의 `네임스페이스` 이기 때문에 인스턴스 생성과 상관없이 클래스 내의 메서드를 직접 호출할 수 있다.→ 이게 무슨말이에요?

## 메서드와 함수의 차이

- 메서드는 object(객체)와 연관된 함수
- 함수는 print() type()
- 메서드는 a.split() a.append()느낌!
