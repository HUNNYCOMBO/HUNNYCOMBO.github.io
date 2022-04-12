---
layout: single
title:  "B-Tree 구조"
categories: datastructure
tags: [datastructure, B-Tree]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---

## 1. B-Tree란(balanced tree)?
B트리는 모든 leaf node 들이 같은 레벨을 가질 수 있도록 자동으로 밸런스를 맞추는 트리입니다.  
정렬된 순서를 보장하고, 멀티ㅔ레벨 인덱싱을 통한 빠른 검색을 할 수 있어서 DB에서 사용되는 자료구조 중 한 종류입니다.  
B트리는 하나의 노드에 많은 수의 정보를 가지고 있습니다. 최대 M개의 자식을 가질 수 있는 B트리를 M차 B트리라고 합니다.

- node는 최대 M개부터 M/2개 까지의 자식을 가질 수 있습니다.  
- 
