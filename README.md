![디깅 소개 이미지](https://user-images.githubusercontent.com/62272445/154015715-fe9d3ac8-1c5b-4dc3-9ebc-ca2e6daf5855.png)

**[👉🏻 diggging 구경하기](https://diggging.com/)**

# ver.1.0.
- 2021/8/24 ver.1.0. : Django, HTML with Django Template, CSS, Vanila JavaScript, AWS
- 2021/12/24 ver.2.0. : DRF, Next.js, AWS, Vercel

<br/>


## 기획의도
대부분의 개발자들은 매일 같이 개발 중 문제들을 해결하기 위해 많은 시간을 쏟습니다.

당장은 앞으로 나아가지 못해 시간 낭비라는 생각이 들어도, 이런 경험이 쌓여

더 훌륭한 개발자가 될 수 있을 것이라는 믿음으로 'Diggging'이라는 서비스를 만들었어요.

Diggging에 기록하고, 다른 개발자들이 겪은 어려움을 찾아보며 더 빨리 성장하세요.

알 수 없는 에러를 발견하더라도 당황하지 않고 이곳에서 검색해보세요!

많은 개발자들이 자신들의 삽질 경험을 공유하고 있을 거에요😃

<br/>
<br/>

## 체크리스트

- [ ]  나는 코딩 중에 삽질을 한 경험이 있다.   ( 1점 )
- [ ]  나는 모든 에러의 해결 방법을 알고 있다. (-3점)
- [ ]  나는 코딩 도중 마주하는 에러들의 해결방법을 자주 잊어버린다. ( 3점 )
- [ ]  나는 코딩 중 겪는 문제를 해결하기 위해 주변의 도움을 구하곤 한다. ( 2점 )
- [ ]  나는 스택오버플로우의 국내버전이 있으면 좋겠다고 생각한 적 있다. (3점)
- [ ]  나는 영어를 충분히 잘해서 구글링하며 얻은 정보를 모두 이해해서 적용할 수 있다.( -1점)
- [ ]  나는 삽질을 한 것에 대한 기록을 효율적으로 남기고 싶다. ( 3점 )
- [ ]  나는 동기부여를 받으며 개발할 수 있는 개발자 커뮤니티를 원한다. ( 3점 )
- [ ]  나는 개발자다. (3점)

나의 점수 = ?

축하합니다! 총합 3점이 넘는다면 당신은 삽질모음.txt의 유저가 될 자격이 충분합니다 🤭

<br/>
<br/>


# 주요기능
- 질문 및 답변 작성
- 답변 채택
- 질문 sorting, filter : (최신순/인기순), (답변 완료, 대기, 채택)
- 댓글 작성
- 게시글 좋아요, 링크공유
- 해시태그
- 계정 프로필 관리
- 검색 기능
<br/>
<br/>

## 추가될 기능

📝 **개발 기록 페이지**
- 개발 중 겪은 어려움과 해결 방법들을 자유롭게 적을 수 있는 개발 기록 페이지 추가 예정입니다.

- 앞으로는 삽질한 기록들을 Digggng에 모두 기록할 수 있게 되고, 많은 개발자들의 삽질 기록 데이터들이 모여 서로에게 도움을 줄 수 있을 것입니다.

📝 **포스트 관련 기능**
- 도움이 되고, 언제든지 마이페이지에서 확인 가능하도록 스크랩 기능을 추가할 예정입니다. 
- 스크랩 한 포스트는 마이페이지의 '스크랩'탭에서 찾아볼 수 있습니다.

📁 **폴더 기능**
- 질문 혹은 기록을 작성할 때 어떤 폴더에 담을지 선택할 수 있습니다.
- 사용자가 직접 폴더를 생성하고, 수정하고, 삭제할 수 있습니다.

- 😮 구 버전 디깅에서는...
    
    언어와 프레임워크에 따라 폴더가 자동 생성되며, 사용자는 언어 / 프레임워크 / 해결여부에 따른 폴더를 선택하여 글을 작성하였습니다. 하지만 몇 가지 한계점이 있었고 고민 끝에, 디깅팀은 자동 폴더 기능을 과감하게 삭제하고, 커스텀 폴더 기능을 제공하기로 하였습니다. 
    이젠 유저들 마음대로 폴더를 만들고, 원하는 분류로 글을 정리할 수 있습니다.
    

🔍 **검색 기능**
- 언어와 프레임워크, 해결 여부에 따른 기본 폴더 기능을 삭제한 대신, 해시태그 기능을 추가하여 검색의 편리성을 보완했습니다.
- 검색 결과 최적화를 위해 지속적인 노력을 쏟을 예정입니다.

🎃 **유저 기능**
**point & level**
- 유저의 활동(질문, 답변, 채택, 기록 작성, 댓글 등)에 따라서 모래알(point)이 쌓이게 됩니다.
- 유저의 모래알이 일정 수치 이상 쌓이면 level up하게 됩니다.
- level은 맨바닥 → 모래성 → 벽돌집 → 빌딩 순이며, 
  삽질경험이 견고한 집을 쌓아 올리는 과정임을 유저들에게 일깨워줍니다.
**account**
- 아이디 찾기
- 회원 탈퇴

🛠 **보완될 사항들**
- 모바일 뷰 및 반응형 웹 완성
- Cross browsing 적용
- SEO 개선
- 게시글  editor 기능 보완

<br/>
<br/>

# Our vision

대부분의 개발자들은 매일 같이 개발 중 문제들을 해결하기 위해 많은 시간을 쏟습니다.

당장은 앞으로 나아가지 못해 시간낭비라는 생각이 들어도, 이런 경험이 쌓여

더 훌륭한 개발자가 될 수 있을 것이라는 믿음으로 삽질모음 서비스를 만들었어요.

내가 지금 겪는 어려움은 다른 누구도 분명히 이전에 겪어본 문제일거에요.

이곳에서 어려움을 공유하고 함께 에러 구덩이를 극복해보아요.

몇 시간 째 답을 알 수 없는 에러에 빠지더라도,

이젠 시간낭비라고 생각하지 마세요!

삽질모음에 기록하고, 다른 개발자들이 겪은 어려움을 찾아보며 더 빨리 성장하세요.

알 수 없는 에러를 발견하더라도 당황하지 않고 이곳에서 검색해보세요!

많은 개발자들이 자신들의 삽질경험을 공유하고 있을 거에요😃

<br/>
<br/>


### 후원하기
Diggging은 아직 개발을 배워가는 과정 중에 있는 학생들이 모여 만든 팀 프로젝트입니다. 
여러분들의 후원 금액은 서버 비용, 교육용 강의 결제 비용 등으로 사용될 수 있습니다. 👩🧑
- 정기후원 : https://www.patreon.com/diggging?fan_landing=true
- 카카오페이 후원
<img src="https://user-images.githubusercontent.com/62272445/154016055-b18c866a-bdc6-4d10-967a-d48ae54b554d.jpg" width="30%" height="30%"/>


<br/>

### 삽질모음을 만든 사람들
김종빈, 김지수, 김현주, 손시형, 이종권 😏


### Contact Info
teamdiggging@gmail.com
