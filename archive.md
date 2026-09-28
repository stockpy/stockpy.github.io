---
layout: page
title: "Archive"
permalink: /archive/
---

<!-- 1. 연도별 바로가기 버튼 (오직 숫자 연도만 표기) -->
<div class="archive-years" style="margin-bottom: 25px; display: flex; flex-wrap: wrap; gap: 10px;">
  {% assign postsByYear = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
  {% for year in postsByYear %}
    <!-- 💡 href="#year-2026" 형태로 앵커 매핑 -->
    <a href="#year-{{ year.name }}" style="font-size: 1rem; font-weight: bold; text-decoration: none; padding: 6px 12px; border: 1px solid #e1e4e8; border-radius: 6px; background: #fafbfc; color: #24292e;">
      {{ year.name }}
    </a>
  {% endfor %}
</div>

<hr style="border: 0; height: 1px; background: #eaecef; margin: 20px 0;">

<!-- 2. 연도별 포스트 리스트 출력 구역 -->
<div class="archive-list">
  {% for year in postsByYear %}
    <!-- 💡 상단 버튼이 클릭 시 찾아올 수 있도록 id="year-2026" 설정 및 제목도 숫자만 표기 -->
    <h2 id="year-{{ year.name }}" style="margin-top: 35px; border-bottom: 1px solid #eaecef; padding-bottom: 8px; color: #0366d6;">
      {{ year.name }}
    </h2>
    <ul style="list-style: none; padding-left: 0;">
      {% for post in year.items %}
        <li style="margin-bottom: 10px; display: flex; align-items: center;">
          <span style="color: #6a737d; font-size: 0.9rem; margin-right: 15px; font-family: monospace;">
            {{ post.date | date: "%m-%d" }}
          </span>
          <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #24292e; font-weight: 500;">
            {{ post.title }}
          </a>
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
</div>

<!-- 💡 테마의 싱글페이지/스크롤 방해 스크립트를 우회하기 위한 강제 스크롤 스타일 -->
<style>
  html {
    scroll-behavior: smooth !important;
  }
</style>