# Exact candidate parameters

All theorem inputs are represented exactly. Decimal values in this file are
either exact terminating decimals or explicitly directed summaries of
interval output.

Throughout, \(y_0\) denotes the positive square root of the listed
\(y_0^2\).

## Criterion row

| item | exact value | decimal or directed value |
|---|---:|---:|
| barrier abscissa \(X\) | \(6000000185827\) | exact integer |
| required zeta height \(X/2\) | \(6000000185827/2\) | \(3000000092913.5\) |
| Platt--Trudgian height \(T_{\rm PT}\) | \(3000175332800\) | exact integer |
| verified-height margin | \(350479773/2\) | \(175239886.5\) |
| time \(t_0\) | \(129/800\) | \(0.16125\) |
| height square \(y_0^2\) | \(87677/2500000\) | \(0.0350708\) |
| candidate \(t_0+y_0^2/2\) | \(893927/5000000\) | \(0.1787854\) |
| final-height ceiling \(1-2t_0\) | \(271/400\) | \(0.6775\) |
| canopy top square \(y_0^2+2t_0\) | \(893927/2500000\) | \(0.3575708\) |

Useful exact brackets are

\[
\frac{1872719}{10^7}
<y_0<
\frac{23409}{125000}
\]

and

\[
\frac{8231038}{10^7}
<\sqrt{1-2t_0}\le
\frac{8231039}{10^7}.
\]

## Closed barrier

| item | exact value | directed result |
|---|---:|---:|
| \(x\)-box | \([X,X+1]\) | closed |
| \(y\)-box | \([1809/10000,1]\) | \([0.1809,1]\) |
| \(t\)-box | \([0,129/800]\) | \([0,0.16125]\) |
| floor-square margin | \(y_0^2-(1809/10000)^2=234599/10^8\) | \(0.00234599\) |
| approximation allowance | \(1/800\) | \(0.00125\) |
| displayed-formula error upper | — | \(<0.000356523011600037\) |
| time prisms | \(883\) | consecutive closed coverage |
| minimum prism margin | — | \(>0.519849894613872543374989997\) |
| aggregate winding enclosure | — | contained in \([-8.95,8.95]10^{-13}\) |
| stored matrix components | \(7688\) | \(7688/7688\) contained |
| omitted Taylor tail | — | \(<1.954234593244762\times10^{-22}\) |

The Riemann--Siegel window index is exactly \(N=690988\) throughout the
closed barrier box.

## Finite final-time lane

| item | exact value | decimal or directed value |
|---|---:|---:|
| first window | \(N=690988\) | closed-left |
| finite/tail overlap | \(N=3840000\) | complete shared window |
| finite rows | \(3840000-690988+1\) | \(3149013\) |
| global stored \(T\)-floor | \(791366/10^{12}\) | \(0.000000791366\) |
| effective-error upper \(E_{\max}\) | — | \(0.000000233494905212335514\) |
| finite nonvanishing margin | — | \(\ge0.000000557871094787\) |
| worst Dini ratio upper | — | \(0.99999860767275095\) |
| correction logarithmic-rate upper | — | \(-1.3631121547576400\) |

The later-leg producer box is

\[
t\in
\left[\frac{161250000}{10^9},
      \frac{161250001}{10^9}\right],
\qquad
y_0^2=\frac{350708}{10^7}.
\]

The P11 stored shards use the singleton box

\[
t\in\left[\frac{16125}{100000},\frac{16125}{100000}\right].
\]

Both include the exact \(t_0\).

### Finite ladder

| family | auxiliary primes | \(N\)-range | rows | stored minimum |
|---|---|---:|---:|---:|
| P11 | \(2,3,5,7,11\) | \(690988\ldots728999\) | \(38012\) | \(0.000000791366@690988\) |
| P7 | \(2,3,5,7\) | \(729000\ldots818999\) | \(90000\) | \(0.000315112459@729000\) |
| P5 | \(2,3,5\) | \(819000\ldots1027999\) | \(209000\) | \(0.000305788807@819000\) |
| P23 | \(2,3\) | \(1028000\ldots3840000\) | \(2812001\) | \(0.000309285478@1028000\) |

## Infinite final-time lane

| item | exact value | directed Arb summary |
|---|---:|---:|
| cutoff \(N_*\) | \(3840000\) | closed |
| convolution head \(M\) | \(153814\) | exact |
| error head \(M_{\rm err}\) | \(3000\) | exact |
| contraction \(D\) | — | \(<0.999721\) |
| mollifier upper \(M_{\max}\) | — | \(<1.608290\) |
| normalized flow lower | — | \(>0.0001735326089372\) |
| error upper | — | \(<0.000000011671604\) |
| post-error margin | — | \(>0.0001735209373337\) |

The tail checker evaluates the complete boxes

\[
I_t=
\left[\frac{129}{800},\frac{161250001}{10^9}\right],
\]

\[
I_{\rm box}=
\left[\frac{1872719}{10^7},\frac{23409}{125000}\right],
\qquad
I_{\rm ext}=
\left[\frac{1872719}{10^7},\frac{8231039}{10^7}\right].
\]

The primary independent tail certificates are at 256 and 512 bits. The
broader Python interval checks at 160, 256, and 384 bits are corroborating
replays.

## Runtime lock

The historical finite replay image is

```text
image: dbn21a-flint
image ID: sha256:bedf7303c0be0d35d658d3893cf9f8424aab9f55bc4167644ddf3df564a16538
Python dependency: mpmath 1.4.1
```

The standalone tail and barrier primary checkers use FLINT/Arb. See
`ENVIRONMENT.txt`, `Dockerfile`, and the replay scripts for the complete
toolchain record.
