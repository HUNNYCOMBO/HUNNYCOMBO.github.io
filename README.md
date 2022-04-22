# [블로그 바로가기](https://lala-ogu.github.io/)

## 수정 참고 링크
- [syh39](https://syh39.github.io/blog/github_blog_setting/)
- [커스터마이징](https://www.wonseoko.com/jekyll/minimal-mistakes/)

## 주의할 점
- 띄어쓰기는 대부분 하이픈(-)으로 작성
- 태그는 웬만하면 한글로 적었음

## 작성에 사용하는 front matter
```html
---
title: 
excerpt: 
tags: []
header:
  teaser: /assets/images/
  overlay_image: /assets/images/
  overlay_filter: 0.4
---
```
## collapsible block 사용법
details 태그 안에는 markdown 작성을 못하므로, liquid 문법을 이용하여 치환하여 사용하여야합니다.  
모두 본문에 작성합니다.  
```liquid
{% capture summarymd %}이곳에 마크다운 작성{% endcapture %}
{% capture detailsmd %}이곳에 마크다운 작성{% endcapture %}

<details>
  <summary>
    {{ summarymd | markdownify | remove: '<p>' | remove: '</p>' }}
  </summary>
  
  {{ detailsmd | markdownify }}

</details>
```