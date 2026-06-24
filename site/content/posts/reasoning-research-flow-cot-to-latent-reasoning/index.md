---
title: 'Reasoning 연구의 흐름: CoT에서 latent reasoning까지'
date: '2026-06-24T10:22:38+09:00'
lastmod: '2026-06-24T10:22:38+09:00'
slug: reasoning-research-flow-cot-to-latent-reasoning
categories:
- paper-review
tags:
- chain-of-thought
- deepseek-r1
- reasoning
- large-language-models
- latent-reasoning
draft: true
---

reasoning 에 대한 연구 흐름을 짚어 본다.

이 흐름을 따라가다 보면 연구자들의 관심이 어디로 이동했는지가 비교적 선명하게 보인다. 처음에는 `모델이 생각을 글로 드러내게 하면 성능이 오른다`는 사실이 충격이었다. 하지만 시간이 지나면서 질문은 점점 더 근본적인 방향으로 이동했다. 정말 중요한 것은 그럴듯하게 쓰인 사고 과정인지, 아니면 그 사고 과정을 가능하게 하는 내부 계산인지가 핵심 쟁점이 되기 시작한 것이다.

이 변화의 흐름을 보여주는 마일스톤 논문들은 대략 다음과 같다.

| 논문 | 연도 | 핵심 내용 |
| --- | --- | --- |
| *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* | 2022 | 중간 추론 단계를 텍스트로 적게 하면 복잡한 문제 해결 성능이 크게 오른다는 사실을 보여줌 |
| *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning* | 2025 | 사람의 추론 예시 없이도 강화학습만으로 self-reflection, verification 같은 reasoning 행동이 출현할 수 있음을 보임 |
| *From Explicit CoT to Implicit CoT: Learning to Internalize CoT Step by Step* | 2024 | 추론 문장을 점차 제거해도 성능이 유지될 수 있음을 보이며, reasoning이 텍스트가 아니라 내부 상태로 내재화될 수 있음을 제안 |
| *Training Large Language Models to Reason in a Continuous Latent Space* (Coconut) | 2024 | reasoning을 토큰 시퀀스가 아니라 연속적인 latent / hidden-state trajectory로 다루는 방향을 제시 |

## 1. CoT: reasoning은 우선 텍스트로 드러나는 것처럼 보였다

reasoning 연구의 현대적 출발점은 CoT 논문이라고 해도 과장이 아니다. 이 논문이 보여준 것은 단순하지만 강력했다. 모델에게 정답만 묻는 대신, 몇 개의 예시 안에 중간 사고 과정을 포함시키면 수학, 상식, 기호 추론 같은 과제에서 성능이 크게 오른다는 것이다.

이 논문의 의의는 단순히 `프롬프트를 잘 쓰면 성능이 오른다`는 수준이 아니다. 더 중요한 것은 많은 사람들이 이 결과를 통해 `추론은 중간 단계를 언어로 전개하는 과정`이라는 그림을 갖게 되었다는 점이다. 다시 말해 CoT는 reasoning을 눈에 보이는 텍스트 trajectory와 거의 같은 것으로 이해하게 만든 첫 번째 대형 계기였다.

또 하나 중요한 점은 이 논문 제목에 들어 있는 단어가 `creates`가 아니라 `elicits`라는 점이다. 즉 저자들의 원래 문제의식은 추론 능력을 새로 만들었다기보다, 큰 모델 내부에 이미 어느 정도 존재하던 능력을 적절한 형식으로 끌어냈다는 쪽에 더 가까웠다. 그러나 이후 커뮤니티에서 실제로 받아들여진 인상은 조금 더 강했다. CoT 이후에는 자연스럽게 `잘 쓰인 사고 과정이 곧 reasoning`이라는 분위기가 강해졌다.

