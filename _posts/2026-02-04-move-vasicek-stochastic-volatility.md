---
title: "MOVE 지수를 활용한 확률적 평균 회귀 금리 모형"
date: 2026-02-04
categories: [Quant, Mathematical-Modeling]
tags: [vasicek, black-scholes, stochastic-volatility, move-index, interest-rate, quantlib]
toc: true
toc_sticky: true
---

## 📌 연구 개요

Vasicek 금리 모형의 "상수 변동성" 한계를 극복하기 위해, **MOVE 지수(채권시장 공포지수)**를 활용한 확률적 변동성 금리 모형을 개발했습니다.

**핵심 아이디어**: 채권시장 변동성 지수(MOVE)가 금리의 평균회귀 속도와 변동성에 영향을 준다는 가설을 수학적으로 모델링

---

## 🎯 연구 목적

1. 기존 Vasicek 모형의 고정 파라미터(θ, σ) 한계 극복
2. 시장 상황에 따라 동적으로 변하는 금리 모형 개발
3. 관측 가능한 지표(MOVE)를 활용한 실증적 검증 가능성 확보

---

## 📐 수학적 모형

### 1. 기본 Vasicek 모형

$$dr_t = \kappa(\theta - r_t) \, dt + \sigma \, dW_t$$

| 파라미터 | 의미 |
|---------|------|
| $r_t$ | 순간 단기 금리 |
| $\kappa$ | 평균 회귀 속도 |
| $\theta$ | 장기 평균 금리 (상수) |
| $\sigma$ | 변동성 (상수) |

**한계**: θ, σ가 상수 → 시장 위기 시 변동성 급등 반영 불가

### 2. 확장된 MOVE-Vasicek 모형

**금리 과정:**
$$dr_t = \kappa_r\big(\theta(M_t) - r_t\big) \, dt + \sigma(M_t) \, dW_t^r$$

**MOVE 과정 (CIR):**
$$dM_t = \kappa_m(\bar{M} - M_t) \, dt + \xi_m \sqrt{M_t} \, dW_t^m$$

**연결 함수:**
$$\theta(M_t) = \theta_0 + \theta_1 \cdot \log(M_t)$$
$$\sigma(M_t) = \sigma_0 + \sigma_1 \cdot M_t$$

**상관 구조:**
$$\text{Corr}(dW_t^r, dW_t^m) = \rho$$

### 3. 연결 함수의 경제적 의미

| 파라미터 | 의미 | 해석 |
|---------|------|------|
| $\theta_0$ | 기본 장기 평균 | MOVE 정상 시 균형 금리 |
| $\theta_1$ | MOVE 민감도 | 양수면 공포↑ → 균형금리↑ |
| $\sigma_0$ | 기본 변동성 | 평상시 금리 변동성 |
| $\sigma_1$ | 변동성 민감도 | 공포↑ → 변동성↑ |

---

## 🔧 기술 스택

- **Python**: numpy, scipy, pandas
- **QuantLib**: Vasicek 모형 구현, 채권 프라이싱
- **Data Source**: FRED (금리), Bloomberg (MOVE)

---

## 📊 모형 구현

### 1. MOVE 지수 시뮬레이션 (CIR 과정)

```python
def simulate_move_cir(M0, kappa_m, M_bar, xi_m, T, dt, n_paths):
    """CIR 과정으로 MOVE 지수 시뮬레이션"""
    n_steps = int(T / dt)
    M = np.zeros((n_paths, n_steps + 1))
    M[:, 0] = M0
    
    for t in range(n_steps):
        dW = np.random.normal(0, np.sqrt(dt), n_paths)
        drift = kappa_m * (M_bar - M[:, t]) * dt
        diffusion = xi_m * np.sqrt(np.maximum(M[:, t], 0)) * dW
        M[:, t+1] = np.maximum(M[:, t] + drift + diffusion, 0)
    
    return M
```

### 2. 연결 함수 적용

```python
def theta_linked(M, theta0, theta1):
    """MOVE → 장기 평균 금리 연결"""
    return theta0 + theta1 * np.log(M)

def sigma_linked(M, sigma0, sigma1):
    """MOVE → 변동성 연결"""
    return sigma0 + sigma1 * M
```

### 3. 확장 Vasicek 시뮬레이션

```python
def simulate_extended_vasicek(r0, M_path, kappa_r, theta0, theta1, 
                               sigma0, sigma1, rho, T, dt):
    """MOVE 연동 Vasicek 금리 시뮬레이션"""
    n_steps = len(M_path) - 1
    r = np.zeros(n_steps + 1)
    r[0] = r0
    
    for t in range(n_steps):
        theta_t = theta_linked(M_path[t], theta0, theta1)
        sigma_t = sigma_linked(M_path[t], sigma0, sigma1)
        
        # 상관된 브라운 운동
        dW_m = (M_path[t+1] - M_path[t] - kappa_m*(M_bar-M_path[t])*dt) / (xi_m*np.sqrt(M_path[t]))
        dW_r = rho * dW_m + np.sqrt(1-rho**2) * np.random.normal(0, np.sqrt(dt))
        
        drift = kappa_r * (theta_t - r[t]) * dt
        diffusion = sigma_t * dW_r
        r[t+1] = r[t] + drift + diffusion
    
    return r
```

---

## 📈 기대 효과

| 분야 | 활용 |
|------|------|
| 리스크 관리 | MOVE 수준별 듀레이션 조절 |
| 파생상품 | 변동성 스마일 반영 프라이싱 |
| 자산배분 | MOVE 레짐 기반 채권/주식 비중 |
| 스트레스 테스트 | MOVE 급등 시나리오 시뮬레이션 |

---

## 💡 핵심 인사이트

1. **관측 가능성**: 잠재 변수 대신 실제 관측 가능한 MOVE 지수 활용
2. **경제적 해석**: 파라미터가 명확한 경제적 의미를 가짐
3. **실증 검증**: 역사적 데이터로 모형 검증 가능
4. **실무 적용**: 트레이딩 데스크에서 바로 활용 가능

---

## 📚 이론적 배경

### Vasicek (1977)
- 최초의 평균 회귀 금리 모형
- Affine Term Structure Model의 기초

### Black-Scholes (1973) & Heston (1993)
- 확률적 변동성 개념 도입
- 분산 과정의 CIR 모델링

### Cox-Ingersoll-Ross (1985)
- 음수 방지 확률 과정
- $\sqrt{X_t}$ 확산 계수의 수학적 근거

---

## 🔗 관련 자료

- [QuantLib Documentation](https://www.quantlib.org/)
- [MOVE Index - ICE](https://www.ice.com/publicdocs/ICE_BofAML_MOVE_Index.pdf)
- [Vasicek Original Paper (1977)](https://www.sciencedirect.com/science/article/abs/pii/0304405X77900162)

---

*이 연구는 서강대학교 퀀트 연구 과정의 일환으로 진행되었습니다.*
