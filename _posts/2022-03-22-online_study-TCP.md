---
layout: single
title:  "TCP 송/수신 원리 - 유튜브 강의(널널한 개발자 TV)"
categories: network
tags: [네트워크, 온라인강의, TCP/IP]
toc: true
toc_sticky : true
author_profile: false
sidebar:
    nav: "docs"
search: true
---
## 링크
+ [널널한 개발자 TV](https://www.youtube.com/watch?v=K9L9YZhEjC0)

## RWX
읽는다는 개념과 쓴다의 개념은 socket에서 각각 receive, send로 표현합니다.  

## socket
tcp/ip등 통신 방법을 추상화 한 것입니다.  

## buffer
송수신 하려는 리소스를 나누어서 메모리에 read하게 하는 개념.  

## NIC
OSI L2에 속하는 H/W(Lan카드).

## TCP segment
메모리에 로드된 나뉘어진 리소스를 갖고있는 buffer에 copy해 입출력 합니다.(buffered I/O)  
buffer를 다시 segment로 쪼개 IP로 보냅니다.  
예를들면, 60개의 직쏘퍼즐 중, buffer size가 4인 곳에 4개씩 나눈다면, 다시 순서를 구분하여 1개씩 segment로 포장합니다.  

## packet
segment를 포장하는 개념. 패킷이 NIC로 내려가면 Frame이라는 개념으로 생각하면 됩니다.  
패킷단위는 IP수준에서 다루게 됩니다.  

## File I/O
client socket에 연결된 file buffer. client 입장에서 tcp buffer(os / network에서 쌓인 버퍼)에서 쌓인 세그먼트를 빠르게 file buffer로 보낼 수 있어야 합니다.  

## receive 속도 > network 속도
file buffer의 receive 속도는 무조건 tcp buffer의 network속도보다 빨라야 합니다.  
그렇지 못할경우, tcp buffer의 size(window size)가 점점 채워지게 됩니다(속도 장애).  
속도 튜닝의 경우 제일 먼저 확인해야 할 것이 receive속도 입니다.  

## ACK(acknowledge)
받은 segment가 옳다는 신호를 송신측(client)에서 수신측(server)으로 보냄. 이 신호가 서버측에 닿아야지만 다음 segment를 받게 됌.  
window size(client측의 tcp buffer크기라고 이해)를 포함하고 있습니다.  

## wait
sever 측에서 ack를 받기 까지 대기하는 상태. 속도지연의 원인. ack에는 window size 정보도 포함 돼있어, (maximum segment size 보다!) **window size가 부족하면 wait상태에 빠집니다**.  

