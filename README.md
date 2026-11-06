# makeMoney: CPA 랜딩페이지 사이트

주제별 정보성 랜딩페이지에 CPA 제휴 링크를 넣고 구글 검색으로 방문자를 모으는 정적 사이트입니다.

- 실손보험 / 인터넷·TV 가입 / 정수기 렌탈 / 자동차보험 / 이사 견적 (5개)
- 주소: https://alddeul.com (사이트 이름: 알뜰 가이드)

## 1. CPA 링크 넣기
`config.py`의 `CPA_LINKS`에 텐핑, 애드픽, 링크프라이스 등에서 받은 내 링크를 붙여넣으세요.
링크가 비어 있으면 버튼이 '상담 링크 준비 중'으로 표시됩니다.

## 2. 사이트 공개 (최초 1회)
GitHub 저장소 → Settings → Pages → Source를 **GitHub Actions**로 바꿉니다.
그다음부터는 main 브랜치에 올릴 때마다 자동으로 배포됩니다.

## 2-1. 도메인 연결 (alddeul.com, Cloudflare)
Cloudflare → alddeul.com → DNS → Records 에 아래를 추가 (Proxy status는 **DNS only**, 회색 구름):

| Type | Name | Content |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | jachun05-dot.github.io |

그다음 GitHub → Settings → Pages → Custom domain에 `alddeul.com` 입력 → 확인되면 **Enforce HTTPS** 체크.

## 3. 구글에 등록 (최초 1회)
1. https://search.google.com/search-console 접속 → 속성 추가 → **URL 접두어**에 `https://alddeul.com` 입력
2. 'HTML 태그' 인증 선택 → `content="..."` 안의 값을 `config.py`의 `GOOGLE_SITE_VERIFICATION`에 넣고 배포
3. 인증 후 Sitemaps 메뉴에 `sitemap.xml` 제출

## 페이지 추가
`pages.py`의 `PAGES`에 같은 형식으로 항목을 추가하고, `config.py`의 `CPA_LINKS`에 같은 `offer` 키를 넣으면 됩니다.

## 로컬 빌드
```
python3 build.py   # dist/ 폴더에 결과물 생성
```