후속 연구들과 비교해 보면, CoT의 가장 큰 특징은 reasoning을 `표현된 과정`으로 본다는 점이다. reasoning이 어디서 일어나는지, 내부 상태가 어떤 역할을 하는지 같은 질문은 아직 전면에 나오지 않는다. 이 시기의 핵심은 어디까지나 `생각을 쓰게 하라`였다.

## 2. DeepSeek-R1: 생각의 예시 없이도 생각하는 행동은 생길 수 있는가

DeepSeek-R1이 중요한 이유는 CoT의 문제를 완전히 다른 방향에서 다시 던졌기 때문이다. CoT가 `생각 과정을 보여주면 성능이 오른다`고 말했다면, DeepSeek-R1은 `그 생각 과정을 굳이 사람이 써줘야 하는가`라는 질문을 던진다.

이 논문에서 특히 충격적이었던 지점은 DeepSeek-R1-Zero였다. 여기서는 사람이 작성한 reasoning trajectory를 대량으로 주입하지 않고도, 정답 중심의 보상과 형식 제약만으로 모델이 스스로 점검하고, 되돌아보고, 재확인하는 행동을 만들어내는 모습을 보였다. 논문이 강조하는 self-reflection, verification, exploration 같은 패턴은 바로 이 지점에서 나온다.

이 논문의 의의는 reasoning을 더 이상 단순한 모방의 산물로 보지 않게 만들었다는 데 있다. CoT 이후에는 자연스럽게 `좋은 사고 예시를 많이 보여주면 모델도 따라 배운다`는 그림이 강했다. 그런데 DeepSeek-R1은 `정답을 맞히도록 압력을 주기만 해도 reasoning처럼 보이는 행동이 자발적으로 나타날 수 있다`는 가능성을 강하게 밀어붙였다.

이 지점이 CoT와 갈라지는 가장 큰 차이다. CoT는 reasoning을 `텍스트로 드러난 중간 단계`로 생각했다면, DeepSeek-R1은 reasoning을 `목표를 잘 달성하기 위해 형성되는 정책적 행동 패턴`으로 읽게 만든다. 즉 초점이 `무엇을 쓰는가`에서 `어떤 행동이 출현하는가`로 이동한 셈이다.

물론 DeepSeek-R1은 동시에 새로운 혼란도 남겼다. 모델이 길게 생각을 쓰고, 스스로 검증하고, 경로를 바꾸는 모습을 보인다고 해서 그것이 곧바로 `더 깊은 reasoning`을 의미하는지는 별개의 문제이기 때문이다. 바로 그 지점에서 다음 단계의 논의가 시작된다.

## 3. Implicit CoT: reasoning은 꼭 텍스트로 써야만 존재하는가

*From Explicit CoT to Implicit CoT*는 reasoning 연구 흐름에서 꽤 중요한 전환점이다. 이 논문이 던지는 질문은 정면으로 단순하다. 만약 CoT가 정말 reasoning 그 자체라면, 중간 추론 문장을 없애는 순간 성능도 무너져야 한다. 그런데 실제로는 중간 단계를 점차 줄여도 성능이 꽤 유지되는 경우가 관찰된다.

바로 여기서 관점이 바뀐다. reasoning의 본질이 출력된 CoT 문장 그 자체가 아니라, 그 문장을 생성하는 동안 내부 hidden state에서 이루어지는 계산일 수 있다는 해석이 힘을 얻기 시작한다. 다시 말해 CoT는 reasoning 그 자체라기보다, reasoning이 텍스트로 번역된 한 가지 외형일 수 있다는 것이다.

이 논문의 가장 큰 의의는 reasoning 논의의 중심을 `보이는 사고 과정`에서 `내재화된 사고 과정`으로 옮겼다는 데 있다. CoT는 reasoning을 밖으로 꺼내 쓰는 방식에 집중했고, DeepSeek-R1은 그러한 행동이 어떻게 출현하는지를 보여줬다. 반면 Implicit CoT는 한 걸음 더 들어가서, `그런 표현이 없어도 reasoning은 내부에서 계속 일어날 수 있다`는 가능성을 본격적으로 제기한다.

