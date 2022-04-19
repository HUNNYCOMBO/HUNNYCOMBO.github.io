---
title:  "B-Tree 구조"
tags: [b-tree]
excerpt: mysql index 구조로 사용되는 b-tree에 대해 알아봅니다.
header:
  teaser: /assets/images/etc/b-tree.png
---

## 참고링크
+ [emplam27](https://velog.io/@emplam27/%EC%9E%90%EB%A3%8C%EA%B5%AC%EC%A1%B0-%EA%B7%B8%EB%A6%BC%EC%9C%BC%EB%A1%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EB%8A%94-B-Tree)

## 1. B-Tree란(balanced tree)?
B트리는 이진트리에서 발전한 형태로 모든 leaf node 들이 같은 레벨을 가질 수 있도록 자동으로 밸런스를 맞추는 트리입니다.  
정렬된 순서를 보장하고, 멀티레벨 인덱싱을 통한 빠른 검색을 할 수 있어서 DB에서 사용되는 자료구조 중 한 종류입니다.  
B트리는 **하나의 노드에 많은 수의 정보**를 가지고 있습니다. 최대 M개의 자식을 가질 수 있는 B트리를 M차 B트리라고 합니다.

- leaf node : 자식이 없는 노드
- 내부 노드 : leaf 노드가 아닌 모든 노드
- root node : 최상위 노드


### 1.1. B-Tree의 특징
- node는 최대 $M$개부터 $M/2$개 까지의 자식을 가질 수 있습니다.  
- node에는 최대 $M-1$개 부터 $(M/2) -1$개의 키가 포함될 수 있습니다.
- node의 key가 $x$개 라면, 자식의 수는 $x+1$개 입니다.
- 최소차수는 자식수의 하한값을 의미하며, 최소차수가 t라면 $M=2t-1$을 만족합니다.

![images_emplam27_post_ddbae2c9-da94-457d-bad8-77ff6791255b_B트리 기본 형태](https://user-images.githubusercontent.com/78904413/162943946-c0a04984-59a9-43c1-9122-5b788b5565ae.png)
위 그림은 3차 B트리 입니다(아래가 자식노드). 파란색 부분은 각 노드의 key를 나타냅니다. 빨간색 부분은 자식노드를 가르키는 포인터입니다.  
key들은 노드 안에서 항상 정렬된 값을 가지며, 왼쪽 자식들은 항상 key보다 작은 값을, 오른쪽은 큰 값을 가집니다.  

## 2. key 검색과정
루트노드에서 시작하여 하향식으로 검색을 시작합니다. 18을 검색할 때 루트노드부터 시작하는 예입니다.  

## 3. key 삽입과정
key를 삽입하기 위해서는 두가지 경우가 있습니다. 분할이 일어나는 경우와 일어나지 않는 경우입니다.  

### 3.1. 분할이 일어나지 않는 경우
leaf 노드가 가득 차지 않았다면, 오름차순으로 9를 삽입하는 예 입니다. 이때는 검색과 동일한 방법으로 비교하여 찾습니다.  

![images_emplam27_post_95b4c5c3-c267-4423-865e-778a68ad4a50_B트리 삽입 1-1](https://user-images.githubusercontent.com/78904413/162945843-510f5beb-5981-4d92-b1ca-651d9d90f586.png)


### 3.2. 분할이 일어나는 경우
만일 리프노드에 할당할 수 있는 key가 가득 찬 경우 중앙값에서 노드를 분할합니다. 중앙값은 부모 노드로 병합하거나 새로 생성됩니다.  
이때는 하향식이 아닌 상향식으로 이루어진다고 볼 수 있습니다.  

![images_emplam27_post_4b5003e5-55de-441c-a3ee-15e4db7a2abd_B트리 삽입 2-1](https://user-images.githubusercontent.com/78904413/162945890-1ee76200-a086-431e-b19a-6918c30173a7.png)
![images_emplam27_post_13ab96a4-04cc-42a7-bb01-eac1276bdf67_B트리 삽입 2-2](https://user-images.githubusercontent.com/78904413/162945926-5f67f0d1-514d-496e-a375-8fbbbdbd849d.png)
![images_emplam27_post_d99cdbc8-c5b4-4667-be7d-2589adca45e8_B트리 삽입 2-3](https://user-images.githubusercontent.com/78904413/162945958-a1987919-f4da-433c-9b5c-905393114c0f.png)  

## 4. key 삭제 과정
요소를 삭제하기 위해서는 삭제할 key가 있는 노드를 검색 후 필요에 따라 tree 균형 조정을 해야 합니다.  
삭제 과정을 이하해가진 몇가지 용어를 정의하고 넘어갑니다.  
- inorder predecessor : 노드의 왼쪽 자손에서 가장 큰 key
- inorder successor : 노드의 오른쪽 자손에서 가장 작은 key
- 부모 key : 부모노드의 key들 중 왼쪽 자식으로 본인 노드를 가지고 있는 key값입니다. 단, 마지막 자식 노드의 경우에는 부모의 마지막 key 입니다.


### 4.1. 삭제할 key가 leaf node에 있는 경우
#### 4.1.1. (leaf node)현재 node의 key 개수가 최소 key 개수보다 클 경우
다른 node들에 영향 없이 해당 key를 단순 삭제합니다.  
![images_emplam27_post_e0e2045e-33a2-439f-a781-f6f9af8d0b66_B트리 삭제 1-1](https://user-images.githubusercontent.com/78904413/162947502-f450ece9-962e-488c-b15c-59549c72125b.png)  


#### 4.1.2. (leaf node)현재 node의 key 개수가 최소 key 이하면서, 형제 노드의 key가 최소 key 개수 이상일 경우
![images_emplam27_post_8e7b0f78-ae26-48df-8925-47171c588c48_B트리 삭제 1-2](https://user-images.githubusercontent.com/78904413/162947556-f568acef-65f4-4606-ad03-189365d3d447.png)
최소 key 개수 =1인 경우 예제입니다.  
1. 부모 key 값(14)으로 15를 대체합니다.
2. 최소 key개수 이상의 key를 가진 형제 node를 기준으로 부모 key값을 대체합니다.

#### 4.1.3. (leaf node) 형제 노드의 key가 최소 key의 개수이고, 부모node의 key가 최소 개수 이상인 경우
![images_emplam27_post_dde5e5ae-892c-4d1c-9299-4710023f7531_B트리 삭제 1-3](https://user-images.githubusercontent.com/78904413/162947948-d65491e0-023f-481d-b54d-d32a4877b50c.png)  
1. 18을 삭제한 후, 부모 key를 형제 node와 병합합니다.
2. 부모node의 key 개수를 하나 줄이고, 자식 수 역시 하나를 줄여 B-Tree를 유지합니다.

#### 4.1.4. (leaf node) 자신과 형제, 부모 node의 key 개수가 모두 최소 key 개수인 경우
부모 node를 root node로 한 부분 트리의 높이가 줄어드는 경우이기 때문에 재구조화 과정이 일어납니다. 4.3.2.의 과정으로 이동합니다.  

### 4.2. 삭제할 key가 내부 node에 있고, node나 자식에 key가 최소 key 개수보다 많을 경우
1. 현재 노드의 inorder predesessor 또는 inorder successor와 10의 자리를 바꿉니다.
2. leaf node의 10을 삭제하면, leaf node가 삭제되었을 때의 조건으로 변합니다.

![images_emplam27_post_6d4a5d37-1633-45a1-8225-c6e558031865_B트리 삭제 2](https://user-images.githubusercontent.com/78904413/162949182-c634c112-547c-48ac-b79f-9a76ceea181c.png)  

### 4.3. 삭제할 key가 내부 node에 있고, node에 key 개수가 최소 key 개수만큼있고 해동 node의 자식 key 개수도 모두 최소 key 개수인 경우
모든 node들이 최소 key 개수를 가지므로 재구조화가 일어나는 경우입니다.  

![images_emplam27_post_84dbc50f-fff4-4207-8e27-a34b9043f798_B트리 삭제 3-1](https://user-images.githubusercontent.com/78904413/162949846-8f755598-594c-481a-9209-d9d37360a73d.png)
![images_emplam27_post_e2f82f30-2f9c-4177-a908-1b5333f8e9d6_B트리 삭제 3-2](https://user-images.githubusercontent.com/78904413/162949890-1d24b1e0-9653-44d9-93af-3b25668ff45a.png)


1. 14를 삭제하고, 14의 양쪽 자식을 병합하여 하나의 노드로 만듭니다.
2. 14의 부모key를 인접한 형제 node에 붙인 후, 이전에 병합했던 node를 자식 node로 설정합니다.
3. 부모 node의 개수에 따라 이후 수행과정이 달라집니다.
3.1. 만일 새로 구성된 인접 형제 node가 최대 key 개수를 넘어 갔다면, 삽입 연산의 노드 분할 과정을 수행합니다.
3.2. 만일 인접 형제node가 새로 구성되더라도 원래 14의 부모 node가 최소 key개수보다 작아진다면, 부모 node에 대하여 2번 과정부터 다시 수생합니다.  


