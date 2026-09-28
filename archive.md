---
layout: page
title: "연도별 아카이브"
permalink: /archive/
---

<!-- 1. 상단에 연도별 바로가기 버튼 리스트 (클릭 시 해당 연도로 스크롤 이동) -->
<div class="archive-years" style="margin-bottom: 30px; display: flex; flex-wrap: wrap; gap: 15px;">
  {% assign postsByYear = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
  {% for year in postsByYear %}
    <a href="#year-{{ year.name }}" style="font-size: 1.1rem; font-weight: bold; text-decoration: none; padding: 5px 10px; border: 1px solid #ddd; border-radius: 4px; background: #f9f9f9; color: #333;">
      {{ year.name }}년 ({{ year.items | size }})
    </a>
  {% endfor %}
</div>

<hr style="border: 0; height: 1px; background: #eee; margin: 20px 0;">

<!-- 2. 연도별 포스트 출력 구역 -->
<div class="archive-list">
  {% for year in postsByYear %}
    <h2 id="year-{{ year.name }}" style="margin-top: 40px; border-bottom: 2px solid #2a7ae2; padding-bottom: 5px; color: #2a7ae2;">
      {{ year.name }}년
    </h2>
    <ul style="list-style: none; padding-left: 0;">
      {% for post in year.items %}
        <li style="margin-bottom: 12px; display: flex; align-items: center;">
          <span style="color: #888; font-size: 0.9rem; margin-right: 15px; min-width: 50px;">
            {{ post.date | date: "%m-%d" }}
          </span>
          <a href="{{ post.url | relative_url }}" style="text-decoration: none; color: #333; font-weight: 500;">
            {{ post.title }}
          </a>
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
</div>