이 차이는 생각보다 크다. CoT와 DeepSeek-R1이 모두 겉으로 보이는 긴 reasoning trajectory를 중요한 단서로 삼았다면, Implicit CoT는 오히려 그 trajectory를 점점 제거해 보면서 reasoning의 핵심이 어디에 남는지를 확인하려고 한다. 따라서 이 논문은 reasoning을 `텍스트 생성 행위`가 아니라 `내부 상태 변화`로 다시 해석하는 출발점에 가깝다.

## 4. Coconut: 그렇다면 추론을 아예 latent space에서만 하게 만들 수 있는가

Coconut은 앞선 논의들을 한 번 더 밀어붙인 작업이다. CoT가 reasoning을 텍스트로 드러내게 했고, Implicit CoT가 reasoning이 hidden state에 내재화될 수 있다고 말했다면, Coconut은 자연스럽게 다음 질문을 던진다. 그렇다면 아예 생각을 토큰으로 풀어 쓰지 않고, latent space 안에서만 reasoning을 진행할 수는 없는가.

이 논문이 제시하는 핵심은 매우 급진적이다. reasoning state를 단어 토큰이 아니라 hidden state 자체로 간주하고, 그것을 다시 다음 입력으로 연결함으로써 연속적인 thought trajectory를 구성하려는 것이다. 여기서는 언어가 사고의 필수 매개가 아니라, 필요할 때만 최종적으로 표면화되는 출력 채널에 가까워진다.

Coconut의 의의는 reasoning 연구의 질문 자체를 바꿔 놓는 데 있다. CoT의 질문은 `어떻게 하면 생각을 잘 쓰게 할 수 있는가`였다. DeepSeek-R1의 질문은 `그런 생각하는 행동을 어떻게 출현시킬 수 있는가`였다. Implicit CoT의 질문은 `그 생각을 꼭 쓰지 않아도 되는가`였다. Coconut은 여기서 더 나아가 `그렇다면 reasoning의 주 무대는 처음부터 언어가 아니었던 것 아닌가`라고 묻는다.

이런 점에서 Coconut은 앞선 논문들과 같은 선상에 있으면서도 결이 다르다. CoT와 DeepSeek-R1은 여전히 긴 텍스트 사고 과정을 중요한 관찰 대상으로 삼는다. Implicit CoT는 그 텍스트를 제거해도 성능이 남는지를 본다. Coconut은 한 단계 더 나아가, reasoning을 관찰 가능한 텍스트가 아니라 애초에 continuous latent computation으로 설계하려고 시도한다.

## 5. 흐름을 다시 묶어 보면

이 네 편을 한 줄로 이어 보면 reasoning 연구의 관심사가 꽤 분명하게 이동해 왔다는 것을 알 수 있다.

CoT는 `생각을 쓰게 하면 성능이 오른다`는 현상을 발견했다. DeepSeek-R1은 `그 생각하는 행동은 사람의 추론 예시 없이도 강화학습으로 나타날 수 있다`고 주장했다. Implicit CoT는 `그렇다면 그 생각은 사실 텍스트가 아니라 내부 상태에 있을 수도 있다`는 방향으로 문제를 뒤집었다. Coconut은 마지막으로 `그 내부 상태를 reasoning의 본 무대로 직접 다뤄 보자`는 시도를 내놓는다.

결국 reasoning 연구는 `잘 쓴 사고 과정`의 발견에서 출발해, `사고 과정이 실제로 어디에서 일어나는가`라는 질문으로 이동하고 있다. 초기에 중요한 것은 모델이 생각을 말하게 만드는 일이었다. 지금 중요한 것은 그 생각이 정말 말의 형태를 필요로 하는지, 아니면 언어는 그저 내부 계산의 표면적 표현에 불과한지 따져보는 일이다.
