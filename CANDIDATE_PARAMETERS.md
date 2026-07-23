# Exact candidate parameters

| item | exact value | decimal / directed value |
|---|---:|---:|
| \(X\) | \(6000000185827\) | — |
| \(t_0\) | \(129/800\) | \(0.16125\) |
| \(y_0^2\) | \(87677/2500000\) | \(0.0350708\) |
| candidate \(B=t_0+y_0^2/2\) | \(893927/5000000\) | \(0.1787854\) |
| full ceiling \(1-2t_0\) | \(271/400\) | \(0.6775\) |
| finite start | \(690988\) | closed |
| finite/tail split | \(3840000\) | closed overlap |
| finite rows | \(3149013\) | exact |
| global \(T\)-floor | \(791366/10^{12}\) | \(0.000000791366\) |
| \(E_{\max}\) upper | — | \(0.000000233494905212335514\) |
| finite binding lower | — | \(0.000000557871094787\) |
| correction-rate upper | — | \(-1.3631121547576400\) |
| worst Dini ratio upper | — | \(0.99999860767275095\) |
| tail head \(M\) | \(153814\) | — |
| tail \(D\) upper | — | \(0.999720909379940\) |
| tail slack lower | — | \(0.000173520942813\) |

## Closed boxes

Finite later-leg producer box:

\[
t\in
\left[\frac{161250000}{10^9},
\frac{161250001}{10^9}\right],
\qquad y_0^2=\frac{350708}{10^7}.
\]

The P11 stored shards use the exact degenerate \(t\)-box
\([16125/100000,16125/100000]\).

Tail small-height box:

\[
\frac{1872719}{10^7}
<y_0<
\frac{23409}{125000}.
\]

Tail extended top:

\[
\frac{4115519}{5000000}
<\sqrt{1-2t_0}\le
\frac{8231039}{10000000}.
\]

## Finite ladder

| family | \(P\) | \(N\)-range | rows | minimum |
|---|---|---:|---:|---:|
| P11 | \(2,3,5,7,11\) | \(690988\ldots728999\) | 38012 | \(0.000000791366@690988\) |
| P7 | \(2,3,5,7\) | \(729000\ldots818999\) | 90000 | \(0.000315112459@729000\) |
| P5 | \(2,3,5\) | \(819000\ldots1027999\) | 209000 | \(0.000305788807@819000\) |
| P23 | \(2,3\) | \(1028000\ldots3840000\) | 2812001 | \(0.000309285478@1028000\) |

## Runtime lock

```text
image: dbn21a-flint
image ID: sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538
Python dependency: mpmath 1.4.1
```
